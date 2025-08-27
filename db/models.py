from sqlalchemy import Column, Integer, String, Float,Date
from sqlalchemy.ext.declarative import declarative_base

# 用于创建一个基类，后续定义的所有表示数据库表的类都将集成这个基类
# 这个基类会自动处理很多与数据库映射相关的底层逻辑，例如表名，列的定义与数据库实际表结构的关联
Base =declarative_base()

#数据库表模型类，将会与数据库中的transactions表进行映射(通过__tablename__属性指定表名)
class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    stock_symbol = Column(String, nullable=False)
    stock_name = Column(String, nullable=False)
    transaction_type = Column(String, nullable=False)  # 'buy' or 'sell'
    quantity = Column(Integer, nullable=False)
    price_per_share = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)


class Stocks(Base):
    __tablename__ = 'stocks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_symbol = Column(String, nullable=False)
    stock_name = Column(String, nullable=False)
