# Overview

There are three basic components to the dat API.

- [Fields](api.md#fields)
- [Models](api.md#models)
- [QuerySets](api.md#queryset)


## <a name="fields"></a>Fields

At present there are 8 field types:

- `Int` => type: *int*
- `Float` => type: *float*
- `Char` => type: *unicode*
- `Id` => type: *bson.objectid.ObjectId*
- `Dict` => type: *dict*
- `List` => type: *list*
- `Set` => type: *set*
- `TimeStamp` => type: *datetime.datetime*

Each of the above field classes is used to define the model schema via
instantiation to an attribute of the [Model](api.md#models) at class definition.
What this means is that you can subclass the `dat.models.Model` class and
instantiate one of the above fields to an attribute on the model. e.g.

```python
import pymongo
from datetime import datetime
from dat.models import Model
from dat.fields import Int, TimeStamp, Char, Dict


class ExampleModel(Model):

    name = Char()
    total = Int(index=pymongo.DESCENDING, default=0)
    created = TimeStamp(default=detetime.utcnow)
    subdoc_info = Dict()
```

The following is a list of key word arguments that can be set on the fields.

##### Index - *Field Keyword Argument*
Specifies a field level index on the model. Indexing is executed upon definition
of the class via the use of a MetaModel. Accepts: `ASCENDING, DESCENDING, GEO2D, TEXT `
from `pymongo` as values.
For more information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).


---

##### Default - *Field Keyword Argument*
Accepts either a callable or a value. This value is used to populate the field
if no value for the field is given upon instantiation of the model class.

---

##### Unique - *Field Keyword Argument*
Boolean. If `True` then the field is indexed to force uniqueness of values in
that field across all documents within the model's collection. If no value is
given for the `index` kwarg then `pymongo.ASCENDING` is used. For more
information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).

```python
class ExampleModel(Model):
    ...
    name = Char(index=ASCENDING, unique=True)
    ...
```

---

##### Sparse - *Field Keyword Argument*
Boolean (default: False). If True, omit from the index any documents that lack the indexed field.
For more information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).

```python
class ExampleModel(Model):
    ...
    total = Int(index=ASCENDING, sparse=True)
    ...
```

---

##### Background - *Field Keyword Argument*
Boolean (default: True). If True this index should be created in the background. For more
information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).

```python
class ExampleModel(Model):
    ...
    total = Int(index=ASCENDING, background=False)
    ...
```

---

##### Geo Min - *Field Keyword Argument*
Integer. Minimum value for keys in a GEO2D index
For more information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).

---

##### Geo Max - *Field Keyword Argument*
Integer. Maximum value for keys in a GEO2D index
For more information about unique indexing please refer to the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.create_index).

---

##### Storage Considerations
By default none of the fields are required to be set upon instantiation of the
model class. This is because fields with a value of `None` are not saved on
the document. The reason for this is that it reduces document size and it is
possible to check for the non-existence of these fields via
`{'<field_name>': {'$exists': False}}` in the conditions portion of a query.

---



## <a name="models"></a>Models

##### Collection Name - *Class Attribute*

This is a option string that can be used to give the model's collection a
custom name. By default the model's class name (all lower case) is used for
the collection name.

---

##### Collection - *Class Property*

Returns a pymongo.collection.Collection instance associated to the definition
of the `Model` subclass.
This effectively exposes pymongo's API for the collection.

---

##### Save - *Instance Method*

`model.save()`

Returns a Model instance.

```python
from pymongo import TEXT
from datetime import datetime
from dat.models import Model
from dat.fields import Int, Float, Char, List, TimeStamp

class Person(Model):

    collection_name = 'my_custom_collection_name'

    created = TimeStamp(default=datetime.utcnow)
    age = Int()
    name = Char(index=TEXT)
    parents = List()
    height = Float()

bob = Person(name='Bob', age=40, height=1.67)
bob.save()
```

---

##### Create - *Class Method*

`Model.create(**kwargs)`

Returns a Model instance. This is a convenience method that inserts the
document into the collection without hitting the save function.

```python
# imports ...

class Person(Model):
    ...

bob = Person.create(name='Bob', age=40, height=1.67)
```

---

##### Update - *Instance Method*

`model.update(**kwargs)`

Returns the updated Model instance. This is a convenience method that allows
the user to update the instance and save those changes to the collection.

```python
# imports ...

class Person(Model):
    ...

bob = Person.create(name='Bob', age=40, height=1.67)

# DO SOME OTHER STUFF

bob.update(parents=['Mary', 'John'])

print bob.parents
    => ['Mary', 'John']
```

---

##### Bulk Create - *Class Method*

`Model.bulk_create(list_of_models)`

Returns the count of model instances saved to the collection.

```python
# imports ...

class Person(Model):
    ...

person1 = Person(...)
person2 = Person(...)
person3 = Person(...)

# No RTT to MongoDB yet

count = Person.bulk_create([person1, person2, person3])
print count
    => 3
```

---

##### Unique Together - *Class Attribute*

Defines fields that should be unique together on a document within the
collection. e.g.

```python
import pymongo
from dat.models import Model

class SomeModel(Model):

    unique_together = ('some_field_name', 'another_field_name')
    ...

# OR you can specify the type of index you would like to use as well

class SomeOtherModel(Model):

    unique_together = [
        ('some_field_name', pymongo.ASCENDING),
        ('another_field_name', pymongo.TEXT)
    ]
    ...
```

---

##### Compound Index - *Class Attribute*

Defines fields that should be indexed together to better represent the document
in a B-Tree search. e.g.

```python
import pymongo
from dat.models import Model

class SomeModel(Model):

    compound_index = ('some_field_name', 'another_field_name')
    ...

# OR you can specify the type of index you would like to use as well

class SomeOtherModel(Model):

    compound_index = [
        ('some_field_name', pymongo.ASCENDING),
        ('another_field_name', pymongo.TEXT)
    ]
    ...
```

---

##### Get - *Class Method*
`Model.get(conditions=None, projection=None, include=None, exclude=None, limit=None)`

Returns a Model instance.

Raises Model.DoesNotExist if a document could not be found.
Raises Model.MultipleObjectsExist if more than one document is found.

```python
# imports
...

class Person(Model):
    # define the fields
    ...

bob = Person.get({'name': 'Bob'})

# if you don't want the _id for some reason then...
bob = Person.get({'name': 'Bob'}, exclude=['_id', ])  # _id exclusion must be explicit
```

---

##### Filter - *Class Method*
`Model.filter(conditions=None, projection=None, include=None, exclude=None, limit=None)`

Returns a [QuerySet](api.md#queryset).

The filter method allows the user to fetch multiple documents at a time via the
lazy definition of conditions and projections. By returning a QuerySet instance
instead of the documents themselves it is possible to postpone use of the cursor,
and to extend the conditions to be used through "daisy-chaining" filters.

```python
# imports
...

class Person(Model):
    # define the fields
    ...

queryset = Person.filter({'age': {'$gte': 20}})
queryset.filter({'sex': 'm'})
# at this point the cursor has not been executed
for person in queryset:
    # now the cursor has been executed
    print person.name
```

As can be seen above dat provides a thin layer around the querying API for mongo
through the use of pymongo.

Conditions are the parameters used to compare against documents in the
collection and filter out any that don't match up. Whereas projections filter
out the fields from the resultant documents. The dat filter method is a thin
wrapper around the driver API that abstracts inclusion and exclusion of fields.
This is done through the assignment of the include and exclude kwargs
respectively.

---

## <a name="queryset"></a>QuerySets

QuerySet is a iterable object that configures and contains the cursor resulting
from the conditions and projections on a `Model.filter` call.

##### Filter - *Instance Method*
`queryset.filter(conditions=None, projection=None, include=None, exclude=None, limit=None)`

Allows for daisy-chaining of `filter` expressions. E.g.

```python
queryset = ExampleModel.filter({'name': 'Some Name'})
queryset.filter({'total': {'$gt': 20}})
```

---

##### Limit - *Instance Method*

`queryset.limit(<int>)`

Returns a QuerySet instance. Modifies the cursor so to limit the number of
documents returned. By default there is no limit set.
For more information please refer the the pymongo
[docs]().

```python
# imports
...

class Person(Model):
    # define the fields
    ...

queryset = Person.filter({'age': {'$gte': 20}})
queryset.filter({'sex': 'm'})
queryset.limit(10)
```

---

##### Hint - *Instance Method*
`queryset.hint(index)`

Returns a QuerySet instance. Modifies the cursor so to facilitate the search
with hinted index. For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.hint).

---

##### Sort - *Instance Method*
`queryset.sort(key_or_list, direction=ASCENDING)`

Returns a QuerySet instance. Modifies the cursor by adding sorting on the
returned documents. For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.sort).

---

##### Skip - *Instance Method*
`queryset.skip(<int>)`

Returns a QuerySet instance. Modifies the cursor by skiping documents.
For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.skip).

---

##### Distinct - *Instance Method*
`queryset.distinct(key_or_list)`

Returns a list. Returns a list of unique values within the found documents
for the specified field names. For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.distinct).

---

##### Update - *Instance Method*
`queryset.update(document, multi=True, upsert=False, **kwargs):`


Returns a QuerySet instance. Provides a thin wrapper around the MongoDB driver
for updates. It uses the conditions specified by the series of filters and executes
the defined document to be used when updating the found documents.

```python
# imports
...

class Person(Model):
    # define the fields
    ...

queryset = Person.filter({'age': {'$gte': 20}})
queryset.filter({'sex': 'm'})
queryset.limit(10)

queryset.update({'$set': {'generation': 'x'}})
```

For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update).

---

##### Count - *Instance Method*

`queryset.count(with_limit_and_skip=False)`

Returns an integer. For more information please refer the the pymongo
[docs](http://api.mongodb.org/python/current/api/pymongo/cursor.html#pymongo.cursor.Cursor.count).

---

##### len(queryset)

Returns an integer.

Calls queryset.count(with_limit_and_skip=True)

---
