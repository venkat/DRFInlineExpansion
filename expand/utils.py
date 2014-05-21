from expand.exceptions import ImproperExpandException

def split_expands(expand):
    """
        Convert ['a', 'a.b', 'a.d', 'c'] in the expand attribute
        into first_level_expands - ['a', 'c'] and
        next_level_expands {'a': ['b', 'd']}
    """

    first_level_expands = []
    next_level_expands = {}

    if not isinstance(expand, list):
        expand = [a.strip() for a in expand.split(',') if a.strip()]
    for e in expand:
        if '.' in e:
            first_level, next_level = e.split('.', 1)
            first_level_expands.append(first_level)
            next_level_expands.setdefault(first_level, []).append(next_level)
        else:
            first_level_expands.append(e)
    first_level_expands = list(set(first_level_expands))
    return first_level_expands, next_level_expands


def initialize_explandable_serializer(obj, cls, *args, **kwargs):
    """
        Dynamically initialize the fields of a serializer
        based on the expandable field names in obj.expand
        and the serializers specified for those names in
        expandable_fields
    """

    #don't pass the expand args up to the superclass
    obj.expand = kwargs.pop('expand', obj.expand if hasattr(obj, 'expand') else '')

    print cls, obj
    # instantiate the superclass normally
    super(cls, obj).__init__(*args, **kwargs)

    if obj.expand and not obj.expandable_fields:
        raise ImproperExpandException

    obj.first_level_expands, obj.next_level_expands = split_expands(obj.expand)

    for field in obj.first_level_expands:
        if field not in obj.expandable_fields:
            raise ImproperExpandException
        serializer, args, kwargs = obj.expandable_fields[field]
        if field in obj.next_level_expands:
            kwargs = dict(kwargs, **{'expand': obj.next_level_expands[field]})
        obj.fields[field] = serializer(*args, **kwargs)
