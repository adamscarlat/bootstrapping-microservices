import os

def get_file_size(path: str):
  return os.path.getsize(path)

# Function to read video file as bytes
def stream_video_file(video_path: str):
  with open(video_path, mode='rb') as video_file:
    while True:
      chunk = video_file.read(1024)
      if not chunk:
        break
      yield chunk