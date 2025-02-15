from argparse import ArgumentParser

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from esparx_api.routes import (
    ArtifactRegisterRouter,
    ArtifactRouter,
    ConnectionRouter,
    PipelineRouter,
)

app = FastAPI(
    title="e-SparX API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)


app.include_router(ArtifactRegisterRouter, prefix="/register")
app.include_router(ArtifactRouter, prefix="/artifacts")
app.include_router(PipelineRouter, prefix="/pipelines")
app.include_router(ConnectionRouter, prefix="/connections")


@app.get(
    "/", tags=["Welcome"]
)  # tags are used to group the endpoints in the documentation
async def root():
    """Base route with welcome message."""

    return {
        "message": "Welcome to the e-SparX API. Go to /docs for the API documentation."
    }


def main():
    """Start FastAPI server"""

    parser = ArgumentParser(description="e-SparX API")
    parser.add_argument(
        "-r", "--reload", action="store_true", help="Enables auto-reload"
    )
    parser.add_argument(
        "-p", "--port", type=int, help="Port on which the API will listen", default=8080
    )
    parser.add_argument(
        "-s", "--share", action="store_true", help="Allow API access from other devices"
    )
    parser.add_argument(
        "--root-path",
        type=str,
        help="API root path for example, if it is hosted behind a proxy",
        default="/",
    )
    # store true means that argument will be set to True when the flag
    # is given and to False otherwise

    args = parser.parse_args()

    # App must listen on 0.0.0.0, which binds the server to all network interfaces
    # inside the container. If the app is only listening on localhost or 127.0.0.1,
    # it will not be accessible from outside the container.
    uvicorn.run(
        "esparx_api:app",
        host="0.0.0.0" if args.share else "127.0.0.1",
        reload=args.reload,
        port=args.port,
        root_path=args.root_path,
    )
