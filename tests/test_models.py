from datetime import datetime
from .utils import TestCase
from dat.fields import Int, Char, Float, List, TimeStamp, Field

from pymongo import TEXT, collection, database
from dat.models import Model
from dat.db import QuerySet, DATABASE_NAME

from uuid import uuid4


COUNT = 0


class Person(Model):

    collection_name = 'test_collection'

    created = TimeStamp(default=datetime.utcnow)

    age = Int()
    name = Char(index=TEXT)
    parents = List()
    height = Float()
    inc = Int()

    def __init__(self, *args, **kwargs):
        global COUNT
        super(Person, self).__init__(*args, **kwargs)
        if self.inc is None and not self._from_db:
            self.inc = COUNT
            COUNT += 1


class Product(Model):

    unique_together = ('size', 'name')

    name = Char()
    serial = Char(default=uuid4)
    size = Int()


class TestModels(TestCase):

    def setUp(self):
        self.data = {
            'age': 29, 'name': 'Anthony', 'parents': ['the', 'streets'],
            'height': 1.76
        }
        self.expected_fields = self.data.keys() + ['created', '_id', 'inc']

    def tearDown(self):
        Person.collection.remove()

    def test_init(self):
        anthony = Person(**self.data)
        for fieldname, field in anthony.meta.fields.items():
            self.assertTrue(
                fieldname in self.expected_fields,
                '%s is not in the list of fields' % fieldname
            )
            self.assertTrue(issubclass(field.__class__, Field))
        for key, value in self.data.items():
            self.assertEqual(getattr(anthony, key), value)

    def test_collection(self):
        collection_names = Person._db.collection_names()
        if hasattr(Person, 'collection_name'):
            collection_name = Person.collection_name
        else:
            collection_name = 'person'
        self.assertTrue(collection_name in collection_names)
        self.assertTrue('product' in collection_names)
        self.assertIsInstance(Person.collection, collection.Collection)

    def test_db(self):
        self.assertTrue(DATABASE_NAME in Person._client.database_names())
        self.assertIsInstance(Person._db, database.Database)

    def test_save(self):
        anthony = Person(**self.data)
        anthony = anthony.save()
        self.assertTrue(anthony._id is not None)
        self.assertTrue(Person.get({'name': 'Anthony'}) is not None)

    def test_get(self):
        self.assertRaises(Person.DoesNotExist, Person.get, {'name': 'asfasf'})
        anthony1 = Person.create(**self.data)
        Person.create(**self.data)
        self.assertRaises(
            Person.MultipleObjectsExist, Person.get, {'name': 'Anthony'}
        )
        gotten_anthony = Person.get({'_id': anthony1._id})
        self.assertIsInstance(gotten_anthony, Person)

        # Check that the projection works as expected i.e. no projection gives
        # all fields
        self.assertEqual(gotten_anthony._id, anthony1._id)
        self.assertEqual(gotten_anthony.name, anthony1.name)
        self.assertEqual(gotten_anthony.age, anthony1.age)
        self.assertEqual(gotten_anthony.parents, anthony1.parents)
        self.assertEqual(gotten_anthony.height, anthony1.height)
        self.assertEqual(gotten_anthony.inc, anthony1.inc)

        gotten_anthony = Person.get(
            {'_id': anthony1._id}, include=['name', 'parents']
        )
        self.assertEqual(gotten_anthony._id, anthony1._id)
        self.assertEqual(gotten_anthony.name, anthony1.name)
        self.assertEqual(gotten_anthony.age, None)
        self.assertEqual(gotten_anthony.parents, anthony1.parents)
        self.assertEqual(gotten_anthony.height, None)
        self.assertEqual(gotten_anthony.inc, None)

        gotten_anthony = Person.get(
            {'_id': anthony1._id}, exclude=['_id', 'name', 'parents']
        )
        self.assertEqual(gotten_anthony._id, None)
        self.assertEqual(gotten_anthony.name, None)
        self.assertEqual(gotten_anthony.age, anthony1.age)
        self.assertEqual(gotten_anthony.parents, None)
        self.assertEqual(gotten_anthony.height, anthony1.height)
        self.assertEqual(gotten_anthony.inc, anthony1.inc)

        gotten_anthony = Person.get(
            {'_id': anthony1._id, 'parents': 'the'}, {'parents.$': 1}
        )
        self.assertEqual(gotten_anthony.parents, ['the', ])

        gotten_anthony.name = "Tony"
        gotten_anthony.save()
        self.assertEqual(gotten_anthony.name, "Tony")
        self.assertEqual(Person.filter({'name': 'Tony'}).count(), 1)

        young_anthony = Person(**self.data)
        young_anthony.age = 22
        young_anthony.save()
        self.assertTrue(young_anthony._from_db)
        self.assertEqual(
            Person.filter({'name': 'Anthony', 'age': 22}).count(), 1
        )

        self.assertRaises(
            Person.DoesNotExist, Person.get, {'name': 'Alice'}
        )

        Person.create(name='Tony')

        self.assertRaises(
            Person.QueryError, Person.filter(name__asfdf='asfd').__getitem__, 0
        )

        def iterate():
            for i in Person.filter(name__asfdf='asfd'):
                print i

        self.assertRaises(Person.QueryError, iterate)

        self.assertRaises(
            Person.MultipleObjectsExist, Person.get, {'name': 'Tony'}
        )

    def test_filter(self):
        clones = [Person(**self.data) for idx in range(10)]
        Person.bulk_create(clones)
        queryset = Person.filter({'name': 'Anthony'})
        self.assertIsInstance(queryset, QuerySet)

        # check that all of the functionality exists
        self.assertTrue(hasattr(queryset, 'count'))
        self.assertTrue(hasattr(queryset, 'limit'))
        self.assertTrue(hasattr(queryset, 'skip'))
        self.assertTrue(hasattr(queryset, 'sort'))
        self.assertTrue(hasattr(queryset, 'hint'))
        self.assertTrue(hasattr(queryset, 'distinct'))

        self.assertTrue(hasattr(queryset, 'filter'))
        self.assertTrue(hasattr(queryset, 'update'))
        self.assertTrue(hasattr(queryset, 'exists'))
        self.assertTrue(hasattr(queryset, 'serialize'))

        self.assertFalse(Person.filter({'name': 'asdf'}).exists())
        self.assertTrue(queryset.exists())
        self.assertEqual(queryset.count(), 10)

        # test update functionality
        queryset = Person.filter({'name': 'Anthony', 'inc': {'$gt': 4}})
        self.assertEqual(queryset.count(), 5)
        ret = queryset.update({'$set': {'age': 60}})
        ages = [person.age for person in ret]
        age_set = set(ages)
        self.assertEqual(len(age_set), 1)
        self.assertEqual(list(age_set)[0], 60)

        # test daisy chaining filters
        queryset = Person.filter({'name': 'Anthony'}, exclude=['inc', '_id'])
        queryset.filter({'age': {'$gt': 40}})
        self.assertEqual(queryset.count(), 5)

        # test that you can't add a field to the document that isn't in the
        # model schema
        self.assertRaises(ValueError, queryset.update, not_here=1000)

        # test that setting values via a kwarg is possible
        queryset.update(age=100)

        # test serialization of queryset, also tests projection on filter
        # via the exclude
        data = self.data
        data['age'] = 100
        for d in queryset.serialize():
            self.assertItemsEqual(d, data)
            self.assertDictContainsSubset(d, data)
        self.assertTrue(queryset.exists())

        # test count and len after limit
        queryset.limit(2)
        self.assertEqual(queryset.count(), 5)
        self.assertEqual(queryset.count(True), 2)
        self.assertEqual(len(queryset), 2)

        # test distinct
        unique_values = queryset.distinct('name')
        self.assertEqual(len(unique_values), 1)
        self.assertEqual(unique_values, ['Anthony', ])

    def test_field_index(self):
        self.assertTrue(
            'name_text' in Person.collection.index_information()
        )
        self.assertTrue(
            'size_1_name_1' in Product.collection.index_information()
        )
