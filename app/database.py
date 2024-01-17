# Importing necessary modules from SQLAlchemy for ORM and database interaction
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL. Here we're using PostgreSQL, but you could also use SQLite or other databases.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:roblion23@localhost/fastapi"

# Creating the SQLAlchemy engine that will handle the communication with the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Creating a local session factory. This will be used to get a session that is local to the current thread.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating the base class for declarative models. This is where we define our models (tables).
Base = declarative_base()

# Dependency for getting a database session. This will be used in FastAPI dependencies.
def get_db():
    # Creating a new session
    db = SessionLocal()
    try:
        # Yielding the session to be used in the request
        yield db
    finally:
        # Closing the session
        db.close()