from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE learning_log  (
                request_id UUID PRIMARY KEY,
                user_id TEXT NOT NULL,
                word_count INTEGER NOT NULL CHECK (word_count >= 0),
                timestamp TIMESTAMP NOT NULL
            );
            """,
        ),
    ]
