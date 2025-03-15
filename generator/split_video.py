import subprocess
import glob

segment_counter = 0  

for i in range(1, 6):
    input_file = f"music{i}.mp3"
    output_pattern = "output_%03d.wav"

    cmd = [
        "ffmpeg", "-i", input_file, "-f", "segment", "-segment_time", "10", "-segment_start_number", str(segment_counter), "-c", "copy", output_pattern
    ]

    subprocess.run(cmd)

    segment_counter = len(glob.glob("output_*.mp3"))