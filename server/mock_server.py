import os
import json
from flask import Flask, request

app = Flask(__name__)
STORAGE_DIR = "server_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def handle_upload():
    if 'file' not in request.files or 'hash' not in request.form:
        return "Missing data", 400

    file = request.files['file']
    file_hash = request.form['hash']
    file_path = os.path.join(STORAGE_DIR, f"{file_hash}_{file.filename}")
    file.save(file_path)

    metadata = {
        "original_name": file.filename,
        "hash": file_hash,
        "size_bytes": os.path.getsize(file_path)
    }
    with open(f"{file_path}.json", "w") as f:
        json.dump(metadata, f)
    print(f"Saved: {file.filename} with metadata.")
    return "OK", 200

if __name__ == "__main__":
    app.run(port=8000)