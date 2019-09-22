import logging
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from . import config

logger = logging.getLogger()
logger.setLevel(config.LOGLEVEL)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_size=20)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

