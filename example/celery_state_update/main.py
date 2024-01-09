root@choozmo3060:~/AIGV_examples/celery# cat status_test.py
from status_test.tasks import export_video
from time import sleep
from tqdm import tqdm

if __name__ == "__main__":
        res = export_video.delay('angela.mp4')
        p = 0
        while(True):
                state = res.state
                info = res.info
                if state == "PROGRESS" and info:
                        t = tqdm(total=info['total'], unit='frame')
                        break
                sleep(0.5)

        while(True):
                state = res.state
                info = res.info
                if state == "PROGRESS" and info:
                        t.update(info['current']-p)
                        p = info['current']
                if state == "SUCCESS":
                        t.update(t.total-p)
                        t.close()
                        break
                sleep(0.5)
