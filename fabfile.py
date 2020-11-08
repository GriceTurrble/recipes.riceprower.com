import posixpath

from fabric import task, Connection


@task
def deploy(
    c,  # type: Connection
):
    """Deploy the Hometools site."""
    # See the type hint above?
    # If you use real type annotation syntax, Fabric throws a ValueError
    # because its usage appears to be out of date. So, we have to use a comment.
    update_from_github(c)
    update_venv(c)
    update_django_project(c)
    restart_services(c)


def update_from_github(c: Connection):
    with c.cd(c.config.dirs.code_root):
        c.run("git fetch")
        c.run("git checkout main")
        c.run("git reset --hard origin/main")
        c.run("find . -name '*.pyc' -delete")


def update_venv(c: Connection):
    """Update pip dependencies."""
    # fmt: off
    files = (
        posixpath.join(c.config.dirs.code_root, "requirements.txt"),
    )
    # fmt: on
    with c.prefix(f"source {c.config.dirs.env_root}/bin/activate"):
        for req_file in files:
            c.run(f"pip install -r {req_file}")


def update_django_project(c: Connection):
    """Run migrate and collectstatic."""
    with c.cd(c.config.dirs.manage_root):
        with c.prefix(f"source {c.config.dirs.env_root}/bin/activate"):
            c.run("python manage.py collectstatic  --clear --noinput")
            c.run("python manage.py migrate --noinput")


def restart_services(c):
    c.sudo("sudo systemctl daemon-reload")
    c.sudo("sudo systemctl restart gunicorn nginx")
