#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class KVDB(object):
  '''
    a simple wrapper of kvdb
  '''

  def __init__(self):
    if RUN_LEVEL:
      import sae_ as sae
    else:
      import sae.kvdb
    self.kv = sae.kvdb.KVClient(debug=1)

  def __exit__(self, type, value, traceback):
    self.kv.disconnect_all()

  def __enter__(self):
    return self

  def set(self, key, val):
    #print 'set:', key, val
    dataVersion = json.loads(self.get('dataVersion'))
    dataVersion['dataVersion'] = int(time.time() * 1000)
    self.kv.set('dataVersion', json.dumps(dataVersion).encode('utf-8'))
    return self.kv.set(key.encode("utf-8"), val)

  def add(self, key, val):
    '''
      同set， 但只在key不存在时起作用
    '''
    #print 'add:', key, val
    dataVersion = json.loads(self.get('dataVersion'))
    dataVersion['dataVersion'] = int(time.time() * 1000)
    self.set('dataVersion', json.dumps(dataVersion))
    if key.encode('utf-8').startswith('goodsId#'):  # 自动生成一个最小的商品ID
      keys = self.getkeys_by_prefix(key)
      for i in xrange(300):
        if "%s%.3d" % (key.encode('utf-8'), i) not in keys:
          if self.get(key):
            return self.kv.set("%s%.3d" % (key.encode('utf-8'), i), val.encode('utf-8'))
          return self.kv.add("%s%.3d" % (key.encode('utf-8'), i), val.encode('utf-8'))
      return 'no enough id'
    elif key.encode('utf-8').startswith('sortId#'):  # 自动生成一个最小的分类ID
      keys = self.getkeys_by_prefix("sortId#")
      if key.lstrip("sortId#") == "000":
        begin = 0
        end = 300
      elif key.lstrip("sortId#") == "300":
        begin = 300
        end = 600
      for i in xrange(begin, end):
