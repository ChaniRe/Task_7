import json
import os

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/asset_catalog")
        self.config_path = os.path.join(self.config_dir, "config.json")
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_dir, exist_ok=True)
            default_config = {"server_url": "http://localhost:8000"}
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f)

    def get_server_url(self):
        with open(self.config_path, 'r') as f:
            return json.load(f).get("server_url", "http://localhost:8000")