import pytest
from unittest.mock import Mock
from src.backend.utils import validate_language_code, format_response, validate_audio_file
from src.backend.exceptions import AudioProcessingException, FileSizeException

def test_validate_language_code():
    assert validate_language_code("en") is True
    assert validate_language_code("invalid") is False

def test_format_response():
    response = format_response(True, {"key": "value"}, "Success")
    assert response["success"] is True
    assert response["data"]["key"] == "value"
    assert response["message"] == "Success"
    assert "timestamp" in response

def test_validate_audio_file_no_filename():
    mock_file = Mock()
    mock_file.filename = None
    
    with pytest.raises(AudioProcessingException):
        validate_audio_file(mock_file, 10, ["wav", "mp3"])

def test_validate_audio_file_invalid_format():
    mock_file = Mock()
    mock_file.filename = "test.txt"
    
    with pytest.raises(AudioProcessingException):
        validate_audio_file(mock_file, 10, ["wav", "mp3"])

def test_validate_audio_file_too_large():
    mock_file = Mock()
    mock_file.filename = "test.wav"
    mock_file.file.seek.return_value = None
    mock_file.file.tell.return_value = 15 * 1024 * 1024  # 15MB
    
    with pytest.raises(FileSizeException):
        validate_audio_file(mock_file, 10, ["wav", "mp3"])