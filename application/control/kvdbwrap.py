#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import os
RUN_LEVEL = 0
if '/home/atupal' in os.environ.get('HOME', ''):
  RUN_LEVEL = 1

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
    return self.kv.set(key.encode("utf-8"), val)

  def add(self, key, val):
    '''
      同set， 但只在key不存在时起作用
    '''
    #print 'add:', key, val
    if self.get(key):
      return self.kv.set(key.encode("utf-8"), val.encode('utf-8'))
    return self.kv.add(key.encode("utf-8"), val.encode('utf-8'))

  def replace(self, key, val):
    '''
      同set， 但只在key存在时起作用
    '''
    #print 'replace:', key, val
    return self.kv.replace(key.encode("utf-8"), val.encode('utf-8'))

  def delete(self, key):
    #print 'delete:', key
    return self.kv.delete(key.encode('utf-8'))

  def get(self, key):
    #print "get:", key
    return self.kv.get(key.encode('utf-8'))

  def get_multi(self, keys, key_prefix=''):
    '''
      一次获取多个key的值，返回一个key/value的dict
      keys: key的列表，类型必须为list
      key_prefix: 所有key的前缀， 请求时会在所有key前加上该前缀， 返回值里所有的key都会去掉该前缀
    '''
    #print 'get_multi', keys
    keys = [key.encode('utf-8') for key in keys]
    return self.kv.get_multi(keys, key_prefix)

  def get_by_prefix(self, prefix):
    '''
      返回一个list，item为一个(key, value)的tuple
    '''
    #print 'get_by_prefix:', prefix
    return self.kv.get_by_prefix(prefix.encode('utf-8'), max_count=1000, start_key=None)
  
  def getkeys_by_prefix(self, prefix, max_count=1000, start_key=None):
    #print 'getkeys_by_prefix:', prefix
    return self.kv.getkeys_by_prefix(prefix.encode('utf-8'), max_count=max_count)

  def get_info():
    '''
      返回一个kbdb信息的字典
    '''
    return self.kv.get_info()


  ############################################################
  #  my own's method
  ############################################################
  def update(self, key, item):
    """更新某个item

    item: 要更新的key/value map
    """
    items = self.get(key)
    if items:
      items = json.loads(items)
      items.update(item)
      self.set(key, json.dumps(items))
      return json.dumps(items) 
    return None

  def fetch(self, handle=None, start=0, count=100):
    return None
