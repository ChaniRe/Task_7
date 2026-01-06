import hashlib

class FileHasher:
    #Responsible for generating a unique 'fingerprint' for a file based on its content
    def get_hash(self, file_path):
        #Calculates the SHA-256 hash of a file
        #Reads the file in chunks to be memory-efficient for large assets
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error hashing file: {e}")
            return None