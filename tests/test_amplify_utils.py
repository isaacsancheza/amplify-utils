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


def test_dump_pydantic_errors():
    try:
        example = Example(name='  1juan   ', phone='123 456 789', username='j1uan..')
    except ValidationError as e:
        assert amplify_utils.dump_pydantic_errors(e.errors()) == [
            {
                'field': 'name',
                'message': 'Solo letras y espacios.',
            },
            {
                'field': 'username',
                'message': 'No es un nombre de usuario valido.',
            }
        ]
    with pytest.raises(AssertionError):
        amplify_utils.dump_pydantic_errors([])

    with pytest.raises(AssertionError):
        amplify_utils.dump_pydantic_errors([{'field': 'kappa', 'mes': ''}])


def test_dump_errors():
    try:
        example = Example(name='  1juan   ', phone='123 456 789', username='j1uan..')
    except ValidationError as e:
        assert amplify_utils.dump_errors('VALIDATION', amplify_utils.dump_pydantic_errors(e.errors())) == {
            'errors': {
                'type': 'VALIDATION',
                'message': dumps([
                    {
                        'field': 'name',
                        'message': 'Solo letras y espacios.',
                    },
                    {
                        'field': 'username',
                        'message': 'No es un nombre de usuario valido.',
                    }
                ]),
            },
        }

        with pytest.raises(AssertionError):
            assert amplify_utils.dump_errors('', '')
            assert amplify_utils.dump_errors(' ', ['hello'])
            assert amplify_utils.dump_errors(' ', [])
            assert amplify_utils.dump_errors(' ', [{'field': 'name', 'message': 'kappa'}])
            assert amplify_utils.dump_errors('VALIDATION', [{'field': 'name', 'msg': 'kappa'}])


def test_dump_error():
    assert amplify_utils.dump_error('type', 'field', 'message') == {
        'errors': {
            'type': 'type',
            'message': dumps([{'field': 'field', 'message': 'message'}])
        }
    }

    with pytest.raises(AssertionError):
        amplify_utils.dump_error('', 'field', 'message')


def test_iso8601():
    utc_now = amplify_utils.iso8601_utc_now()
    assert utc_now == utc_now
    assert amplify_utils.parse_iso8601_utc_date(utc_now).isoformat() == utc_now


def test_get_context():
    event = {
        'identity': {
            'resolverContext': {'context': dumps({'id': 'user-id'})}
            }
        }
    assert amplify_utils.get_context(event) == {'id': 'user-id'}
