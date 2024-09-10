from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLSession
from sqlalchemy.orm import sessionmaker

from edl_api import settings


def get_session():
    return LocalSession


Engine = create_engine(settings.DAGDB_CONNECTSTRING)
"""Database engine.

Should not be used directly in most cases. Use `database.Session` instead.
"""

LocalSession = sessionmaker(bind=Engine)
"""Database session used for all database operations.

Should not be used directly in most cases. Use `database.Session` instead.
"""

Session = Annotated[sessionmaker[SQLSession], Depends(get_session)]
"""Database session predefined for FastAPI Dependencie injection.

Can automatically be injected in FastAPI routes and used to interact with the database.
```python
@app.get("/route")
def route(session: Session):
    with session.begin() as s:
         # do something
    ...
```

Note: use Session.begin() if you want changes to be commited automatically

---
"""
