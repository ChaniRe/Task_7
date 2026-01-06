import os
import pytest
from client.database import DatabaseManager
from client.database import DatabaseManager

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_state.db"
    return DatabaseManager(db_path=str(db_file))

def test_mark_and_check_upload(temp_db):
    test_hash = "fake_hash_123"
    test_path = "/path/to/file.jpg"
    
    assert temp_db.is_already_uploaded(test_hash) is False
    
    temp_db.mark_as_uploaded(test_hash, test_path)
    
    assert temp_db.is_already_uploaded(test_hash) is True

def test_persistence(tmp_path):
    db_file = str(tmp_path / "persistent.db")
    
    db1 = DatabaseManager(db_path=db_file)
    db1.mark_as_uploaded("hash_a", "path/a")
    
    db2 = DatabaseManager(db_path=db_file)
    assert db2.is_already_uploaded("hash_a") is True