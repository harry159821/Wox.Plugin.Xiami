#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib,urllib2,json
from bs4 import BeautifulSoup
import play,sys
import thread
true = True
null = None
false = False

def query(Allkey):
	Allkey = Allkey.encode("utf-8")
	key = ' '.join(Allkey.split(" ")[1:])
	if not key:
		return ""
	results = []
	url = 'http://www.xiami.com/search?key='+key.replace(" ",'+')		
	print url
	html = requests(url)
	bs = BeautifulSoup(html)
	for i in bs.select("tbody tr"):
		res = {}

		temp =  i.select("td.chkbox input")
		songID = temp[0]["value"]#歌曲id

		detail = getDetail(songID)
		if detail:
			songUrl = detail['location']
		else:
			songUrl = getUrl(songID)
		print songUrl

		temp =  i.select("td.song_name a")
		songName = temp[0]["title"]#歌曲名称
		songName = songName.replace(u'该艺人演唱的其他版本','')

		temp =  i.select("td.song_album a")
		songAlbum = temp[0].text#歌曲专辑

		temp =  i.select("td.song_artist a")
		SongArtist = temp[0].text#歌曲演唱者
		SongArtist = SongArtist.replace('\t','')
		SongArtist = SongArtist.replace('\n','')
		SongArtist = SongArtist.replace('\r','')
		SongArtist = SongArtist.replace(' ','')
		SongArtist = SongArtist.replace(u'该艺人演唱的其他版本','')

		if songName:
			songName = '-'+songName
		if not songUrl:
			'GetNoMp3'
			songName += '- GetNoMp3'
		res["Title"] = SongArtist+songName
		res["SubTitle"] = songAlbum
		res["ActionName"] = 'playMp3'
		res["IcoPath"] = './icon.png'
		res["ActionPara"] = songUrl
		results.append(res)

	return json.dumps(results)

def requests(url,timeouts=5):
	header = {
			'Referer': 'http://www.xiami.com/',
			#'Cookie':'_unsign_token=368284ea1c2f0791894ef34f82f7d767; bdshare_firstime=1399371186962; __gads=ID=4359827986682a79:T=1399371187:S=ALNI_MbmSeLyu1uEsvXqduaifFSnc_kN8g; _ga=GA1.2.410144452.1399299839; CNZZDATA921634=cnzz_eid%3D1456075632-1399299834-%26ntime%3D1402231078%26cnzz_a%3D1%26ltime%3D1402210763734%26rtime%3D14; CNZZDATA2629111=cnzz_eid%3D1234576666-1399299834-%26ntime%3D1402231078%26cnzz_a%3D1%26ltime%3D1402210764004%26rtime%3D14; __guestplay=MjA4MzMxOCwxOzM2NTIzMjYsMTszMzkwMTU5LDE7MzM5MDE1MywxOzE3Njg5NDgzMTQsMTszNDU4NDU2LDI7MjA4Mzc4OSwzOzM3MTI1NiwzOzIwNzU0NDgsNDsxNzcxMTM0NjAzLDE7MTc3MDU4MDE3NSwx; __utma=251084815.410144452.1399299839.1402382777.1403540428.21; __utmc=251084815; __utmz=251084815.1399299839.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); music_taobao_closed=1; member_auth=hD%2FKHo1P6jsxhvCRH4A2eiQatOGHH2KPld5R3OZ75Qp2JdtfZdf%2Fx6uZQQ5A0CWUkQBOVv%2FV3D5HF%2Bxc; user=8358857%22harry159821%22images%2Favatar_new%2F167%2F17%2F8358857%2F8358857_1358144591_1.jpg%222%2216280%22%3Ca+href%3D%27%2Fwebsitehelp%23help9_3%27+%3EDo%E2%80%A2%3C%2Fa%3E%2222%229%2210087%22f80ec7322e%221404989705; xgj_closed=1; ahtena_is_show=false; pnm_cku822=143tpOWUuXBidH1MRUA99K3ssfit9LnkrZhtg%3D%3D%7CtaBkcTQxVFF0YRRhNLEksWY%3D%7CtJFV4sbweFGpcSkNye3Y3fk9GW72Hlau1%2B7KHco%3D%7Cs6aDR2N2MzZTVnNmE2YztiOmAwbi1%2BKXwrciZwI3UlfSh%2BLHUgcj9A%3D%3D%7Csqcy9kFUkPWQlVF0sJSs5MAXwA%3D%3D%7CsYRA9%2FI2IxZzFtLHgsfCBgPH0pfS1xOGg4ZCVxJXUpYDBgPUAw%3D%3D%7CsPXw9TE08NURBEFUkKXwhUEE0w%3D%3D; t_sign_auth=263; isg=96BAD0EDD67A4E3F80DB7E29D280A010; _xiamitoken=73aef36dc220735c2b0c946223835367',
			'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
			}	
	request = urllib2.Request(url,headers=header)
	response = urllib2.urlopen(request,timeout=timeouts)
	html = response.read()
	if html:	
		return html
	return False

def location_dec(str):
	head = int(str[0])
	str = str[1:]
	rows = head
	cols = int(len(str)/rows) + 1

	out = ""
	full_row = len(str) % head
	for c in range(cols):
		for r in range(rows):
			if c == (cols - 1) and r >= full_row:
				continue
			if r < full_row:
				char = str[r*cols+c]
			else:
				char = str[cols*full_row+(r-full_row)*(cols-1)+c]
			out += char
	return urllib.unquote(out).replace("^", "0")

def getDetail(id):
	url = 'http://songs.sinaapp.com/apiv3.php?type=1&id='+id
	html = requests(url)
	html = html.replace('\/','/')
	html = json.loads(html)
	#print html['location']
	#print html['pic']
	#print html['lyric']
	return html

def getUrl(id):
	url = 'http://www.xiami.com/song/playlist/id/'+id+'/object_name/default/object_id/0'
	html = requests(url)
	bs = BeautifulSoup(html)
	bs = BeautifulSoup(str(bs))
	url = ''
	try:
		url = location_dec(bs.select('location')[0].text)
	except Exception, e:
		print e
	return url

def playMp3(context,url):
	thread.start_new_thread(playThread,(1,url))
	thread.exit()
	#play.play(url)
	#sys.exit(0)

def playThread(num,url):
	play.play(url)

if __name__ == '__main__':
	print query(u"xiami chelly")
	#print query(u"xiami fallen down")
