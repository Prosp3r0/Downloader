# coding:utf-8
import sys
import re
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
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

class MyThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url

    def run(self):
        MultiDownloader(self.url).download()

class MyApp(QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        untitled.Ui_MainWindow.__init__(self)
        self.setupUi(self)
#        self.DownloadButton.clicked.connect(lambda: SpeedConfiguration().NetworkConfig())
#        self.DirButton.clicked.connect(lambda: self.TaskBrowser_1.setText(SpeedConfiguration().iprouter[0]))
        self.DownloadButton.clicked.connect(lambda: self.startdownload())

    def startdownload(self):
        # file_url = 'http://dldir1.qq.com/qqfile/qq/QQ8.0/16968/QQ8.0.exe'
        link = self.textEdit.toPlainText().split(';')
        #print(link)
        if link == ['']:
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Empty!", QMessageBox.Cancel)
            reply.exec_()
            #print('ok')
            return
        t = []
        # self.TaskBrowser_1.setText(link[0])
        link = list(set(link))
        s = SpeedConfiguration(link)
        if not s.GetHost():
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Wrong url!", QMessageBox.Cancel)
            reply.exec_()
            return
        s.NetworkConfiguration()
        for url in link:
            if url != '':
                self.TaskBrowser_1.setText(url)
                h = MyThread(url)
                t.append(h)
                h.setDaemon(False)
                h.start()
        for th in t:
            th.join()
        s.NetworkRecover()
        """
        for th in t:
            th.start()
        for th in t:
            th.join()
        s.NetworkRecover()
        """


        """
        c = []
        task1 = MultiDownloader('http://dldir1.qq.com/qqfile/qq/QQ8.9/20029/QQ8.9.exe')
        task2 = MultiDownloader('http://down.sandai.net/mac/thunder_3.0.4.2714.dmg')
        a = threading.Thread(task1.download())
        b = threading.Thread(task2.download())
        c.append(a)
        c.append(b)
        for th in c:
            th.run()
        #a.start()
        #b.start()
        """


class SpeedConfiguration:
    def __init__(self, DownloadLinks):
        self.LinkIPAddr = []
        self.iprouter = []
        self.LinkHost = []
        self.links = DownloadLinks
        self.DoubleInterfaceFlag = 0
        self.GetIPRouter()
        self.NetworkTest()
        #threading.Thread(self.GetIPRouter()).start()

    #        self.TaskBrowser_1.setText(self.iprouter[0])

    def GetFileSize(self, url):
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/47.0.2526.106 Safari/537.36')
        req.method = 'HEAD'  # use request 'HEAD' instead of 'GET'
        return int(urllib.request.urlopen(req).getheader('Content-Length', 0))

    def CompareFileSize(self):
        size = []
        for ln in self.links:
            size.append(self.GetFileSize(ln))
        if size[0] < size[1]:
            self.LinkIPAddr.reverse()

    def GetLinkIP(self):
        #self.LinkIPAddr.append(socket.gethostbyname(link))
        try:
            for host in self.LinkHost:
                ip = socket.gethostbyname(host)
                if ip == '':
                    reply = QMessageBox(QMessageBox.Warning, u"Error", u"Connot Establish Connection!",
                                        QMessageBox.Cancel)
                    reply.exec_()
                    return
                r = ip.split('.')
                madeupip = r[0] + '.' + r[1] + '.' + r[2] + '.0/24'
                self.LinkIPAddr.append(madeupip)
        except:
            reply = QMessageBox(QMessageBox.Warning, u"Error", u"Connot Establish Connection!", QMessageBox.Cancel)
            reply.exec_()
            return
        #return madeupip
        #return socket.gethostbyname(link)

    def NetworkConfiguration(self):
        if self.DoubleInterfaceFlag == 1:
            #self.GetHost()
            self.GetLinkIP()
            self.CompareFileSize()
            self.AddACL(self.LinkIPAddr[0], self.iprouter[0])
            self.AddACL(self.LinkIPAddr[1], self.iprouter[1])

    def NetworkRecover(self):
        if len(self.LinkIPAddr) != 1 and self.DoubleInterfaceFlag == 1:
            self.DelACL(self.LinkIPAddr[0], self.iprouter[0])
            self.DelACL(self.LinkIPAddr[1], self.iprouter[1])

    def NetworkTest(self):
        if self.DoubleInterfaceFlag == 1:
            targetIP = '172.217.5.68'
            self.AddACL(targetIP, self.iprouter[0])
            avgspeed1 = self.GetAvgSpeed()
            self.DelACL(targetIP, self.iprouter[0])

            self.AddACL(targetIP, self.iprouter[1])
            avgspeed2 = self.GetAvgSpeed()
            self.DelACL(targetIP, self.iprouter[1])
            self.SpeedCompare(avgspeed1, avgspeed2)
            # threading.Thread(self.DownloadButton.clicked.connect(self.startdownload))
            self.DoubleInterfaceFlag = 1 # Double Interfaces exist

    def AddACL(self, DesIPAddr, RouterIP):
        cmd_add = 'sudo route -n add -net ' + DesIPAddr + ' ' + RouterIP
        system(cmd_add)

    def DelACL(self, DesIPAddr, RouterIP):
        cmd_delete = 'sudo route -n delete ' + DesIPAddr + ' ' + RouterIP
        system(cmd_delete)

    def GetHost(self):
        if self.links != '':
            for url in self.links:
                rest = urlsplit(url).netloc
                rex = re.match(r'(?i)^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', rest)
                if not rex:
                    print(rest)
                    return 0
                self.LinkHost.append(rest)
            return 1
        else:
            return 0

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
        if len(self.iprouter) != 1:
            self.DoubleInterfaceFlag = 1
        else:
            return

    def TestSpeed(self):
        c = pycurl.Curl()
        # c.setopt(pycurl.ENCODING, 'gzip')
        c.setopt(pycurl.URL, '172.217.5.68')
        #c.setopt(pycurl.MAXREDIRS, 5)
        c.perform()
        http_speed_downlaod = c.getinfo(pycurl.SPEED_DOWNLOAD)
        # print("平均下载速度： %d k/s" % (http_speed_downlaod))
        return (http_speed_downlaod)

    def GetAvgSpeed(self):
        speed = []
        a = 0
        sum = 0
        while a < 10:
            speed.append(self.TestSpeed())
            a = a + 1
        for i in speed:
            sum = int(sum) + int(i)
        avgspeed = sum / len(speed)
        # print(avgspeed)
        return avgspeed

    def SpeedCompare(self, avg1, avg2):
        if avg1 < avg2:
            self.iprouter.reverse()  # put faster network in front of slow one


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
        #self.download()

    def __del__(self):
        self.fout.close()
        pass

    def get_file_size(self):
        """
                获取文件大小
                """
        try:
            req = urllib.request.Request(self.url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                     'Chrome/47.0.2526.106 Safari/537.36')
            req.method = 'HEAD'  # use request 'HEAD' instead of 'GET'
            return int(urllib.request.urlopen(req).getheader('Content-Length', 0))
        except Exception as err:
            #print(err)
            reply = QMessageBox(QMessageBox.Warning, u"Error", u"Connot Establish Connection!", QMessageBox.Cancel)
            reply.exec_()
            return

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
        """
        for write_range in self.__get_download_range():
            self.__write_block(write_range)
        """

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
