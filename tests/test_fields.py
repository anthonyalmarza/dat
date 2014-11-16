from .utils import TestCase
from datetime import datetime
from bson.timestamp import Timestamp
from bson.objectid import ObjectId
from dat.fields import (
    Field, Id, Int, Float, Char, List, Dict, Set, TimeStamp, serializeDatetime,
    serializeList, serializeDict
)
from dat.exceptions import SerializationError
from dat.utils import strftime


class TestFieldBase(TestCase):

    def test_field_subclasses(self):
        "assert that fields listed in fields are in fact subclassed from Field"
        self.assertTrue(issubclass(Int, Field))
        self.assertTrue(issubclass(Float, Field))
        self.assertTrue(issubclass(Char, Field))
        self.assertTrue(issubclass(List, Field))
        self.assertTrue(issubclass(Dict, Field))
        self.assertTrue(issubclass(Set, Field))
        self.assertTrue(issubclass(TimeStamp, Field))
        self.assertTrue(issubclass(Id, Field))

    def test_default(self):
        "test that the default functionality on all fields works as expected"
        value = 2

        def func():
            return 'hello'

        field = Field(default=value)
        self.assertEqual(field.getDefault(), value)

        field = Field(default=func)
        self.assertEqual(field.getDefault(), func())


class TestSerializers(TestCase):

    def setUp(self):
        self.now = datetime.utcnow()
        self.timestamp = Timestamp(self.now, 0)
        self.now_str = strftime(self.now)

    def test_datetime_serializer(self):
        self.assertEqual(serializeDatetime(2), 2)
        self.assertEqual(serializeDatetime(self.now), self.timestamp)
        self.assertEqual(
            serializeDatetime(self.now, to_json=True), self.now_str
        )

    def test_list_serializer(self):
        data = [1, 'asdf', 3, ['asdf', 7, 9.5, self.now, [1, 'lkj']], 2]
        expected = [
            1, 'asdf', 3, ['asdf', 7, 9.5, self.timestamp, [1, 'lkj']], 2
        ]
        expected_js = [
            1, 'asdf', 3, ['asdf', 7, 9.5, self.now_str, [1, 'lkj']], 2
        ]
        self.assertEqual(list(serializeList(data)), expected)
        self.assertEqual(list(serializeList(data, to_json=True)), expected_js)

    def test_dict_serializer(self):
        data = {
            'hi': 1, '2': 6, 'test': {'?': self.now, 'yo': {'mama': self.now}}
        }
        expected = {
            'hi': 1, '2': 6, 'test': {
                '?': self.timestamp, 'yo': {'mama': self.timestamp}
            }
        }
        expected_js = {
            'hi': 1, '2': 6, 'test': {
                '?': self.now_str, 'yo': {'mama': self.now_str}
            }
        }
        self.assertEqual(dict(serializeDict(data)), expected)
        self.assertEqual(dict(serializeDict(data, to_json=True)), expected_js)

    def test_int(self):
        field = Int(default=9)
        self.assertEqual(field.serialize('2'), 2)
        self.assertEqual(field.serialize(3.44), 3)

        self.assertRaises(SerializationError, field.serialize, 'asfaf')
        self.assertRaises(SerializationError, field.serialize, [1, ])
        self.assertRaises(SerializationError, field.serialize, {'1': 2})

    def test_float(self):
        field = Float(default=9.)
        self.assertEqual(field.serialize('2'), 2.)
        self.assertEqual(field.serialize(3.44), 3.44)
        self.assertEqual(field.serialize(3), 3.)

        self.assertRaises(SerializationError, field.serialize, 'asfaf')
        self.assertRaises(SerializationError, field.serialize, [1, ])
        self.assertRaises(SerializationError, field.serialize, {'1': 2})

    def test_char(self):
        field = Char(default='asdf')
        self.assertEqual(field.serialize('2'), u'2')
        self.assertEqual(field.serialize(3.44), u'3.44')
        self.assertEqual(field.serialize('asdf'), u'asdf')

        self.assertEqual(field.serialize([1, ]), unicode([1, ]))
        self.assertEqual(field.serialize({'1': 2}), unicode({'1': 2}))

    def test_id(self):
        field = Id()
        _id = ObjectId()
        self.assertEqual(field.serialize(_id), _id)
        self.assertEqual(field.serialize(_id, to_json=True), str(_id))
        # N.B. _id needs to be 24 characters
        self.assertEqual(
            field.serialize('123456789012345678901234'),
            ObjectId('123456789012345678901234')
        )
        self.assertRaises(SerializationError, field.serialize, 'asdflkj')

    def test_list(self):
        pass

    def test_dict(self):
        pass

    def test_set(self):
        pass

    def test_timestamp(self):
        pass
