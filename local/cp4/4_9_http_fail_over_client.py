﻿    #!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create on: 2015年11月1日 下午10:13:02
# 说明：让我们从矿大视频网站下载某个视频.，使用resume_download函数实现文件断点续传
# 适当改装一下可以成为爬虫下载某些网站附件的函数，实现断点续传
# todo：多线程断点下载，多线程爬虫
# todo：实时显示下载进度

import urllib
import os

TARGET_URL = 'http://libtrain.cumt.edu.cn/video/videocoll/'
TARGET_FILE = '2.flv'

class CustomURLOpener(urllib.FancyURLopener):
    # Overwrite FancyURLopener to skip error 206
    # when a partial file is being sent
    def http_error_206(self, url, fp, errcode, errmsg, headers, data = None):
        pass
    
def resume_download():
    file_exists = False
    CustomURLClass = CustomURLOpener()
    if os.path.exists(TARGET_FILE):
        out_file = open(TARGET_FILE, 'ab')
        file_exists = os.path.getsize(TARGET_FILE)
        # if the file exists, then only download the unfinished part
        CustomURLClass.addheader('range', 'bytes=%s-' % (file_exists))
    else:
        out_file = open(TARGET_FILE, 'wb')
    web_page = CustomURLClass.open(TARGET_URL + TARGET_FILE)
    
    # Check if last download was OK
    if int(web_page.headers['Content-Length']) == file_exists:
        loop = 0
        print "File already downloaded!"
        
    byte_count = 0
    while True:
        data = web_page.read(8192)
        if not data:
            break
        out_file.write(data)
        byte_count = byte_count + 1
        
    web_page.close()
    out_file.close()
    
    for k, v in web_page.headers.items():
        print k, '=', v
    print "file copied", byte_count, 'bytes from', web_page.url
    
if __name__ == "__main__":
    resume_download()
    
