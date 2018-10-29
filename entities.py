expressions = {
    'equal': lambda a, b: a == b,
    'contains': lambda a, b: b in a,
    'not_contains': lambda a, b: b not in a,
    'more': lambda a, b: a > b,
    'less': lambda a, b: a < b,
    'in': lambda a, b: a in b,
    'not_in': lambda a, b: a not in b
}


class ObjectMeta(type):
    classes = {}

    def __new__(cls, name, bases, attrs):
        api_name = attrs['api_name']
        c = super(ObjectMeta, cls).__new__(cls, name, bases, attrs)

        if api_name is not None:
            cls.classes[api_name] = c

        return c


def get_object_class(name: str):
    """Return class of api 'object' entity by its name"""
    return ObjectMeta.classes[name]


class ObjectBase(metaclass=ObjectMeta):
    api_name = None
    data = None
    allowed_expressions = {}

    def __init__(self, data):
        self.data = data

    def check(self, prop: str, expression: str, value) -> bool:
        if expression not in self.allowed_expressions.get(prop, ()):
            raise ValueError('Property-expression combination is not allowed')

        f = expressions[expression]
        return f(getattr(self, prop), value)


class TextObject(ObjectBase):
    api_name = 'text'
    allowed_expressions = {
        'content': {'contains', 'not_contains'},
        'length': {'more', 'less', 'equal'}
    }

    @property
    def length(self):
        return len(self.data)

    @property
    def content(self):
        return self.data


class CategoryObject(ObjectBase):
    api_name = 'category'
    allowed_expressions = {
        'title': {'equal', 'in', 'not_in'}
    }

    @property
    def title(self):
        return "Новости"  # Hardcoded, as proposed
