#!/usr/bin/env python
#-*- coding:utf-8 -*-
import mailproc
import configparser
import csv
import re
import os
from multiprocessing.dummy import Pool as ThreadPool
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.sql import func
from config import REGBASE

Base = declarative_base()

class Register(Base):
    __tablename__ = 'dumpjrnl'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    boxname = Column(String, nullable=False)
    last_status = Column(String, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    lastrun_date = Column(String, nullable=False)

    def __init__(self, boxname, last_status, count, lastrun_date):
        self.boxname = boxname
        self.last_status = last_status
        self.count = count
        self.lastrun_date = lastrun_date

    def __repr__(self):
        return "<Register('%s','%s', '%s', '%s', '%s')>" \
               % (self.id, self.boxname, self.last_status, self.count, self.lastrun_date)

sqliteng = sqlalchemy.create_engine('sqlite:///' + REGBASE)
metadata = Base.metadata.create_all(sqliteng)
session_factory = sessionmaker(bind=sqliteng)
Session = scoped_session(session_factory)

tpool = ThreadPool(4)

config = configparser.ConfigParser()

# TODO: processing config exception
config.read('settings.cfg')
# TODO: add option set backing up root directory
backuproot = config.get('main', 'backup_root')
# TODO compress folder
compress = config.get('main', 'compress')
# backup mode - simulation (0) or real backup (1)
backupmode = config.get('main', 'backupmode')
loglevel = config.get('main', 'loglevel')
addresses = config.get('main', 'addressfile')

csv.register_dialect('addr', delimiter=';', quoting=csv.QUOTE_NONE)

reader = csv.DictReader(open(addresses), dialect="addr")

pool = {}

# TODO: add return values for registration in base
def multi_run_wrapper(args):
    return mailproc.imapclones(*args)

for row in reader:
    for column, value in row.items():
        pool.setdefault(column, []).append(value)

n = 0
args = []
protocol = 'pop'
# DONE: get imap server by email

for k in pool['address']:
    login = k
    basedomain = re.split("@", k)[1]
    if pool['protocol'][n] == 'imap':
        srvname = "imap." + basedomain
        protocol = 'imap'
    else:
        srvname = "pop." + basedomain
    passw = pool['pass'][n]
    # debug
    n += 1
    print(srvname)
    print(passw)
    if not os.path.exists(backuproot + '/' + k):
        os.mkdir(backuproot + '/' + k)
    localfolder = backuproot + '/' + k
    element_session = Session()
    args.append((srvname, k, 'INBOX', localfolder, passw, protocol, element_session))

tpool.map(multi_run_wrapper, args)
tpool.close()
tpool.join()
