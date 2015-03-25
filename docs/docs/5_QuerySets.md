# QuerySets

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

Returns a QuerySet instance. Modifies the cursor by skipping documents.
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
