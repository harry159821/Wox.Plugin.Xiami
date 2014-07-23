#!/usr/bin/env python
import time
TIME =  time.time()
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer
import urllib2,thread,sys

class Player():
    '''
    music player online
    '''
    def __init__(self,file_name):
        self.file_name = file_name
        self.mp3 = []
        self.i = 0
        self.play()

    def play(self):
        #self.file_name = "http://m5.file.xiami.com/813/98813/471688/1770554727_4338192_l.mp3?auth_key=3a3bd18007f1e3f998b069431fb98eff-1405900800-0-null"
        #dm = muxer.Demuxer(str.split(self.file_name, '.')[-1].lower())
        dm = muxer.Demuxer('mp3')
        #f = open(self.file_name, 'rb')
        snd = dec = None
        header = {
                    #'Referer': 'http://www.xiami.com/',
                    'User-Agent': 'User-Agent:Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36',
                 }
        request = urllib2.Request(self.file_name,headers=header)
        self.f = urllib2.urlopen(request)
        
        print 'Player Init Time:%s'%(time.time()-TIME)
        #s = self.f.read(32000)
        s = self.f.read(10000)
        thread.start_new_thread(self.download,())
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
                        try:
                            snd.play(data)
                        except Exception, e:
                            sys.exit(0)
            if self.i<len(self.mp3):
                s = self.mp3[self.i]
            else:
                s = []
            self.i = self.i + 1
            #s = self.f.read(2000)
        sys.exit(0)
        '''
        print 'DownLoad Complete'
        while snd.isPlaying():
            time.sleep(.05)
        '''

    def download(self):
        s = self.f.read(2000)
        i = 0
        while len(s):
            self.mp3.append(s)
            try:
                s = self.f.read(2000)
            except Exception, e:
                s = 0
            i = i+1        
        print 'Download Complete,Long:%s,Use time:%s'%(i,time.time()-TIME)
        thread.exit_thread()

if __name__ == "__main__":
    print 'python Init Time:%s'%(time.time()-TIME)
    player = Player("http://m5.file.xiami.com/813/98813/471688/1770554727_4338192_l.mp3?auth_key=5de7c9a7be8dc675985385cf5db8b4ee-1406160000-0-null")
