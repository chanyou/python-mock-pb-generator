# python-mock-pb-generator
Mock Protobuf message generator for python projects.

It fills not only the target object, but also the decendents of the object recursively. 

## How to use

```
from mock_pb_gen import make_mock_pb
# assume that ref is an instance of protobuf object
generated = mock_pb_gen.make_mock_pb(ref)

```

Please refer to tests/gen_test.py

