# Models

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

Returns a [QuerySet](QuerySets.md).

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
