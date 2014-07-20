#!/usr/bin/env python
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer
import urllib2
'''
Play Mp3 Online
'''
def play(file_name):
    #file_name = "http://m5.file.xiami.com/813/98813/471688/1770554727_4338192_l.mp3?auth_key=3a3bd18007f1e3f998b069431fb98eff-1405900800-0-null"
    #dm = muxer.Demuxer(str.split(file_name, '.')[-1].lower())
    dm = muxer.Demuxer('mp3')
    #f = open(file_name, 'rb')
    snd = dec = None

    header = {
                    'Referer': 'http://www.xiami.com/',
                    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
                    }	
    request = urllib2.Request(file_name,headers=header)
    f = urllib2.urlopen(request)
    	
    s = f.read(32000)

    while len(s):
        frames = dm.parse(s)
        if frames:
            for fr in frames:
                if dec == None:
                    dec = acodec.Decoder(dm.streams[fr[0]])
                    
                r = dec.decode(fr[1])
                if r and r.data:
                    if snd == None:
                        snd = sound.Output(
                            int(r.sample_rate),
                            r.channels,
                            sound.AFMT_S16_LE)
                    data = r.data
                    snd.play(data)
        s = f.read(2000)

    while snd.isPlaying():
        time.sleep(.05)

if __name__ == "__main__":
    play("http://m5.file.xiami.com/813/98813/471688/1770554727_4338192_l.mp3?auth_key=3a3bd18007f1e3f998b069431fb98eff-1405900800-0-null")
