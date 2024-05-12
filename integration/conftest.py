import asyncio
import dotenv
dotenv.load_dotenv("../.env")


import db

def pytest_sessionstart(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    print ("HERE: pytest_sessionstart")
    db.seed_db()

def pytest_sessionfinish(session, exitstatus):
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    db.clean_db()