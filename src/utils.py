import hashlib

def calculate_hash(file_path, chunk_size=4096):
    """Вычисляет MD5-хэш файла"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()