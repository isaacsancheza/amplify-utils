from . import dump_error
from os import environ
from typing import Optional, Any
from functools import wraps
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext


def get_logger(level: Optional[str] = None, **kwargs: Any) -> Logger:
    level = level if level else 'DEBUG' if environ['ENV'] != 'prod' else 'INFO'
    return Logger(level=level, **kwargs)


def safe_handler(logger: Logger, **kwargs):  # type: ignore
    def decorator(func): # type: ignore
        @logger.inject_lambda_context(correlation_id_path=correlation_paths.APPSYNC_RESOLVER, **kwargs) 
        @wraps(func)
        def wrapper(event: dict, context: LambdaContext):  # type: ignore
            try:
                return func(event, context) # def lambda_handler(event, context):
            except Exception as e:
                logger.exception(e, exc_info=True)
                return dump_error('SERVER_ERROR', 'NONE', '%s' % context.aws_request_id)
        return wrapper
    return decorator
