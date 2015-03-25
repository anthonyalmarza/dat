# About

Dat is a light-weight solution to building schema's for
[MongoDB](http://www.mongodb.org/) with Python.
The overall design of this project is heavily inspired by Django's ORM but
is trimmed down and tightly coupled to Mongo's API. This means that it is
not currently possible to change the backend database technology to say
PostgreSQL or redis. If you're looking for a more performant
database engine [TokuMx](https://github.com/Tokutek/mongo) is a Mongo
engine alternative that apparently works seamlessly with MongoDB drivers.
What this means is that you can use a cloud service such as
[ClouDB](https://cloudbs.io/) and connect to it in exactly the same way
you would connect to the MongoDB engine on say [MongoHQ]() or
[Compose.io]() but experience up to 50x performance improvements. Read
more TokuMX [here](http://www.tokutek.com/tokumx-for-mongodb/).

The story behind the name is simple. I don't ever want my co-workers to
ever use .csv or .dat files for data-science ever again. So because "dat"
is short and sweet I chose *dat* as the name (ha ha, get it?!).
Conveniently it also serves as a constant reminder of hell that is poorly
managed data and that the goal here is to create an easy to use interface
for Mongo document storage.
