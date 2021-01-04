import posixpath
import datetime

import pytz
from fabric import task, Connection

### DEPLOYMENT ###


def filename_time_str():
    """Output a timestamp string usable within a filename."""
    eastern = pytz.timezone("US/Eastern")
    return eastern.localize(datetime.datetime.now()).strftime("%Y-%m-%dT%H%M%S%z")


def pull_from_github(c: Connection):
    with c.cd(c.config.dirs.code_root):
        c.run("git fetch")
        c.run("git checkout main")
        c.run("git reset --hard origin/main")
        c.run("find . -name '*.pyc' -delete")


def update_dependencies(c: Connection):
    """Update pip dependencies."""
    with c.cd(c.config.dirs.code_root):
        # Upgrade pip first
        c.run(f"{c.config.python_bin} -m pip install --upgrade pip")
        # Install dependencies using Poetry
        c.run(f"{c.config.poetry_bin} install --no-dev --no-root --no-interaction")


def run_django_manage_steps(c: Connection):
    """Run migrate and collectstatic."""
    with c.cd(c.config.dirs.manage_root):
        with c.prefix(f"source {c.config.dirs.env_root}/bin/activate"):
            c.run("python manage.py collectstatic  --clear --noinput")
            c.run("python manage.py migrate --noinput")


def restart_services(c: Connection):
    c.sudo("sudo systemctl daemon-reload")
    c.sudo("sudo systemctl restart gunicorn nginx")


@task
def deploy(
    c,  # type: Connection
):
    """Deploy the Hometools site."""
    # See the type hint above?
    # If you use real type annotation syntax, Fabric throws a ValueError
    # because its usage appears to be out of date. So, we have to use a comment.
    print("+---------------------+")
    print("| Starting deployment |")
    print("+---------------------+\n")
    s3_backup(c)
    pull_from_github(c)
    update_dependencies(c)
    run_django_manage_steps(c)
    restart_services(c)
    print("\n+---------------------+")
    print("| Deployment complete |")
    print("+---------------------+")


### S3 BACKUP AND RESTORE ###
@task
def s3_backup(
    c,  # type: Connection
):
    """Take a manual backup of the database and push to S3."""
    db_name = c.config.postgres.db_name
    backup_filename = f"postgres_{db_name}_{filename_time_str()}.pgdump"
    db_user = c.config.postgres.user

    c.run(f'echo "Backing up {db_name}"')
    c.run(f'echo "  Dump file: {backup_filename}"')
    with c.cd(c.config.dirs.backups):
        c.run(
            (
                f"pg_dump --username {db_user} --format=custom {db_name} "
                f"> {backup_filename}"
            )
        )
        c.run(f'echo "  Copying to bucket {c.config.s3_buckets.backups} ..."')
        c.run(
            f"aws s3 cp {backup_filename} {c.config.s3_buckets.backups}/{backup_filename}"
        )
    c.run(f'echo "Backup completed for {db_name}"')


@task
def s3_restore(
    c,  # type: Connection
):
    """Restore the latest backup of the database from S3."""
    db_name = c.config.postgres.db_name
    db_user = c.config.postgres.user

    # Get our latest backup filename off of S3
    result = c.run(
        f"aws s3 ls {c.config.s3_buckets.backups} | awk '{{print $4}}' | sort | tail -n 1"
    )
    filename = result.stdout.strip()

    # Restore from the latest backup file
    c.run(f'echo "Restoring {db_name}"')
    c.run(f'echo "  Bucket: {c.config.s3_buckets.backups})"')
    c.run(f'echo "  Latest: {filename}"')
    c.run(
        (
            f"aws s3 cp {c.config.s3_buckets.backups}/{filename} - "
            f"| pg_restore --username {db_user} --dbname {db_name} --clean --no-owner"
        )
    )

    # Cleanup
    c.run('echo "Restore completed"')


@task
def s3_ls_latest(
    c,  # type: Connection
):
    """List the latest file in the S3 bucket for backsups."""
    c.run('echo "Latest backup in S3:"')
    c.run(f"aws s3 ls {c.config.s3_buckets.backups} | tail -n 1")
