# Run Production

```bash
    gunicorn -k eventlet -w 1 -b 0.0.0.0:8000 "der_duemmste:create_app()"
```

## Run Local

```bash
uv run der-duemmste
```
