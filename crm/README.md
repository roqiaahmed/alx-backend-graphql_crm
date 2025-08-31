InstallRedis and dependencies.

```bash
    redis-server
    pip install -r requirements.txt

```

Run migrations.

```bash
    python manage.py migrate

```

Start Celery worker.

```bash
    celery -A crm worker -l info

```

Start Celery Beat .

```bash
    celery -A crm beat -l info

```
