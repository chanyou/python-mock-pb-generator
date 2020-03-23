import unittest
from tests.resource import test_pb2
import mock_pb_gen
from google.protobuf import symbol_database as _symbol_database


_sym_db = _symbol_database.Default()


def is_filled(target_pb):
    """
        Check whether the protobuf object is properly filled or not. 
        - i.e., whether each variable has its own value (i.e, the value has set)
        - 'repeated' variables are exception. This function will return true even if the 'repeated' has no element.
    """
    try:
        desc = target_pb.DESCRIPTOR
    except Exception as e:
        return True
    if target_pb.ByteSize() == 0:  # Detect a not-filled field
        return False

    for oneof in desc.oneofs:
        res = False
        for child in oneof.fields:
            res = res or is_filled(getattr(target_pb, child.name))
        if not res:
            return False

    for child in desc.fields:
        if child.containing_oneof is not None:
            continue
        if child.message_type is not None:
            re = _sym_db._classes[child.message_type]
            if not is_filled(getattr(target_pb, child.name)):
                return False
    return True


class MockPBGenTest(unittest.TestCase):
    def test(self):
        ref = test_pb2.Test()
        generated = mock_pb_gen.make_mock_pb(ref)
        self.assertTrue(is_filled(generated))

if __name__ == '__main__':
    unittest.main()
