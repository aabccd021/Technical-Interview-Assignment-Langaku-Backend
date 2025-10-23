from django.db import migrations

class Migration(migrations.Migration):
    initial = True
    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE my_table (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                word_count INTEGER NOT NULL,
                user_id INTEGER NOT NULL
            );
            """,
        ),
    ]
