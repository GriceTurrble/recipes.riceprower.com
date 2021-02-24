# Docker compose stuff

## Basics

We've complicated things a little bit by having two docker-compose config files, one meant to override the other.

- For development, run `docker-compose ...` by itself.
- For production, run `docker-compose -f docker-compose.yml`, specifying the main config file. This should ignore the `.override` file, so we use production settings only.

```bash
# Startup
docker-compose up -d

# Shut down
docker-compose down

# Run a command inside one of the services
# Example: create superuser in the web service container
# (remember we use poetry, and try to specify the full path for completeness)
docker-compose exec web poetry run python /app/recipesite/manage.py createsuperuser

# Container seems out-of-sync? Build them:
docker-compose build
# Can also pass `--no-cache` to skip any cached steps
# and completely rebuild those containers from scratch

# Show the full config:
docker-compose config
```
