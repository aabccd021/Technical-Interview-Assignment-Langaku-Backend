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
We will assume that the client will provide a unique `request_id` UUID for each request.

#### Implemented solution: `UNIQUE` constraint on `request_id`

To solve this, we simply store the `request_id` along with the request data in the database,
with a unique constraint on the `request_id` column. When duplicated requests arrive, 
we will catch the unique constraint violation error from the database,
and return 409 Conflict response to the client.

#### Alternative solution / future improvement 1: Using Redis for `request_id`s

We can use another storage to keep track of processed `request_id`s, such as Redis or simply python 
list in memory. Old `request_id`s can be expired after some time.

This solution will have faster lookups, as we don't need to hit the database for every request.
Also, we don't need to store `request_id` in the main database, as it's never used for anything else.

But doing this with python's memory will not work well with multiple django processes invoked by wsgi server.
Using Redis will work, but it adds operational complexity.

#### Alternative solution / future improvement 2: Pre-checking for existing `request_id`

We can select and check for existing entries with the same `request_id` before inserting a new entry.
The code will look better this way, as we don't need to "stringly match" database error messages like in the implemented solution.

Although this solution will require an extra database query for each request,
which will add latency and load to the database.

Also since this solution is not atomic,
there might be a race condition if two identical requests arrive at the same time,
which will require us to handle unique constraint violation error anyway.

#### Alternative solution / future improvement 3: Do nothing on conflict

Instead of returning 409 Conflict for duplicate requests, we can just return 200 OK.
On the SQL query we will do `ON CONFLICT ... DO NOTHING` to avoid unique constraint violation error.

This solution is totally valid. 
The only reason we return 409 Conflict in the implemented solution is to make the unit tests simpler. 
We can test duplicate request handling without needing to `SELECT` from the database after the insert.


### Aggregating learning data by time periods

#### Implemented solution: Using SQL aggregation functions

I delegated all the complexity of implementing this feature to PostgreSQL,
by writing a single SQL query that returns the aggregated data.

SQL query is declarative and a bit hard to read, so here is an imperative pseudocode of what the query does:
1. Generate all "period" from `from` to `to` with the given `granularity` (day, week, month).
2. For each generated "period", select all learning log entries that belong to that period.
3. Calculate the average `word_count` for the entries in that period.

The [`DATE_TRUNC`](https://www.postgresql.org/docs/current/functions-srf.html#FUNCTIONS-SRF)
function was used to determine "period" group of a timestamp.

#### Alternative solution / future improvement 1: Returning only periods with data

The implemented solution will return all periods even if there is no data for some periods.
This will simplify the client code, as the client will not need to fill in missing periods,
which is especially useful if we need to implement client code on multiple platforms (web, mobile, etc).

Although this also means we return "useless" data which can be omitted, 
increasing the amount of data transferred over the network, on both `database -> server` and `server -> client`.

If we want to optimize for smaller data transfer, we can modify the SQL query to only return periods that have data:

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

As you can see, this will also significantly simplify the SQL query, and reduce the load on the database.

#### Alternative solution / future improvement 2: Pre-aggregation and denormalization

When our application scales up, and we have a lot of learning log entries,
the aggregation query might become slow, as it needs to scan a lot of rows in the `learning_log` table.

To optimize this, we can denormalize the data by pre-aggregating the learning log entries into a separate table.
For example, we can have a `learning_log_aggregates` table:

```sql
CREATE TABLE learning_log_aggregates (
    user_id UUID,
    period TIMESTAMP,
    granularity VARCHAR(10),
    total_word_count INT,
    entry_count INT,
    PRIMARY KEY (user_id, period, granularity)
);
```

Then every time a new learning log entry is created, we also update the corresponding aggregate entry.
When querying for aggregated data, we simply select from the `learning_log_aggregates` table.
Actually we can just use this table if we don't need to store all the learning log entries,
just want to know the summarized data.

```sql
SELECT
    period,
    (total_word_count / entry_count) AS average_words_learned
FROM learning_log_aggregates
WHERE user_id = %(user_id)s 
  AND period BETWEEN %(from_date)s AND %(to_date)s
  AND granularity = %(granularity)s
ORDER BY period;
```

#### Alternative solution / future improvement 3: Caching results for past time periods

If the `to` parameter is in the past, that means the data will not change anymore.
We can cache the aggregated results for such queries, so that subsequent requests with the same parameters can be served faster.

We can use a simple in-memory KV database like Redis or python memory for this.
One thing to consider is how we construct the key, it needs to be consistent,
so simply stringifying the parameters dictionary might not be a good idea.
