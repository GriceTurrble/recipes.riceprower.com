import multiprocessing
import os

# Gunicorn settings
# https://docs.gunicorn.org/en/latest/settings.html

bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
log_file = "-"
# worker_tmp_dir = "/dev/shm"
workers = multiprocessing.cpu_count() * 2 + 1
# worker_class = "uvicorn.workers.UvicornWorker"
timeout = 30
keepalive = 2
