from celery import Celery

app = Celery('status_test',
             broker='redis://localhost:6379',
             backend='redis://localhost:6379',
             include=['status_test.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
