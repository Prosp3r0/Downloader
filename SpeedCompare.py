import sys
import threading
import netifaces
import pycurl
import time
import urllib.request
from os import system
from os import stat
from os.path import isfile
from urllib.parse import urlsplit
import socket
import re

class MultiDownloader:
    def __init__(self, url):
        self.filename='default'
        thread_count=4
        self.starttime = 0
        self.endtime = 0
        self.durationtime = 0
        self.url = url
        self.fout = ''
        if self.filename == 'default':
            self.save_filename = self.url.split('/')[-1]
        else:
            self.save_filename = self.filename
        if isfile(self.save_filename):
            self.current_file_size = self.GetCurrentFileSize()
        else:
            self.current_file_size = 0
        self.thread_count = thread_count
        self.lock = threading.Lock()
        try:
            self.fout = open(self.save_filename, 'wb')
        except:
            self.fout.close()
            raise ValueError('cannot write file')
        #self.download()

    def GetCurrentFileSize(self):
        return stat(self.save_filename).st_size

    def __del__(self):
        self.fout.close()
        pass

    def get_file_size(self):
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/47.0.2526.106 Safari/537.36')
        req.method = 'HEAD'  # use request 'HEAD' instead of 'GET'
        return int(urllib.request.urlopen(req).getheader('Content-Length', 0))

    def __get_download_range(self):
        file_size = self.get_file_size()
        file_size -= self.current_file_size
        block_size = int(file_size) / self.thread_count
        return [(int(x * block_size + self.current_file_size), int((x + 1) * block_size - 1 + self.current_file_size))
                for x in range(self.thread_count)]

    def __write_block(self, write_range):
        req = urllib.request.Request(self.url)
        #req.add_header('User-Agent',
        #               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/47.0.2526.106 Safari/537.36')
        #req.add_header('Connection', 'Keep-Alive')
        #req.add_header('Range', 'bytes=%d-%d' % (write_range[0], write_range[1]))
        req.headers['Range'] = 'bytes=%d-%d' % (write_range[0], write_range[1])
        res = urllib.request.urlopen(req)
        buffer = res.read()
        self.lock.acquire()
        try:
            self.fout.seek(write_range[0], 0)
            self.fout.write(buffer)
        finally:
            self.lock.release()

    def download(self):
        all_threads = []
        #t = threading.Thread(self.GetSpeed())
        #t.setDaemon(False)
        #t.start()
        for write_range in self.__get_download_range():
            write_thread = threading.Thread(target=self.__write_block, args=(write_range,))
            write_thread.setDaemon(False)
            write_thread.start()
            all_threads.append(write_thread)
        for t in all_threads:
            t.join()

            """
        for write_range in self.__get_download_range():
            self.__write_block(write_range)
            """
    def GetSpeed(self):
        durationtime = 0
        starttime = time.time()
        former_file_size = 0
        while 1:
            currenttime = time.time()
            durationtime = currenttime - starttime
            while durationtime >= 3:
                current_file_size = self.GetCurrentFileSize()
                print (current_file_size/1024)
                downloadfile = current_file_size - former_file_size
                print ('speed: %s' % (float(downloadfile)/durationtime))
                durationtime = 0
                former_file_size = current_file_size
                starttime = currenttime

class MyThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        #startime = time.time()
        d = MultiDownloader(self.url)
        #t = threading.Thread(d.GetSpeed())
        #t.setDaemon(False)
        d.download()
        #d.GetSpeed()
        #t.start()

if __name__ == '__main__':
    t = []
    link1 = 'http://dldir1.qq.com/qqfile/qq/QQ8.9/20029/QQ8.9.exe'
    link2 = 'http://xmp.down.sandai.net/xmp/XMPSetup_5.2.14.5672-dl.exe'
    #regex.match
    #rex = re.match(r'(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$',link3)

    #rex = re.match(r'(?:)(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|',link3)
    """
    if rex:
        print('valide')
    else:
        print('wrong')
    """
    #print(len(result))
    task1 = MyThread(link1)
    t.append(task1)
    task2 = MyThread(link2)
    t.append(task2)
    start = time.time()
    task1.start()
    task2.start()
    for th in t:
        th.join()
    end = time.time()
    print(str(end - start))

