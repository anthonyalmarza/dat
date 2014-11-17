# Dat v0.0.0

**dat**: Lightweight MongoDB ORM.

Look how easy it is to use:

    from dat.models import Model
    from dat.fields import Int, Float, Char, List, TimeStamp

    class Person(Model):

        namespace = 'my_custom_collection_name'

        created = TimeStamp(default=datetime.utcnow)
        age = Int()
        name = Char(index=TEXT)
        parents = List()
        height = Float()

    bob = Person(name='bob', age=30, parents=['Mary', 'John'], height=1.7)
    bob.save()

## Features

- Easy to use Django-like schema definition and query interface
- Daisy-chain filter queries
- Easy to use indexing
- Light-weight documents i.e. fields not set aren't saved to the document
- `unique_together` and `compound_index` definitions on the model
- Thinly wraps pymongo to leverage full use of it's drivers

## Installation

Install dat by running:

    pip install dat

## Contribute

- Issue Tracker: [https://github.com/anthonyalmarza/dat/issues](https://github.com/anthonyalmarza/dat/issues)
- Source Code: [https://github.com/anthonyalmarza/dat](https://github.com/anthonyalmarza/dat)

## Support

If you are having issues, please let us know.
We have a mailing list located at: dat@google-groups.com

## License

The project is licensed under the MIT license.
