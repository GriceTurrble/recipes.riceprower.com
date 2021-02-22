# Docker compose stuff

## Basics

```bash
# Startup
docker-compose up -d

# Shut down
docker-compose down

# Run a command inside one of the services
# Example: run migrations manually
docker-compose exec web poetry run python /app/hometools/manage.py migrate

# Container seems out-of-sync? Rebuild it:
docker-compose up -d --no-deps --build web
```

## TODO

Nginx is messing up at the root, redirecting to browser to `https://app`. What?

Go back to basics on it, try to reconfigure that kajigger?
