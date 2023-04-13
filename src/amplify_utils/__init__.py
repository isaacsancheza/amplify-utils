from json import loads
from typing import List
from datetime import datetime


def get_context(event: dict) -> dict:
    """
    Returns the user from the event.
    """
    return loads(event['identity']['resolverContext'])


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


def dump_errors(errors: List[dict]) -> List[dict]:
    """
    Dumps the errors into a list of dictionaries with the following structure:
    {
        'field': 'field_name',
        'message': 'error_message'
    }
    """
    dumped_errors = []
    for error in errors:
        if len(error['loc']) > 1:
            for field in error['loc']:
                dumped_errors.append({
                    'field': field,
                    'message': error['msg']
                })
        else:
            dumped_errors.append({
                'field': error['loc'][0],
                'message': error['msg']
            })
    return dumped_errors


def dumps_errors(errors: List[dict]) -> str:
    """
    Dumps the errors into a JSON string
    """
    return dumps(dump_errors(errors))
