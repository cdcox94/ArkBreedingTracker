#!/usr/bin/env python
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy
from sqlalchemy.orm import relationship

from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

import datetime

Base = declarative_base()

class PCR_Data(Base):
	__tablename__ = 'DinoType'

	id = Column(Integer, primary_key = True)
	type = Column(VARCHAR(250), nullable = False, unique = True )
	diet = Column(VARCHAR(250), nullable = False)
	tamebable = Column(VARCHAR(250),nullable = False)
	rideable = Column(VARCHAR(250),nullable = False)
	breedable = Column(VARCHAR(250),nullable = False)

class PCR_Calls(Base):
	__tablename__ = 'Dinos'
	id = Column(Integer, primary_key = True)
	name = Column(Integer, ForeignKey('PCR_Data.id'), nullable = False)
	tameLevel = Column(Integer)
	health = Column(FLOAT)
	stamina = Column(FLOAT)
	oxygen = Column(FLOAT)
	food = Column(FLOAT)
	weight = Column(FLOAT)
	meleeDamage = Column(FLOAT)
	mother = Column(Integer)

engine = create_engine( 
    'mysql+pymysql://python:python@10.10.10.3/resultstore')

Base.metadata.create_all(engine) 