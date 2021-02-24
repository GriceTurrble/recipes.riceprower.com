# Development Nginx configuration

When running on a dev machine, the Dockerfile located here is used to copy in a barebones `nginx.conf` file to a containerized Nginx process. This lets us test using Nginx connectivity as a reverse-proxy to our usual Gunicorn service.

On production, by contrast, we'll use system Nginx to make more granular configurations, including SSL verification and host-specific changes.

This image is enabled by calling `docker-compose <command>`, which calls in `docker-compose.override.yml` automatically. This is suitable for a development environment only.

On production, the path to the main docker-compose config should be specified:

```bash
docker-compose -f docker-compose.yml <command>
```

Doing so will ignore the override file.
