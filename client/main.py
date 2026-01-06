import sys
import time
from client.database import DatabaseManager
from client.hasher import FileHasher
from client.uploader import AssetUploader
from client.monitor import DirectoryMonitor, Observer
from client.config_manager import ConfigManager

def main():
    if len(sys.argv) < 2:
        print("Usage: python client/main.py <directory_to_watch>")
        return

    watch_path = sys.argv[1]
    config = ConfigManager()
    db = DatabaseManager()
    hasher = FileHasher()
    uploader = AssetUploader(config.get_server_url())
    monitor = DirectoryMonitor(watch_path, db, hasher, uploader)
    monitor.scan_existing_files()
    observer = Observer()
    observer.schedule(monitor, watch_path, recursive=False)
    observer.start()

    print(f"Monitoring: {watch_path}")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()