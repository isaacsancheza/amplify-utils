from json import loads
from typing import List, Optional


class Schema:
    def __init__(self, path: Optional[str] = None):
        path = path if path else '/opt/schema.json'
        with open(path) as f:
            self._schema = loads(f.read())

    @property
    def types(self) -> List[str]:
        return [s['type'] for s in self._schema if s['type'] not in ('Query', 'Mutation',)]

    @property
    def fields(self) -> List[str]:
        fields = []
        for entry in [s for s in self._schema if s['type'] not in ('Query', 'Mutation',)]:
            for f in entry['fields']:
                field = '%s.%s' % (entry['type'], f)
                fields.append(field)
        return fields

    @property
    def queries(self) -> List[str]:
        return self.__lookup('Query')
    
    @property
    def mutations(self) -> List[str]:
        return self.__lookup('Mutation')
    
    def __lookup(self, field: str) -> List[str]:
        return list(set([s for s in self._schema if s['type'] == field][0]['fields']))

    def denied_fields(self, allowed_fields: List[str]) -> List[str]:
        return self.__denied('fields', allowed_fields)

    def denied_types(self, allowed_types: List[str]) -> List[str]:
        return self.__denied('types', allowed_types)

    def denied_queries(self, allowed_queries: List[str]) -> List[str]:
        return self.__denied('queries', allowed_queries)

    def denied_mutations(self, allowed_mutations: List[str]) -> List[str]:
        return self.__denied('mutations', allowed_mutations)

    def __denied(self, attr: str, allowed: List[str]) -> List[str]:
        # remove duplicated fields
        allowed = list(set(allowed))

        prop = getattr(self, attr)
        unknown_fields = [f for f in allowed if f not in prop]
        unknown_fields_string = ', '.join(unknown_fields)

        # validate fields are real. 
        assert not unknown_fields, 'The following "%s" are not valid: %s' % (attr, unknown_fields_string)
        return [field for field in prop  if field not in allowed]

    def build_denied_queries(self, queries: List[str]) -> List[str]:
        return self.__build_denied('Query', queries)

    def build_denied_mutations(self, mutations: List[str]) -> List[str]:
        return self.__build_denied('Mutation', mutations)

    def __build_denied(self, dtype: str, denied: List[str]) -> List[str]:
        return ['%s.%s' % (dtype, d) for d in denied]

    def dump(self) -> List[str]:
        return self.types + self.fields + self.build_denied_queries(self.queries) + self.build_denied_mutations(self.mutations)
