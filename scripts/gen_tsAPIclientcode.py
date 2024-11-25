#!/usr/bin/env python

"""
This script generates the OpenAPI JSON from a FastAPI application, generates TypeScript
API client code, and updates the TypeScript API client to dynamically set the BASE URL.
It is intended to be used as part of the build or development process for projects
utilizing FastAPI with a TypeScript frontend.
"""

import argparse
import json
import subprocess
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from esparx_api import app

ROOT_DIRECTORY = Path(__file__).parent.parent
FRONTEND_PATHS = {
    "base": ROOT_DIRECTORY / "frontend",
    "api_dir": ROOT_DIRECTORY / "frontend" / "src" / "lib",
    "openapi_json": ROOT_DIRECTORY / "frontend" / "src" / "lib" / "openapi.json",
    "openapi_ts": ROOT_DIRECTORY
    / "frontend"
    / "src"
    / "lib"
    / "api"
    / "core"
    / "OpenAPI.ts",
}


def generate_openapi_json(verbose: bool = False):
    """Create openapi.json for api documentation"""

    openapi_schema = get_openapi(
        title="e-SparX API",
        version="0.0.1",
        routes=app.routes,
    )

    if verbose:
        print(json.dumps(openapi_schema, indent=2))

    # Ensuring the directory exists
    FRONTEND_PATHS["api_dir"].mkdir(parents=True, exist_ok=True)

    # Writing the OpenAPI schema to a file
    with FRONTEND_PATHS["openapi_json"].open("w") as file:
        json.dump(openapi_schema, file, indent=2)

    if verbose:
        print(f"OpenAPI JSON has been generated at: {FRONTEND_PATHS['openapi_json']}")


def generate_typescript_code(verbose: bool = False):
    """Generates TypeScript code from the OpenAPI specification."""

    # This is the command to run openapi-typescript-codegen
    # command = "npx openapi-typescript-codegen --input ./src/lib/openapi.json --output ./src/lib/api"

    command = (
        f"npx @hey-api/openapi-ts --input {FRONTEND_PATHS['openapi_json']} "
        f"--output {FRONTEND_PATHS['api_dir'] / 'api'}"
    )

    # Running the command in the frontend directory
    process = subprocess.run(
        command, shell=True, check=True, cwd=FRONTEND_PATHS["base"]
    )

    # Checking whether the command was successful
    if process.returncode == 0:
        if verbose:
            print("Successfully generated TypeScript code from OpenAPI spec.")
    else:
        print("Error occurred while generating TypeScript code.")


def delete_openapi_json(verbose: bool = False):
    """Deletes the OpenAPI.json file."""
    try:
        FRONTEND_PATHS["openapi_json"].unlink()
        if verbose:
            print("OpenAPI.json file has been deleted.")
    except FileNotFoundError:
        if verbose:
            print("OpenAPI.json file does not exist, no need to delete.")


def main():
    parser = argparse.ArgumentParser(
        description=(
            "This script generates the OpenAPI JSON from a FastAPI application and updates "
            "the TypeScript API client to dynamically set the BASE URL. It is intended to "
            "be used as part of the build or development process for projects utilizing "
            "FastAPI with a TypeScript frontend."
        )
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output for more detailed information about the script's operations.",
    )
    args = parser.parse_args()

    generate_openapi_json(verbose=args.verbose)
    generate_typescript_code(verbose=args.verbose)
    delete_openapi_json(verbose=args.verbose)


if __name__ == "__main__":
    main()
