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

##

https://www.postgresql.org/docs/current/functions-srf.html#FUNCTIONS-SRF


## Future improvements

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

cache
