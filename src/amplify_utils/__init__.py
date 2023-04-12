from typing import List


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

