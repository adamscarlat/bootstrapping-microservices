from pydantic import BaseModel


class ViewedVideoMessage(BaseModel):
  id: str
  video_path: str