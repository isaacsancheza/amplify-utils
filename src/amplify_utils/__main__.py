from json import dump
from yaml import safe_load
from argparse import FileType
from argparse import ArgumentParser


def convert_schema(source: str, dest: str) -> None:
    """
    Convert a xml file to json.
    """
    yaml_schema = safe_load(source)

    schema = []
    for key in yaml_schema:
        mini_schema = {
            'type': key,
            'fields': yaml_schema[key],
        }
        schema.append(mini_schema)
    
    with open(dest, 'w') as f:
        dump(schema, f, indent=4)


def diff_schema(a: str, b: str) -> None:
    """
    Compares a given schema agains another one. b_schema should be the main schema.
    """ 
    a_schema = safe_load(a)
    b_schema = safe_load(b)
    
    a_types = [key for key in a_schema if key not in ('Query', 'Mutation')]
    a_queries = a_schema.get('Query', [])
    a_mutations = a_schema.get('Mutation', [])

    a_fields = []
    for key in a_schema:
        if key in ('Query', 'Mutation',):
            continue
        a_fields += a_schema[key]

    b_types = [key for key in b_schema if key not in ('Query', 'Mutation',)]
    b_queries = b_schema.get('Query', [])
    b_mutations = b_schema.get('Mutation', [])

    b_fields = []
    for key in b_schema:
        if key in ('Query', 'Mutation',):
            continue
        b_fields += b_schema[key]
    pairs = (
        ('Types', [t for t in a_types if t not in b_types]),
        ('Fields', [f for f in a_fields if f not in b_fields]),
        ('Queries', [q for q in a_queries if q not in b_queries]),
        ('Mutations', [m for m in a_mutations if m not in b_mutations]),
    )
    for k, v in pairs:
        if not v:
            print('%s: None' % k)
            continue
        print(k)
        for vv in v:
            print('    -%s' % vv)


if __name__ == '__main__':
    parser = ArgumentParser('amplify-utils')
    subparser = parser.add_subparsers(dest='command')
    
    convert_parser = subparser.add_parser('convert')
    convert_parser.add_argument('schema', type=FileType('r', encoding='UTF-8'))
    convert_parser.add_argument('output')

    diff_parser = subparser.add_parser('diff')
    diff_parser.add_argument('a', type=FileType('r', encoding='UTF-8'))
    diff_parser.add_argument('b', type=FileType('r', encoding='UTF-8'))
    
    args = parser.parse_args()
    if args.command == 'convert':
        convert_schema(args.schema, args.output)
    elif args.command == 'diff':
        diff_schema(args.a, args.b)
    else:
        parser.print_help()
