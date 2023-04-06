from amplify_utils import serialize


def test_serializer():
    data = {
        "foo": "bar",
        "baz": "qux",
    }
    serialized = serialize(data)
    assert serialized == {'baz': {'S': 'qux'}, 'foo': {'S': 'bar'}}
