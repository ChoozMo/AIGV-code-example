# Openshot

## Basic
The Basic code is like below.
```python
import openshot
from tqdm import tqdm
import sys
from pathlib import Path

if __name__ == "__main__":

  timeline = openshot.Timeline(1280, 720, openshot.Fraction(30000, 1001), 44100, 2, openshot.LAYOUT_STEREO)
  reader = openshot.FFmpegReader(sys.argv[1])
  clip = openshot.Clip(reader)
  timeline.AddClip(clip)
  writer = openshot.FFmpegWriter("tqdm_"+Path(sys.argv[1]).stem+".mp4")
  writer.SetAudioOptions(True, "aac", 44100, 2, openshot.LAYOUT_STEREO, 128000)
  writer.SetVideoOptions(True, "libx264", openshot.Fraction(30000, 1001), 1280, 720,openshot.Fraction(1, 1), False    , False, 10000000)
  timeline.Open()
  writer.Open()
  writer.WriteFrame(timeline, 1, timeline.GetMaxFrame())
  timeline.Close()
  writer.Close()
```

## tqdm (frame by frame)  
The code like this, If you process frame by frmae while writing.  
```python
import openshot
from tqdm import tqdm
import sys
from pathlib import Path

if __name__ == "__main__":

  timeline = openshot.Timeline(1280, 720, openshot.Fraction(30000, 1001), 44100, 2, openshot.LAYOUT_STEREO)
  reader = openshot.FFmpegReader(sys.argv[1])
  clip = openshot.Clip(reader)
  timeline.AddClip(clip)
  writer = openshot.FFmpegWriter("tqdm_"+Path(sys.argv[1]).stem+".mp4")
  writer.SetAudioOptions(True, "aac", 44100, 2, openshot.LAYOUT_STEREO, 128000)
  writer.SetVideoOptions(True, "libx264", openshot.Fraction(30000, 1001), 1280, 720,openshot.Fraction(1, 1), False    , False, 10000000)
  timeline.Open()
  writer.Open()
  for i in tqdm(range(1, timeline.GetMaxFrame()+1), total=timeline.GetMaxFrame(), unit='frame'):
    writer.WriteFrame(timeline.GetFrame(i))
  timeline.Close()
  writer.Close()
```
