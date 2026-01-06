import requests
import os

class AssetUploader:
    def __init__(self, server_url):
        self.server_url = server_url

    def upload(self, file_path, file_hash):
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (os.path.basename(file_path), f)}
                data = {'hash': file_hash}
                response = requests.post(f"{self.server_url}/upload", files=files, data=data)
                return response.status_code == 200
        except Exception as e:
            print(f"Connection error: {e}")
            return False