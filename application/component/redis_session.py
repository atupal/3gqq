import pickle
from datetime import timedelta
from uuid import uuid4
from werkzeug.datastructures import CallbackDict
#from flask.sessions import SessionInterface, SessionMixin
from flask.session import SessionInterface, SessionMixin
import json
import time


import os
# store session use Redis!
if '/home/atupal' in os.environ.get('HOME', '') and False:
  #from redis import Redis
  from redis import StrictRedis
# store session use sae KVDB!
else:
  from application.control import kvdbwrap
  class StrictRedis(object):
    def __init__(self, *args, **kwargs):
      pass

    def get(self, key):
      try:
        with kvdbwrap.KVDB() as kv:
          ret = json.loads( kv.get(key) )
          if int(time.time()) - int(ret.get('init_time')) > int(ret.get('expire')):
            return self.delete(key)
          return ret.get('val')
      except TypeError:
        pass
      except Exception as e:
        print e
        import traceback, sys
        traceback.print_exc(file=sys.stdout)
        return None
    
    def delete(self, key):
      with kvdbwrap.KVDB() as kv:
        kv.delete(key)
      return None

    def setex(self, key, val, expire):
      with kvdbwrap.KVDB() as kv:
        ret = {}
        ret['val'] = val
        ret['init_time'] = int(time.time())
        ret['expire'] = str(expire)
        kv.add(key, json.dumps(ret))

class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, sid=None, new=False):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.sid = sid
        self.new = new
        self.modified = False


class RedisSessionInterface(SessionInterface):
    serializer = pickle
    session_class = RedisSession

    def __init__(self, redis=None, prefix='session:'):
        if redis is None:
            #redis = Redis()
            redis = StrictRedis(host='localhost', port=6379, db=1)
        self.redis = redis
        self.prefix = prefix

    def generate_sid(self):
        return str(uuid4())

    def get_redis_expiration_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        #return timedelta(days=1)
        return timedelta(days=7)

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        val = self.redis.get(self.prefix + sid)
        if val is not None:
            data = self.serializer.loads(val)
            return self.session_class(data, sid=sid)
        return self.session_class(sid=sid, new=True)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        if not session:
            self.redis.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name,
                                       domain=domain)
            return
        redis_exp = self.get_redis_expiration_time(app, session)
        cookie_exp = self.get_expiration_time(app, session)
        val = self.serializer.dumps(dict(session))
        self.redis.setex(self.prefix + session.sid, val,
                         int(redis_exp.total_seconds()))
        response.set_cookie(app.session_cookie_name, session.sid,
                            expires=cookie_exp, httponly=True,
                            domain=domain)
