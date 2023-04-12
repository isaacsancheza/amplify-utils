import pytest
from soteria import validators, normalizers
from pydantic import BaseModel, ValidationError, validator
from amplify_utils import dump_errors, iso8601_utc_now, parse_iso8601_utc_date


class Example(BaseModel):
    name: str
    phone: str
    username: str

    @validator('name', 'username', pre=True)
    def normalize(cls, v):
        for normalizer in [normalizers.strip_string, normalizers.normalize_whitespaces]:
            v = normalizer(v)
        return v

    @validator('name')
    def validate_name(cls, v):
        if not validators.is_spanish_letters_only(v):
            raise ValueError('Solo letras y espacios.')
        return v

    @validator('username')
    def validate_username(cls, v):
        if not validators.is_username(v):
            raise ValueError('No es un nombre de usuario valido.')
        return v


def test_dump_errors():
    with pytest.raises(ValidationError):
        example = Example(name='  1juan   ', phone='123 456 789', username='j1uan..')
        assert dump_errors(example.errors()) == {'name': ['Solo letras y espacios.'], 'username': ['No es un nombre de usuario valido.']}
        example = Example(name='juan', phone='123 456 789', username='j1uan..')
        assert dump_errors(example.errors()) == {'username': ['No es un nombre de usuario valido.']}
        example = Example(name='juan', phone='123 456 789', username='juan')
        assert dump_errors(example.errors()) == {}
        example = Example(name='juan', phone='123 456 789', username='j1uan')
        assert dump_errors(example.errors()) == {}


def test_iso8601():
    utc_now = iso8601_utc_now()
    assert utc_now == utc_now
    assert parse_iso8601_utc_date(utc_now).isoformat() == utc_now
