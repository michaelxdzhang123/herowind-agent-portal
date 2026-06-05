"""Tests for settings.py."""
from settings import LANGUAGES


def test_languages_dict():
    """验证 LANGUAGES 字典包含预期的语言和名称映射。"""
    assert isinstance(LANGUAGES, dict)
    assert 'en' in LANGUAGES
    assert 'cn' in LANGUAGES
    assert LANGUAGES['en'] == 'English'
    assert LANGUAGES['cn'] == 'Chinese'
