import pytest
import amplify_utils
from json import loads, dumps
from soteria import validators, normalizers
from pydantic import BaseModel, ValidationError, validator


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
        assert amplify_utils.dump_errors(example.errors()) == {'name': ['Solo letras y espacios.'], 'username': ['No es un nombre de usuario valido.']}
        example = Example(name='juan', phone='123 456 789', username='j1uan..')
        assert amplify_utils.dump_errors(example.errors()) == {'username': ['No es un nombre de usuario valido.']}
        example = Example(name='juan', phone='123 456 789', username='juan')
        assert amplify_utils.dump_errors(example.errors()) == {}
        example = Example(name='juan', phone='123 456 789', username='j1uan')
        assert amplify_utils.dump_errors(example.errors()) == {}


def test_iso8601():
    utc_now = amplify_utils.iso8601_utc_now()
    assert utc_now == utc_now
    assert amplify_utils.parse_iso8601_utc_date(utc_now).isoformat() == utc_now


def test_get_context():
    event = {
        'identity': {
            'resolverContext': dumps({'id': 'user-id'})
            }
        }
    assert amplify_utils.get_context(event) == {'id': 'user-id'}
