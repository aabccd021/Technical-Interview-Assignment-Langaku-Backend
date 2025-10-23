from pathlib import Path

SECRET_KEY = "django-insecure-4x21@2t7v6skhvmg9-8wslzd+9-g@5_!v(wrmv3f#a7mi$e@ze"

DEBUG = True

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "assignment",
]

ROOT_URLCONF = "assignment.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "mydb",
        "USER": "myuser",
        "PASSWORD": "mypw",
        "HOST": "db",
        "PORT": "5432",
    }
}

STATIC_URL = "static/"
