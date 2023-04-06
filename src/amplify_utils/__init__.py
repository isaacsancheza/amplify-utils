from json import loads, dumps
from decimal import Decimal
from boto3.dynamodb.types import TypeSerializer


serializer = TypeSerializer()


def serialize(dictionary: dict):
    """
    Serializes Python data types to DynamoDB types. 
    TypeSerializer does not accept float. So, we convert float do Decimal
    using serializing the direcctionary and descerializing it again.
    """
    return {
        k: serializer.serialize(v) for k, v in loads(dumps(dictionary), parse_float=Decimal).items()
    }
