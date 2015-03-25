# Installation

Make sure that you have MongoDB installed somewhere.

In your terminal (within a virtualenv) type the following...

```bash
    pip install dat
```

# Making your first model

In your project add a module, which can be called anything but for sanities
sake let's call it `models.py`.

```python
# in your_project/models.py
from dat import fields
from dat.models import Model


class MyFirstModel(Model):

    name = fields.Char()
    count_of_files = fields.Int(default=0)
    seconds_to_mars = fields.Float()

```

Now in a shell we can interface with a mongo database using this schema.

```bash
~$: python
>>> from your_project.models import MyFirstModel
>>> first_instance = MyFirstModel(name='Steve', seconds_to_mars=10.1)
>>> first_instance.save()
```

By default `dat` connects to the default settings for a mongo server on the
localhost. To connect to a remote database refer to the section below.

# Connecting to a remote database

In your terminal define the `DAT_REPLICA_SET_URI` and `DAT_REPLICA_SET_NAME`
environment variables:

```bash
export DAT_REPLICA_SET_URI="mongodb://<USER_NAME>:<PASSWORD>@<URI_1>:<PORT_1>,<URI_2>:<PORT_2>/<DATABASE_NAME>"
export DAT_REPLICA_SET_NAME="set-<UID_HASH>"
```

Make sure to substitute `<USER_NAME>`, `<PASSWORD>`, `<URI_1>`, `<PORT_1>`,
`<URI_2>`, `<PORT_2>`, `<DATABASE_NAME>` and `<UID_HASH>` for actual values.
Remember to keep this information safe e.g. not in your github repository.
