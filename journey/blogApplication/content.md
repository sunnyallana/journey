# Creating and configuring a django project:

You can run the Django development server on a custom host and port or tell Django to load a specific settings file, as follow

```bash
    python manage.py runserver 127.0.0.1:8001 \--settings=mysite.settings
```

## When you have to deal with multiple environments that require different configurations, you can create a different settings file for each environment.


This server is only intended for development and is not suitable for production. Use either of WSGI or ASGI for production.