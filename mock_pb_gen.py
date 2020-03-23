import random
import string
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.pyext._message import RepeatedCompositeContainer, RepeatedScalarContainer
from google.protobuf.timestamp_pb2 import Timestamp

_sym_db = _symbol_database.Default()


def random_str(strlen):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(strlen))


def fill_variable(var):
    prep = {
        str: random_str(random.randint(5, 100)),
        int: random.randint(0, 1000),
        float: random.random() * 1000,
        bool: bool(random.getrandbits(1)),
    }
    return prep[var]


def check_attr(var, attr):
    try:
        _ = getattr(var, attr)
        return True
    except:
        return False


def make_child(child_pb, child_desc):
    res = None
    is_repeated = (type(child_pb) is RepeatedCompositeContainer) or (type(child_pb) is RepeatedScalarContainer)
    # the child is a generic type
    if child_desc.message_type is None:
        if is_repeated:
            res = []
            for _ in range(random.randint(0, 20)):
                if type(child_pb) is RepeatedScalarContainer:
                    res.append(fill_variable(int))
                else:
                    res.append(fill_variable(type(child_pb)))
        else:
            res = fill_variable(type(child_pb))
    else:
        if type(child_pb) is Timestamp:
            res = Timestamp()
            res.GetCurrentTime()
            return res
        pb_elem = _sym_db._classes[child_desc.message_type]
        if is_repeated:
            res = []
            for _ in range(random.randint(0, 20)):
                res.append(make_mock_pb(pb_elem(), target_desc=pb_elem.DESCRIPTOR, target_pb_elem=pb_elem))
        else:
            res = make_mock_pb(child_pb, target_desc=pb_elem.DESCRIPTOR)
    return res


def make_mock_pb(reference_pb, target_desc=None, target_pb_elem=None):
    """
        This function makes a mock protobuf object, i.e, new and filled random protobuf object. 
        It mocks the protobuf object structure of 'reference_pb'
        In case of 'oneof', it randomly selects an object to mock.
    """
    kwargs = {}
    try:
        desc = reference_pb.DESCRIPTOR
    except Exception as e:
        desc = target_desc
    # If there are 'oneof' elements, randomly pick one and generate
    exist_oneofs = check_attr(desc, 'oneofs')
    exist_fields = check_attr(desc, 'fields')
    if exist_oneofs:
        for oneof in desc.oneofs:
            n_oneof = len(oneof.fields)
            child_idx = random.randint(0, n_oneof - 1)  # pick one of the 'oneof' elements
            selected_child = oneof.fields[child_idx]
            child_pb = getattr(reference_pb, selected_child.name)
            kwargs[selected_child.name] = make_child(child_pb, selected_child)

    if exist_fields:
        for child in desc.fields:
            if child.containing_oneof is not None:
                continue
            child_pb = getattr(reference_pb, child.name)
            kwargs[child.name] = make_child(child_pb, child)
    if target_pb_elem is not None:
        return target_pb_elem(**kwargs)
    else:
        return reference_pb.__class__(**kwargs)
