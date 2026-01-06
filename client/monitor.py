import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DirectoryMonitor(FileSystemEventHandler):
    #Watches a directory for changes and orchestrates the upload logic
    def __init__(self, watch_path, db, hasher, uploader):
        self.watch_path = watch_path
        self.db = db
        self.hasher = hasher
        self.uploader = uploader

    def process_file(self, file_path):
        #Core logic: Hash -> Check DB -> Upload -> Update DB
        if not os.path.isfile(file_path): return
        file_hash = self.hasher.get_hash(file_path)
        if not self.db.is_already_uploaded(file_hash):
            if self.uploader.upload(file_path, file_hash):
                self.db.mark_as_uploaded(file_hash, file_path)
                print(f"Uploaded: {os.path.basename(file_path)}")
        else:
            print(f"Skipping (Already exists): {os.path.basename(file_path)}")

    def on_created(self, event):
        #Triggered when a new file is added to the watched directory
        if not event.is_directory: self.process_file(event.src_path)

    def scan_existing_files(self):
        #Recovers state by scanning the directory for files added while client was offline.
        for root, _, files in os.walk(self.watch_path):
            for file in files:
                self.process_file(os.path.join(root, file))