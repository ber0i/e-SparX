"""
This module defines the client responsible for managing the connection to the document database
and executing database operations (create, read, update, delete).
When an instance of the client is created, it establishes a connection to the document database.
"""

import pymongo

from edl_api import settings

DocumentDBClient = pymongo.MongoClient(f"mongodb://{settings.ARTIFACTDB_ENDPOINT}", tz_aware=True)
