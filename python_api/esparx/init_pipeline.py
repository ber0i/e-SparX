from pathlib import Path
import urllib.parse
from argparse import ArgumentParser
from math import ceil

import requests
import mimetypes

from ._client import client
from . import _logging as log

mimetypes.init()


def init_pipeline(
    name: str,
    path: Path | str,
    skip_missing: bool = True,
    ignored_file_types: list[str] = ["text/html"],
):
    """
    Download all artifacts of a pipeline into a directory

    Parameters
    ----------
    name : str
        The name of the pipeline
    path : Path | str
        The path to the directory in which the pipeline will be downloaded
    skip_missing : bool = True
        Whether to skip atifacts with missing download URL or raise an exception
    ignored_file_types : list[str] = ['text/html']
        List of MIME types which are not downloaded
    """

    # check if a pathlib.Path or a string was passed
    if not (isinstance(path, Path) or isinstance(path, str)):
        raise TypeError("path must be a pathlib.Path or a string")
    
    # convert path to a Path object if it is a string
    if isinstance(path, str):
        path = Path(path)

    validate_path(path)

    artifacts = get_artifacts(name)

    for artifact in artifacts:
        download_url = get_download_url(artifact["name"])

        if not download_url:
            if skip_missing:
                log.warning(f"Artifact '{artifact['name']}' is missing a download URL!")
                continue

            raise ValueError(
                f"Oh no! The artifact '{artifact['name']}' is missing a download URL!"
            )

        download_artifact(path, artifact["name"], download_url, ignored_file_types)


def init_pipeline_cli():
    """Function for running pipeline init from the command line"""

    parser = ArgumentParser()

    parser.add_argument("pipeline", type=str)
    parser.add_argument("path", type=str, nargs="?")
    parser.add_argument(
        "-i",
        "--ignore-files",
        help="List of MIME types which will be ignored during download.",
        nargs="*",
        default=["text/html"],
    )
    parser.add_argument(
        "-e",
        "--exit-missing",
        help="Exit if a download URL is missing",
        action="store_true",
    )

    args = parser.parse_args()

    path = Path() / args.pipeline
    if args.path:
        path = Path(args.path)

    init_pipeline(args.pipeline, path, not args.exit_missing, args.ignore_files)


def validate_path(path: Path):
    """Validate path and create directory if it doesn't exist"""

    if not path.exists():
        path.mkdir()
        return

    if not path.is_dir():
        raise NotADirectoryError(
            "Whoops! Make sure you're pointing to a directory for the pipeline initialization!"
        )
    if any(path.iterdir()):
        raise ValueError(
            f"Whoops! '{path}' is not empty. Make sure you're pointing to an empty directory"
        )


def get_artifacts(pipeline_name: str) -> list[dict]:
    """Get all artifacts in a given pipeline"""

    res = client.get(urllib.parse.quote(f"/artifacts/pipeline/{pipeline_name}"))
    body = res.json()

    if res.status_code != 200:
        raise Exception(body["detail"])

    return body


def get_download_url(artifact_name: str) -> str:
    """Fetch the download URL of a given artifact"""

    # safe="" is used to prevent encoding of special characters in the URL,
    # as slashes or spaces
    encoded_artifact_name = urllib.parse.quote(artifact_name, safe="")
    
    res = client.get(f"/artifacts/name/{encoded_artifact_name}")
    body = res.json()

    if res.status_code != 200:
        raise Exception(body["detail"])

    return body.get("download_url", None)


def download_artifact(
    pipeline_path: Path,
    artifact_name: str,
    download_url: str,
    ignored_file_types: list[str],
):
    """Download Artifact to the pipeline path"""

    head = requests.head(download_url)
    headers = head.headers
    file_type = headers["Content-Type"].partition(";")[0].strip()

    if file_type in ignored_file_types:
        log.warning(
            f"Artifact '{artifact_name}' download skipped because of invalid file type '{file_type}'!"
        )
        return

    file_ext = mimetypes.guess_extension(file_type)
    res = requests.get(download_url, stream=True)

    total_len = int(res.headers.get("Content-Length", 0))
    chunk_size = 1024 * 1024  # Download Chunk Size (1 megabyte)

    log.info(f"Downloading Artifact '{artifact_name}'")

    with open(pipeline_path / f"{artifact_name}{file_ext}", mode="wb") as f:
        it = (
            log.progress(
                res.iter_content(chunk_size=chunk_size),
                steps=ceil(total_len / chunk_size),
                unit="MB"
            )
            if (total_len >= 10 * chunk_size)
            else res.iter_content(chunk_size=chunk_size)
        )
        for chunk in it:
            f.write(chunk)
