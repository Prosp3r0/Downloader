# -*- coding: utf-8 -*-

import http.client
from time import time
from os.path import isfile
from os import stat

def GetUrlFileSize(URL):
    try:
#从url中得到host和文件path
        url=str(URL)
        index=url.find('/')
        if(index == -1):
            print('url is invalid,cannot parse')
            return -1
        else:
            host=url[0:index]
            path=url[index:]
        print('The url is %s,host is %s,path is %s'%(URL,host,path))
        conn=http.client.HTTPConnection(host)
        print('Connection have be created')
        conn.request('GET',path)
        res=conn.getresponse()
#得到需要下载的文件大小
        filesum=int(res.getheader('Content-Length'))
    except HTTPException as httpx:
        print(httpx)
    except:
        print('Some exception occured')
    finally:
        conn.close()
        return filesum

def DownloadURL(URL,BEGIN,OFFSET,FILE,FILE_BEGIN):
    try:
        url=str(URL)
        index=url.find('/')
        if(index == -1):
            print('url is invalid,cannot parse')
            return -1
        else:
            host=url[0:index]
            path=url[index:]
        print('The url is %s,host is %s,path is %s'%(URL,host,path))
        import http.client
        from time import time
        conn=http.client.HTTPConnection(host)
        print('Connection have be created')
        heads={"Range":"bytes=%d-%d"%(BEGIN,OFFSET)}
        conn.request('GET',path,"",heads)
        res=conn.getresponse()
#保存下载内容到文件中
        f=open(FILE,'ab')
        f.seek(FILE_BEGIN,0)
        buffer=bytearray(2048)
        total=0
        interval_total=0
        begin_time=time()
        while not res.closed:
            num=res.readinto(buffer)
            total=total + num
            interval_total=interval_total + num
            if(num == 0):
                print('download over')
                break
            f.write(buffer[:num])
            interval_time=int(time()-begin_time)
#每3秒记录一次下载速度
            if interval_time >=3:
                print('download now speed:%.2f(B/S)'%float(interval_total/interval_time))
                interval_total=0
                begin_time=time()
        f.close()
        conn.close()
    except HTTPException as httpx:
        print(httpx)
        return -1
    except:
        print('Some No handled Error occurred')
    finally:
        return total

url='mirror.bjtu.edu.cn/gnu/wget/wget-1.10.1.tar.gz'
#url='wt.onlinedown.net/down/MTV2012_395023.rar'
#从url获得文件名
index=url.rfind('/')
if(index != -1):
    filename=url[(index+1):]
    filesize=GetUrlFileSize(url)
    if isfile(filename):
        download_num=stat(filename).st_size
        print('\n\nbreakpoint:%d continue downloading...\n\n'%(download_num))
    else:
        download_num=0
        print('\n\nfirst downloading...\n\n')
    while download_num < filesize:
        download_num = download_num + DownloadURL(url,download_num,filesize,filename,download_num)
        print('---Execute over download %d sum:%d'%(download_num,filesize))
else:
    print('url parse failed')
