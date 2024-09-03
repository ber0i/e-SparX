from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from edl_api.routes import RegisterRouter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


app.include_router(RegisterRouter, prefix="/register")


@app.get("/", tags=["Welcome"])  # tags are used to group the endpoints in the documentation
async def root():
    """Base route with welcome message."""

    return {"message": "Welcome to the Energy Data Lab API. Go to /docs for the API documentation."}


def main():
    """Start FastAPI server"""

    parser = ArgumentParser(description="Energy Data Lab API")
    parser.add_argument("-r", "--reload", action="store_true", help="Enables auto-reload")
    parser.add_argument("-p", "--port", type=int, help="Port on which the API will listen", default=8000)
    parser.add_argument("-s", "--share", action="store_true", help="Allow API access from other devices")
    # store true means that argument will be set to True when the flag
    # is given and to False otherwise

    args = parser.parse_args()

    # App must listen on 0.0.0.0, which binds the server to all network interfaces
    # inside the container. If the app is only listening on localhost or 127.0.0.1,
    # it will not be accessible from outside the container.
    uvicorn.run("edl_api:app", host="0.0.0.0" if args.share else "127.0.0.1", reload=args.reload, port=args.port)
