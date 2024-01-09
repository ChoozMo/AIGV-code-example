from .celery import app
import openshot
from pathlib import Path
from tqdm import tqdm
from time import time, sleep

@app.task(bind=True)
def export_video(self, filename):
        timeline = openshot.Timeline(1280, 720, openshot.Fraction(30000, 1001), 44100, 2, openshot.LAYOUT_STEREO)
        reader = openshot.FFmpegReader(filename)
        clip = openshot.Clip(reader)
        timeline.AddClip(clip)

        writer = openshot.FFmpegWriter("tqdm_"+Path(filename).stem+".mp4")
        writer.SetAudioOptions(True, "aac", 44100, 2, openshot.LAYOUT_STEREO, 128000)
        writer.SetVideoOptions(True, "libx264", openshot.Fraction(30000, 1001), 1280, 720,openshot.Fraction(1, 1), False, False, 10000000)
        timeline.Open()
        writer.Open()
        #writer.WriteFrame(timeline, 1, timeline.GetMaxFrame())
        total = timeline.GetMaxFrame()
        t = time()
        for i in tqdm(range(1, total+1), total=total, unit='frame',mininterval=1.0):
                writer.WriteFrame(timeline.GetFrame(i))
                if not self.request.called_directly and time()-t>=1:
                        self.update_state(state='PROGRESS', meta={'current': i, 'total': total})
                        t = time()
                sleep(0.1)
        timeline.Close()
        writer.Close()
