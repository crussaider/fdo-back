from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.config import POSTGRES

engine = create_engine(POSTGRES.URL, )

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
