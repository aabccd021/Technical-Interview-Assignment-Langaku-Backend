# Assignment Template

## Requirement
- uv
- docker

## Initial Setup

```sh
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
