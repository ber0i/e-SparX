
from typing import Annotated
from fastapi import Depends, Header

from edl_api.schemas import User

def get_user_id(x_user_id: str = Header(title="X-User-ID", description="User ID of the acting user. Used to identify the user")):
    """ Requires, that the user id is added to the request in order to identify the user.

    WARNING: This is no way to authenticate a user. Any string will be taken as valid user id.
    """

    return User(id=x_user_id)

IdentifiedUser = Annotated[User, Depends(get_user_id)]
""" Identify the user making the request

Inject this on every route, that needs to know the acting user

```python
@app.get("/route")
def my_route(user_id: IdentifiedUser):
    # do something
```

WARNING: This is no way to authenticate a user. Any string will be taken as valid user id.
"""
