# Assignment Template

## Requirement
- [uv](https://github.com/astral-sh/uv)
- Docker

## Getting Started

```sh
# install dependencies
uv sync --all-groups

# run test
uv run poe test

# start dev server on http://127.0.0.1:8000
uv run poe dev

# lint code
uv run poe lint

# format code
uv run poe format
```

## API Documentation

API documentation is available as OpenAPI schema at [schema.yml](./schema.yml).
The schema is automatically generated from codebase using [drf-spectacular](https://github.com/tfranzel/drf-spectacular),
by running `uv run poe generate-schema`.

## Algorithms

### Avoiding duplicate request entries (idempotency)

A client might send the same request multiple times, either due to network issues or user actions.
To avoid creating duplicate entries in the database, our API needs to be idempotent.

#### Implemented solution

I took the simplest solution for this problem.

Let's assume that the client will provide a unique `request_id` UUID for each request.

Then we simply store the `request_id` along with the request data in the database,
with a unique constraint on the `request_id` column.

When duplicated requests arrive, 
we will catch the unique constraint violation error from the database,
and return 409 Conflict response to the client.

#### Alternative solution / future improvement 1

We can use another storage to keep track of processed `request_id`s, such as Redis or simply python 
list in memory. Old `request_id`s can be expired after some time.

This solution will have faster lookups, as we don't need to hit the database for every request.
Also, we don't need to store `request_id` in the main database, as it's never used for anything else.

But doing this with python's memory will not work well with multiple django processes invoked by wsgi server.
Using Redis will work, but it adds operational complexity.

#### Alternative solution / future improvement 2

We can select and check for existing entries with the same `request_id` before inserting a new entry.
The code will look better this way, as we don't need to "stringly match" database error messages like in the implemented solution.

Although this solution will require an extra database query for each request,
which will add latency and load to the database.

Also since this solution is not atomic,
there might be a race condition if two identical requests arrive at the same time,
which will require us to handle unique constraint violation error anyway.

#### Alternative solution / future improvement 3

Instead of returning 409 Conflict for duplicate requests, we can return 200 OK with the existing entry data.
On the SQL query we will do `ON CONFLICT ... DO NOTHING` to avoid unique constraint violation error.

This solution is totally valid. 
The only reason we return 409 Conflict in the implemented solution is to make the unit tests simpler. 
We can test duplicate request handling without needing to `SELECT` from the database after the insert.


### Aggregating learning data by time periods

#### Implemented solution

https://www.postgresql.org/docs/current/functions-srf.html#FUNCTIONS-SRF

#### Alternative solution / future improvement 3

```sql
SELECT
    DATE_TRUNC(%(granularity)s, timestamp) AS period,
    AVG(word_count) AS average_words_learned
FROM learning_log
WHERE user_id = %(user_id)s 
  AND timestamp BETWEEN %(from_date)s AND %(to_date)s
GROUP BY period
ORDER BY period;
```

#### Caching past results

cache
