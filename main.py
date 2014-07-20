#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2,json
from bs4 import BeautifulSoup
import play
import thread
true = True
null = None
false = False

def query(Allkey):
	Allkey = Allkey.encode("utf-8")
	key = Allkey.split(" ")[1]
	if not key:
		return ""
	results = []		
	html = requests('http://www.xiami.com/search?key='+key)
	bs = BeautifulSoup(html)
	for i in bs.select("tbody tr"):
		res = {}

		temp =  i.select("td.chkbox input")
		songID = temp[0]["value"]#歌曲id

		detail = getDetail(songID)

		temp =  i.select("td.song_name a")
		songName = temp[0]["title"]#歌曲名称

		temp =  i.select("td.song_album a")
		songAlbum = temp[0].text#歌曲专辑

		temp =  i.select("td.song_artist b.key_red")
		SongArtist = temp[0].text#歌曲演唱者

		res["Title"] = SongArtist+'-'+songName
		res["SubTitle"] = songAlbum
		res["ActionName"] = 'playMp3'
		res["IcoPath"] = './icon.png'
		if detail:
			res["ActionPara"] = detail['location']
		results.append(res)

	return json.dumps(results)

def requests(url,timeouts=5):
	header = {
			'Referer': 'http://www.xiami.com/',
			'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			}	
	request = urllib2.Request(url,headers=header)
	response = urllib2.urlopen(request,timeout=timeouts)
	html = response.read()
	if html:	
		return html
	return False

def getDetail(id):
	url = 'http://songs.sinaapp.com/apiv3.php?type=1&id='+id
	html = requests(url)
	html = html.replace('\/','/')
	html = json.loads(html)
	#print html['location']
	#print html['pic']
	#print html['lyric']
	return html

def playMp3(context,url):
	thread.start_new_thread(playThread,(1,url))
	#play.play(url)

def playThread(num,url):
	play.play(url)

if __name__ == '__main__':
	print query(u"xiami 苏打绿 ")
