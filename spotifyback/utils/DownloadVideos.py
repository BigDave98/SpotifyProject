from pytube import YouTube
import urllib.request
from urllib.parse import quote
import re
#https://stackoverflow.com/questions/68945080/pytube-exceptions-regexmatcherror-get-throttling-function-name-could-not-find
def video_dowload(songs):
	for song in songs:
		path = ScrapeVidId(song)
		if path.split("//")[0] == "https:":
			yt = YouTube(path)
			try:
				video = yt.streams.get_highest_resolution()
				path_to_download = (r"C:\Users\Davi Ruas\Downloads")
				video.download(path_to_download)
			except Exception as e:
				return print(e)

def ScrapeVidId(query):
	BASIC = "http://www.youtube.com/results?search_query="
	encoded_query = quote(query)  # Codificar apenas o parâmetro de consulta

	URL = BASIC + encoded_query.replace(" ", "+")
	try:
		html = urllib.request.urlopen(URL)
		videos_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
		return "https://www.youtube.com/watch?v=" + videos_ids[0]
	except Exception as e:
		return print(e)






