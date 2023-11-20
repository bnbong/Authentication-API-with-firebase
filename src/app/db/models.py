# import uuid
#
# from sqlalchemy import String, Column
# from sqlalchemy.dialects.mysql import BINARY
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import DeclarativeMeta
#
# Base: DeclarativeMeta = declarative_base()
#
#
# def generate_uuid():
#     return uuid.uuid4().hex
#
#
# class User(Base):
#     __tablename__ = "users"
#
#     uid = Column(BINARY(28), primary_key=True, default=generate_uuid)
#     name = Column(String(50))
#     email = Column(String(100))
#
#     def __repr__(self):
#         return f"<User(name={self.name}, email={self.email})>"
