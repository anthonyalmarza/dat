# Fields

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
instantiation to an attribute of the [Model](models.md) at class definition.
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
Boolean (default: False). If `True` then the field is indexed to force uniqueness of values in
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
