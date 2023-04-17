from json import loads, dumps
from typing import List
from datetime import datetime
from .schema import Schema
from typing import Tuple, List


def get_context(event: dict) -> dict:
    """
    Returns the user from the event.
    """
    return loads(event['identity']['resolverContext']['context'])


def parse_iso8601_utc_date(date_str: str) -> datetime:
    """
    Parses an ISO8601 UTC date string and returns a datetime object
    """
    return datetime.fromisoformat(date_str)


def iso8601_utc_now() -> str:
    """
    Returns the current UTC time in ISO8601 format
    """
    return datetime.utcnow().astimezone().isoformat()


def dump_pydantic_errors(errors: List[dict]) -> List[dict]:
    """
    Dumps the errors into a list of dictionaries with the following structure:
    {
        'field': 'field_name',
        'message': 'error_message'
    }
    """
    assert isinstance(errors, list), 'Errors must be a list.'
    assert errors, 'Errors must not be empty.'
    for error in errors:
        assert 'loc' in error, 'Missing "loc" key.'
        assert 'msg' in error, 'Missing "msg" key.'

    dumped_errors = []
    for error in errors:
        if len(error['loc']) > 1:
            dumped_errors.append({
                'field': error['loc'],
                'message': error['msg'],
            })
        else:
            dumped_errors.append({
                'field': error['loc'][0],
                'message': error['msg']
            })
    return dumped_errors


def dump_errors(error_type: str, errors: List[dict]) -> str:
    """
    Dumps the errors into a JSON string
    """
    error_type = error_type.strip()
    assert error_type, 'Error type must not be empty.'
    assert errors, 'Errors must not be empty.'
    for error in errors:
        assert 'field' in error, 'Missing "field" key.'
        assert 'message' in error, 'Missing "message" key.'
    return {
        'errors': {
            'type': error_type,
            'message': dumps(errors),
        }
    }


def dump_error(error_type: str, error_field: str, error_message: str) -> str:
    error_type = error_type.strip()
    error_field = error_field.strip()
    error_message = error_message.strip()
    
    assert error_type, 'Error type must not be empty.'
    assert error_field, 'Error field must not be empty.'
    assert error_message, 'Error message must not be empty'

    return dump_errors(error_type, [{'field': error_field, 'message': error_message}])


def merge_schemas(*schemas: Tuple[str]) -> List[str]:
    """
    Receive an array of strings representings schema's path then
    merge all theirs possible types, fields, queries, and mutations.
    Usefull to merge denied's fields of role and global denied's fields.
    """
    denied_fields = []
    for schema in [Schema(path) for path in schemas]:
        denied_fields += schema.dump()
    return list(set(denied_fields))
