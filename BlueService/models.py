from sqlalchemy import Column, Integer, Text, DATETIME, ForeignKey, Float
from BlueService.database import Base, engine, SessionLocal
from sqlalchemy.orm import relationship



class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    balance = Column(Float)
    status = Column(Integer)
    join_date = Column(DATETIME)
    is_verified = Column(Integer)

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    support_group_id = Column(Integer)
    support_username = Column(Text)
    wellcome_message = Column(Text)
    help_text = Column(Text)
    min_increase = Column(Integer)
    max_increase = Column(Integer)
    charge_report_topic = Column(Integer)
    backup_topic = Column(Integer)
    bot_status = Column(Integer) # 1 : on, 0 : off
    topic_group = Column(Integer)
    buy_report_channel = Column(Integer)

class ForcedJoinChannels(Base):
    __tablename__ = "forced_join_channels"
    id = Column(Integer , autoincrement=True, primary_key=True)
    channel_id = Column(Integer, unique=True, nullable=True)
    channel_link = Column(Text)
    channel_name = Column(Text)

class ForcedJoinUsers(Base):
    __tablename__ = "forced_join_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    channel_id = Column(Integer, ForeignKey("forced_join_channels.channel_id", ondelete="CASCADE"))

class Admins(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)

class Tickets(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    text = Column(Text)
    datetime = Column(DATETIME)

class TicketReplies(Base):
    __tablename__ = "tickets_replies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id", ondelete="CASCADE"))
    user_id = Column(Integer)
    text = Column(Text)
    datetime = Column(DATETIME)

# Create tables
Base.metadata.create_all(engine)