# coding:utf-8
import sys
import threading
import netifaces
import pycurl
import time
import urllib.request
from os import system
from os import stat
from os.path import isfile
import untitled
from urllib.parse import urlsplit
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyApp(QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        untitled.Ui_MainWindow.__init__(self)
        self.ip = []
        self.iprouter = []

        self.setupUi(self)
        #self.link = self.textEdit.toPlainText()
        #self.file_url.split(';')

        self.GetIPRouter()
        self.TaskBrowser_1.setText(self.iprouter[0])
        cmd = 'sudo route -n add -net 216.58.216.4 ' + self.iprouter[0]
        system(cmd)

        #threading.Thread(self.DownloadButton.clicked.connect(self.startdownload))

    def startdownload(self):
        #file_url = 'http://dldir1.qq.com/qqfile/qq/QQ8.0/16968/QQ8.0.exe'
        link = self.textEdit.toPlainText().split(';')
        #self.TaskBrowser_1.setText(link[0])
        link = list(set(link))
        for url in link:
            if url != '':
                self.TaskBrowser_1.setText(url)
                threading.Thread(MultiDownloader(url).download()).start()

    def GetTargetIPAddr(self):
        for url in self.file_url:
            rest = urlsplit(url).netloc
            self.ip.append(socket.gethostbyname(rest))

    def GetIPRouter(self):
        for interface in netifaces.interfaces():
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                if routingIPAddr != "127.0.0.1":
                    i = 0
                    while interface != netifaces.gateways()[netifaces.AF_INET][i][1]:
                        i += 1
                        if i == len(netifaces.gateways()[netifaces.AF_INET]):
                            i -= 1
                            break
                    self.iprouter.append(netifaces.gateways()[netifaces.AF_INET][i][0])
            except KeyError:
                pass



class MultiDownloader:
    def __init__(self, url, filename='default', thread_count=4):
        self.url = url
        if filename == 'default':
            self.save_filename = self.url.split('/')[-1]
        else:
            self.save_filename = filename
        if isfile(filename):
            self.current_file_size = stat(filename).st_size
        else:
            self.current_file_size = 0
        self.thread_count = thread_count
        self.lock = threading.Lock()
        try:
            self.fout = open(self.save_filename, 'wb')
        except:
            self.fout.close()
            raise ValueError('cannot write file')

    def __del__(self):
        self.fout.close()
        pass

    def get_file_size(self):
        """
                获取文件大小
                """
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
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/47.0.2526.106 Safari/537.36')
        req.add_header('Connection', 'Keep-Alive')
        req.add_header('Range', 'bytes=%d-%d' % (write_range[0], write_range[1]))
        res = urllib.request.urlopen(req)
        buffer = res.read()
        self.lock.acquire()
        try:
            self.fout.seek(write_range[0], 0)
            self.fout.write(buffer)
        finally:
            self.lock.release()

    def download(self):
        """
                根据不同的分块创建多个线程开始下载
                """

        all_threads = []
        for write_range in self.__get_download_range():
            write_thread = threading.Thread(target=self.__write_block, args=(write_range,))
            write_thread.setDaemon(False)
            write_thread.start()
            all_threads.append(write_thread)
        for t in all_threads:
            t.join()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

    # file_url = 'http://s2.cdn.xiachufang.com/870340248ab311e58498b82a72e00100.jpg'
    # file_url = 'http://ww4.sinaimg.cn/thumbnail/4eafaa70gw1ezjvstaokqj21kw1kwe7m.jpg'
    # file_url = 'http://dldir1.qq.com/qqfile/qq/QQ8.0/16968/QQ8.0.exe'
    # start = time.clock()
    # downloader = MultiDownloader(file_url)
    # downloader.download()
    # end = time.clock()
    # print('total time: %f s' % (end - start))
    # print('speed: %f KB/s' % (downloader.get_file_size() / 1024 / (end - start)))
