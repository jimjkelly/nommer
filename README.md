# Nommer

Nommer is an application for ordering food.

## Running Nommer

You can run the development version of the Nommer server by running the following,
assuming you have an up-to-date version of Docker on your system:

```bash
$ docker-compose up -d
$ docker-compose run --rm nommer flask init-db
```

The server is now set up and reaady to go. Run the CLI application like so:

```bash
$ docker-compose run --rm cli poetry run nommer
```

This will start the application, and allow you to interact with the server.
If you need to reset the database, do it like so:

```bash
$ docker-compose run --rm nommer flask drop-db
$ docker-compose run --rm nommer flask init-db
```

## Running Tests

The test suite can be run with the following command:

```bash
$ docker-compose run --rm nommer pytest
```

This runs the tests found in the `tests` folder, runs the [black](https://github.com/ambv/black)
style checker, a flake8 static analysis tool, and finally the mypy
type checker.

## Known Bugs

There are several known bugs:

- The data model as I originally designed it was wrong. I originally
thought I could get away with just having a many-to-many field with
items and orders and that this would allow me to add items to an order
but I didn't consider that this fails if you try to add multiple
instances of an item to an order.  There are several ways to fix
this, all requiring the use of an additional table (there's already
an additional table technically, the ORM made one, but adding it
ourself would allow us to have multiple entries for item/order
comos or a quanitty field).

- I'm using the same testing database as I am for the main
application - if you run the tests it will drop the database.
Normally I would put in some code to create a specific testing
database and remove it but I didn't want to spend the time for
this.

- The JSON-API auto-generated url endpoints are wrong for the id.

## Other Caveats and Limitations

There are a lot of caveats and limitations that come with this code:

- There are no query optimizations here. Things like N+1 queries
are a common source of slowness.  I generally prototype rapidly
not worrying about this, and I'd take an APM to it to identify
bottlenecks.

- There's not any logging beyond the standard Flask logging. Normally
there might be additional information logged, and of course it would
be set up to be logged to an external service.  On that subject,
I'd often integrate a tool like Rollbar for exception alerting,
and something like DataDog for metrics reporting.

- This of course only implements the limited set of API endpoints
necessary for the task at hand.

- The tests are pretty spartan. There's decent coverage - most of
the happy paths are covered, but there's no real coverage of
sad paths.  With more time I'd add tests to the various endpoints
to demonstrate common HTTP response codes, and confirm the form
of the returned error message.

- The amount of attention paid to proper HTTP return codes for
REST was somewhat minimal, aside from some instances like the
PUT returnign a 204.

- The CLI is completely without tests, and only a minimal amount
of thought went into the code design.  This could be improved
but time was a large issue.

- There's no pagination of results on the API. With more time that
would be added.

- There's no versioning of the API endpoints to ensure future
versions don't break existing clients.

- The order states can currently be changed to any valid value.
In real life it probably would make sense to make state changes
here be controlled, and ensure they can only go in a sensible
way (i.e. an open order can't become a cart)

- A more robust setup would have included the currency type.
Related, there should be better tests around currency items.

There's a ton wrong with this, but well, it was done in a day. :)
