# coding:utf-8
import sys
import re
import threading
import netifaces
import pycurl
from time import sleep
import time
import urllib.request
from os import system
from os import stat
from os.path import isfile
import untitled
from urllib.parse import urlsplit
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5 import QtCore

speed = []

class MyThread(threading.Thread):
    def __init__(self, url, filepath):
        threading.Thread.__init__(self)
        self.url = url
        if filepath == '':
            filepath = 'default'
        self.filepath = filepath

    def run(self):
        m = MultiDownloader(self.url)
        start = time.time()
        m.download()
        end = time.time()
        sp = 'taskspeed: ' + str(m.getfilesize() / 1024 / (end - start)) + 'kb/s'
        speed.append(sp)
        #reply = QMessageBox(QMessageBox.Warning, u"Congrats!", u"Done!", QMessageBox.Cancel)
        #reply.exec_()


class MyApp(QMainWindow, untitled.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        untitled.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.s = 0
        self.link = []
        self.addacfflag = 0
        self.dir = ''
        #        self.DownloadButton.clicked.connect(lambda: SpeedConfiguration().NetworkConfig())
        #        self.DirButton.clicked.connect(lambda: self.TaskBrowser_1.setText(SpeedConfiguration().iprouter[0]))
        self.DownloadButton.clicked.connect(lambda: self.startdownload())
        self.DirButton.clicked.connect(lambda: self.opendir())
        self.confacl.clicked.connect(lambda: self.configacl())
        QtCore.pyqtSlot()
        self.clearconf.clicked.connect(lambda: self.clearIPtable())


    def opendir(self):
        self.dir = QFileDialog.getExistingDirectory()
        # if self.dir == '':
        #    self.dir = 'default'
        self.lineEdit.setText(self.dir)

    def configacl(self):
        self.link = []
        self.link.append(self.textEdit.toPlainText())
        self.link.append(self.textEdit_2.toPlainText())
        while '' in self.link:
            self.link.remove('')
        #filter(None, self.link)
        # print(link)
        if self.link == []:
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Empty!", QMessageBox.Cancel)
            reply.exec_()
            # print('ok')
            return
        self.link = list(set(self.link))
        self.s = SpeedConfiguration(self.link)
        if not self.s.GetHost():
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Wrong url!", QMessageBox.Cancel)
            reply.exec_()
            return
        self.s.NetworkConfiguration()
        self.aclsignal.setText('ACL Done')
        self.addacfflag = 1


    def startdownload(self):
        # file_url = 'http://dldir1.qq.com/qqfile/qq/QQ8.0/16968/QQ8.0.exe'
        #link = self.textEdit.toPlainText().split(';')
        '''
        self.addr = self.textEdit.toPlainText() + ';' + self.textEdit_2.toPlainText()
        link = self.addr.split(';')
        '''
        self.link = []
        self.TaskBrowser_1.setText('Downloading...')
        #sleep(2)
        #self.s.NetworkConfiguration()
        self.link.append(self.textEdit.toPlainText())
        self.link.append(self.textEdit_2.toPlainText())
        while '' in self.link:
            self.link.remove('')
        filter(None, self.link)
        # print(link)
        if self.link == ['']:
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Empty!", QMessageBox.Cancel)
            reply.exec_()
            # print('ok')
            return
        t = []
        # self.TaskBrowser_1.setText(link[0])
        self.link = list(set(self.link))
        #self.s = SpeedConfiguration(self.link)
        #sleep(5)
        #print(self.link)
        starttime = time.time()
        for url in self.link:
            if url != '':
                self.TaskBrowser_1.append(url)
                h = MyThread(url, self.dir)
                t.append(h)
                h.setDaemon(False)
                h.start()
        for th in t:
            th.join()
        endtime = time.time()
        self.TaskBrowser_1.append('All Done')
        global speed
        speed.reverse()
        downloadspeed = ';'.join(speed)
        #downloadspeed = 'asdf'
        #print (downloadspeed)
        self.TaskBrowser_1.append(downloadspeed)
        self.TaskBrowser_1.append('Total Time: ' + str(endtime - starttime))
        speed = []

    def clearIPtable(self):
        if self.addacfflag == 1:
            if self.s.DoubleInterfaceFlag == 1 and len(self.link) >= 2:
                self.s.NetworkRecover()
                self.textEdit.setText('')
                self.textEdit_2.setText('')
                self.TaskBrowser_1.setText('')
                self.addacfflag = 0
        else:
            self.textEdit.setText('')
            self.textEdit_2.setText('')
            self.TaskBrowser_1.setText('')
            reply = QMessageBox(QMessageBox.Warning, u"Warning", u"Config ACL first!", QMessageBox.Cancel)
            reply.exec_()
            self.addacfflag = 0
        self.link = []
        self.aclsignal.setText('')
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
        # threading.Thread(self.GetIPRouter()).start()

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
        # self.LinkIPAddr.append(socket.gethostbyname(link))
        try:
            for host in self.LinkHost:
                ip = socket.gethostbyname(host)
                if ip == '':
                    reply = QMessageBox(QMessageBox.Warning, u"Error", u"Cannot Establish Connection!",
                                        QMessageBox.Cancel)
                    reply.exec_()
                    return
                r = ip.split('.')
                madeupip = r[0] + '.' + r[1] + '.' + r[2] + '.0/24'
                self.LinkIPAddr.append(madeupip)
        except:
            reply = QMessageBox(QMessageBox.Warning, u"Error", u"Cannot Establish Connection!", QMessageBox.Cancel)
            reply.exec_()
            return
            # return madeupip
            # return socket.gethostbyname(link)

    def NetworkConfiguration(self):
        if self.DoubleInterfaceFlag == 1 and len(self.links) != 1 and len(self.links) != '':
            # self.GetHost()
            self.GetLinkIP()
            self.CompareFileSize()
            self.AddACL(self.LinkIPAddr[0], self.iprouter[0])
            self.AddACL(self.LinkIPAddr[1], self.iprouter[1])

    def NetworkRecover(self):
        if len(self.LinkIPAddr) != 1 and self.DoubleInterfaceFlag == 1:
            self.DelACL(self.LinkIPAddr[0], self.iprouter[0])
            self.DelACL(self.LinkIPAddr[1], self.iprouter[1])

    def NetworkTest(self):
        if self.DoubleInterfaceFlag == 1 and len(self.links) != 1 and len(self.links) != 0:
            targetIP = '172.217.5.68'
            self.AddACL(targetIP, self.iprouter[0])
            avgspeed1 = self.GetAvgSpeed()
            self.DelACL(targetIP, self.iprouter[0])

            self.AddACL(targetIP, self.iprouter[1])
            avgspeed2 = self.GetAvgSpeed()
            self.DelACL(targetIP, self.iprouter[1])
            self.SpeedCompare(avgspeed1, avgspeed2)
            # threading.Thread(self.DownloadButton.clicked.connect(self.startdownload))
            self.DoubleInterfaceFlag = 1  # Double Interfaces exist

    def AddACL(self, DesIPAddr, RouterIP):
        cmd_add = 'sudo route -n add -net ' + DesIPAddr + ' ' + RouterIP
        system(cmd_add)

    def DelACL(self, DesIPAddr, RouterIP):
        cmd_delete = 'sudo route -n delete ' + DesIPAddr + ' ' + RouterIP
        system(cmd_delete)

    def GetHost(self):
        if len(self.links) != 0:
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
        # c.setopt(pycurl.MAXREDIRS, 5)
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
    def __init__(self, url, filepath='default', thread_count=4):
        self.url = url
        self.filepath = filepath
        self.starttime = 0
        self.durationtime = 0
        self.endtime = 0
        self.save_filename = self.url.split('/')[-1]
        if isfile(self.save_filename):
            self.current_file_size = stat(self.save_filename).st_size
        else:
            self.current_file_size = 0
        self.thread_count = thread_count
        if self.filepath == 'default':
            self.filepath = self.save_filename
        else:
            self.filepath = self.filepath + '/' + self.save_filename
        self.lock = threading.Lock()
        try:
            self.fout = open(self.filepath, 'wb')
        except:
            self.fout.close()
            raise ValueError('cannot write file')
            # self.download()

    def __del__(self):
        self.fout.close()
        pass

    def getfilesize(self):
        # print('ok')
        try:
            req = urllib.request.Request(self.url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                         'Chrome/47.0.2526.106 Safari/537.36')
            req.method = 'HEAD'  # use request 'HEAD' instead of 'GET'
            length = urllib.request.urlopen(req)
            # print('ok')
        except:
            # print(err)
            # self.lock.acquire()
            self.__del__()
            self.lock.release()
            exit(0)
        return int(length.getheader('Content-Length', 0))

    def getdownloadrange(self):
        fsize = self.getfilesize()
        file_size = fsize
        file_size -= self.current_file_size
        if file_size == 0:
            file_size = fsize
            self.current_file_size = 0
        block_size = int(file_size) / self.thread_count
        return [(int(x * block_size + self.current_file_size), int((x + 1) * block_size - 1 + self.current_file_size))
                for x in range(self.thread_count)]

    def writeblock(self, write_range):
        req = urllib.request.Request(self.url)
        # req.add_header('User-Agent',
        #               'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #               'Chrome/47.0.2526.106 Safari/537.36')
        #   req.add_header('Connection', 'Keep-Alive')
        #   req.add_header('Range', 'bytes=%d-%d' % (write_range[0], write_range[1]))
        try:
            req.headers['Range'] = 'bytes=%d-%d' % (write_range[0], write_range[1])
            res = urllib.request.urlopen(req)
        except:
            # self.lock.acquire()
            self.__del__()
            #self.lock.release()
            return
        buffer = res.read()
        self.lock.acquire()
        try:
            self.fout.seek(write_range[0], 0)
            self.fout.write(buffer)
        finally:
            self.lock.release()

    def download(self):
        all_threads = []
        # i = 1
        for write_range in self.getdownloadrange():
            write_thread = threading.Thread(target=self.writeblock, args=(write_range,))
            write_thread.setDaemon(False)
            write_thread.start()
            #allThreadPid.append(write_thread.pid)
            all_threads.append(write_thread)

        for t in all_threads:
            t.join()
        #reply = QMessageBox(QMessageBox.Warning, u"Congrats!", u"Done!", QMessageBox.Cancel)
        #reply.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
