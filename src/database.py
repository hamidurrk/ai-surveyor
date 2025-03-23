from sqlalchemy import create_engine, Column, String, JSON, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class SurveySession(Base):
    __tablename__ = 'survey_sessions'
    
    session_id = Column(String, primary_key=True)
    questions = Column(JSON)
    responses = Column(JSON)
    consent = Column(Boolean)
    state = Column(String)
    created_at = Column(DateTime, default=datetime.now)

engine = create_engine('sqlite:///surveys.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)