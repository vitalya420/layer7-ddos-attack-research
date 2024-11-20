import multiprocessing

bind = "unix:/app/app.sock"
workers = (2 * multiprocessing.cpu_count()) + 1

timeout = 30

worker_class = "sync"

keepalive = 2

max_requests = 1000
max_requests_jitter = 50

reload = True

pidfile = "/app/gunicorn.pid"
