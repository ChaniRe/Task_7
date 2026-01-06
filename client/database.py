import sqlite3
import os

class DatabaseManager:
    #Manages local state to ensure no file is uploaded more than once
    def __init__(self, db_path=None):
        #Initializes the database connection. Uses Linux conventions for default storage.
        if db_path is None:
            base_dir = os.path.expanduser("~/.local/share/asset_catalog")
            os.makedirs(base_dir, exist_ok=True)
            self.db_path = os.path.join(base_dir, "state.db")
        else:
            self.db_path = os.path.expanduser(db_path)
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        #Creates the tracking table if it doesn't exist.
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS uploads (file_hash TEXT PRIMARY KEY, path TEXT)")

    def is_already_uploaded(self, file_hash):
        #Checks if the given hash exists in the local database.
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM uploads WHERE file_hash = ?", (file_hash,))
            return cursor.fetchone() is not None

    def mark_as_uploaded(self, file_hash, file_path):
        #Records a successful upload in the database.
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR REPLACE INTO uploads VALUES (?, ?)", (file_hash, file_path))