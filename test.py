import requests
from urllib.parse import unquote

video_id = "5qap5aO4i9A"
link = f"https://www.youtube.com/get_video_info?&video_id={video_id}"

response = unquote(requests.get(link).text)

StartIndex = response.index("https://manifest.")
StartIndex += response[StartIndex+1:].index("https://manifest.") + 1 
StopIndex = StartIndex + response[StartIndex:].index("index.m3u8") + len("index.m3u8")

print(response[StartIndex:StopIndex])


