# -*- coding: utf-8 -*-
"This is a module for debug kbdb of sae"

import redis


class KVClient(object):
  def __init__(self, debug=0):
    self.rclient = redis.StrictRedis(host='localhost', port=6379, db=1)

  def set(self, key, val, min_compress_len=0):
    """设置key的值为val, 成功则返回True

    min_compress_len启用zlib.compress压缩val的最小长度， 如果val的长度大于此值则启用压缩，0表示不压缩 
    """
    return self.rclient.set(key, val)

  #def add(self, key, val, min_compress_len=0):
  def add(self, *args, **kwargs):
    """同set，但只在key存在时起作用
    """
    return self.set(*args, **kwargs)

  def replace(self, key, val, min_compress_len=0):
    """同set，但只在key存在时起作用
    """
    pass

  def delete(self, key):
    """删除key，成功返回1, 失败返回0
    """
    return self.rclient.delete(key)

  def get(self, key):
    """从kvdb中获取一个key的值。成功返回key的值，失败则返回None
    """
    return self.rclient.get(key)

  def get_multi(self, keys, key_prefix=''):
    """从kvdb中一次获取多个key的值。返回一个key/value的dict

    keys: key的列表，类型必须为list
    key_prefix: 所有key的前缀。请求时会在所有的key前面加上该前缀，返回值里所有的key都会去掉该前缀。
    """
    pass

  def get_by_prefix(self, prefix, max_count=100, start_key=None):
    """从kvdb中查找指定前缀的key/value pair。返回一个list，该list中每个item为一个(key, value)的tuple

    prefix: 需要查找的key的前缀
    max_count: 最多返回的item个数，默认为100
    start_key: 指定返回的第一个item的key，该key不包含在返回中
    """
    keys = self.rclient.keys()
    ret = []
    for key in keys:
      if key.startswith(prefix):
        ret.append(( key, self.rclient.get(key) ))
    return ret

  def getkeys_by_prefix(self, prefix, max_count=100, start_key=None):
    """从kvdb中查找指定前缀的key。返回符合条件的key的list。

    prefix: 需要查找的key的前缀
    max_count: 最多返回的item个数，默认为100
    start_key: 指定返回的第一个item的key，该key不包含在返回中
    """
    keys = self.rclient.keys()
    ret = []
    for key in keys:
      if key.startswith(prefix):
        ret.append(key)
    return ret

  def get_info(self):
    """获取本应用kvdb的统计数据，返回一个字典

    {
      'outbytes': 126,
      'total_size': 3,
      'inbytes': 180,
      'set_count': 60,
      'delete_count': 21,
      'total_count': 1,
      'get_count': 42
    }
    """
    pass

  def disconnect_all(self):
    """关闭kvdb连接
    """
    for c in self.rclient.client_list():
      self.rclient.client_kill(c.get('addr'))
    return True

  def __del__(self):
    self.disconnect_all()

  ####################################################
  #   my methods
  ####################################################
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

  def sync_with_sae(self):
    """同步sae上kvdb的数据
    """
    for key in self.rclient.keys():
      self.delete(key)
    url = 'http://3gqq67.sinaapp.com/kvdbmanage/raw/all'
    import requests, json
    s = requests.Session()
    s.post('http://3gqq67.sinaapp.com/login', data = {'email': '', 'password': ''})
    content = s.get(url).content
    #print content
    ret = json.loads(content)
    for key_val in ret:
      self.set(key_val[0], key_val[1]) 
# 示例代码:
# 
#   import sae.kvdb
# 
#   kv = sae.kvdb.KVClient()
# 
#   k = 'foo'
#   kv.set(k, 2)
#   kv.delete(k)
# 
#   kv.add(k, 3)
#   kv.get(k)
# 
#   kv.replace(k, 4)
#   kv.get(k)
# 
#   print kv.get_info()
#   服务限制:
# 
#     存储空间：100G
#     最大记录条数：1,000,000,000
#     key的最大长度：200 Bytes
#     value的最大长度：4M
#     get_multi获取的最大KEY个数：32

if __name__ == '__main__':
  client = KVClient()
  client.sync_with_sae()
  del client
