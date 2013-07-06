#!/bin/bash/env python
# -*- coding: utf-8 -*-

'''
    db_methods

    author: atupal
'''

try:
    import sae.const

    '''
    sae.const.MYSQL_DB      # 数据库名
    sae.const.MYSQL_USER    # 用户名
    sae.const.MYSQL_PASS    # 密码
    sae.const.MYSQL_HOST    # 主库域名（可读写）
    sae.const.MYSQL_PORT    # 端口，类型为，请根据框架要求自行转换为int
    sae.const.MYSQL_HOST_S  # 从库域名（只读）
    '''

    MYSQL_DB     = sae.const.MYSQL_DB
    MYSQL_USER   = sae.const.MYSQL_USER
    MYSQL_PASS   = sae.const.MYSQL_PASS
    MYSQL_HOST   = sae.const.MYSQL_HOST
    MYSQL_PORT   = sae.const.MYSQL_PORT
    MYSQL_HOST_S = sae.const.MYSQL_HOST_S

except:
    import ConfigParser
    config = ConfigParser.RawConfigParser()
    with open('/home/atupal/src/github/3gqq/dianzan/server-sae/env.cfg','r') as fi:
        config.readfp(fi)
        MYSQL_DB     = config.get('mysql', 'MYSQL_DB')
        MYSQL_USER   = config.get('mysql', 'MYSQL_USER')
        MYSQL_PASS   = config.get('mysql', 'MYSQL_PASS')
        MYSQL_HOST   = config.get('mysql', 'MYSQL_HOST')
        MYSQL_PORT   = config.get('mysql', 'MYSQL_PORT')
        MYSQL_HOST_S = config.get('mysql', 'MYSQL_HOST_S')



import MySQLdb

def init_db():
    db = MySQLdb.connect(host = MYSQL_HOST, port = int(MYSQL_PORT), db = MYSQL_DB , user = MYSQL_USER, passwd = MYSQL_PASS )
    return db

def create_table(db):
    cursor = db.cursor()
    cursor.execute(r'''
    create table task
        (
                id int unsigned not null auto_increment primary key,
                uid char(50),
                ttl int default 0,
                url char(250),
                inc int default 10,
                pos text(1000) default "",
                neg text(1000) default "",
                frr text(5000) default "",
                message char(100)
        );
            ''')
    del cursor

def add_task(db, uid, url, ttl = 10, inc = 10, pos = "", neg = "", frr = ""):
    cursor = db.cursor()
    cursor.execute(r'''
        insert task (uid, ttl, url, inc, pos, neg, frr) values ("%s", %d, "%s", %d, "%s", "%s", "%s");
            ''' % (uid, ttl, url, inc, pos, neg, frr) )
    db.commit()
    db.close()
