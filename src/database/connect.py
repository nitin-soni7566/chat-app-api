from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.core.config import settings
import redis
import boto3


engine = create_engine(settings.DATABASE_URL)


Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


def get_session():
    return Session()


##################
# Redis Connection
##################


def init_redis_pool():
    redis_host = settings.REDIS_HOST
    redis_port = settings.REDIS_PORT
    redis_pass = settings.REDIS_PASSWORD
    pool = redis.ConnectionPool(
        host=redis_host, port=redis_port, password=redis_pass, db=0
    )
    return pool


redis_client = redis.Redis(connection_pool=init_redis_pool())


s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)
