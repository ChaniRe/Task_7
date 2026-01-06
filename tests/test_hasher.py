import os
import pytest
from client.hasher import FileHasher
from client.database import DatabaseManager

def test_consistent_hashing(tmp_path):
    hasher = FileHasher()
    
    p = tmp_path / "hello.txt"
    p.write_text("hello world")
    
    hash1 = hasher.get_hash(str(p))
    hash2 = hasher.get_hash(str(p))
    
    assert hash1 == hash2
    assert len(hash1) == 64 

def test_different_content_different_hash(tmp_path):
    hasher = FileHasher()
    
    p1 = tmp_path / "file1.txt"
    p1.write_text("Content A")
    
    p2 = tmp_path / "file2.txt"
    p2.write_text("Content B")
    
    assert hasher.get_hash(str(p1)) != hasher.get_hash(str(p2))