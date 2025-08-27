# 用于创建数据库连接引擎，根据不同的数据库类型以及配置信息，建立起与数据库的连接通道。
#后续所有的数据库操作都基于这个引擎来进行传递和执行
from sqlalchemy import create_engine 
# 同时导入sessionmaker，用于创建会话工厂
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///liquid.db'

engine=create_engine(DATABASE_URL, echo=True)
# 
SessionLocal =sessionmaker(autocommit=False, autoflush=False, bind=engine)
