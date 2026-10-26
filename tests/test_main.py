import pytest
from src.config import parse_args, validate_config


def test_valid_args():
    args = parse_args(["-p", "requests", "-r", "test_repo.txt", "-m", "file", "-v", "2.31.0"])
    assert args.package == "requests"
    assert args.mode == "file"


def test_bad_version():
    args = parse_args(["-p", "req", "-r", "http://test.com", "-m", "url", "-v", "abc"])
    with pytest.raises(ValueError, match="Неверный формат версии"):
        validate_config(args)


def test_bad_output_ext():
    args = parse_args(["-p", "req", "-r", "http://test.com", "-m", "url", "-v", "1.0", "-o", "graph.jpg"])
    with pytest.raises(ValueError, match="должен иметь расширение .png"):
        validate_config(args)