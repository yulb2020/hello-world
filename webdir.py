# -*- coding: utf-8 -*-
import requests
import sys,json

def _usage():
    print "upload code files to scanner.baidu.com...\r\n"
    print "[usage:]python webdir.py webdir.tar.gz|webdir.zip...\r\n"

def upload_webdir(webdir):
    URL = 'http://scanner.baidu.com/enqueue'
    FILES = {'archive':open(webdir,'rb')}

    try:
        webdir_upload = requests.post(URL,files = FILES)

    except requests.RequestException as e:
        print(e)
    else:
        json_upload = webdir_upload.json()
        #print json_upload
        if json_upload[u'status'] == 'unknown':
            print 'upload failed'
            sys.exit(0)
        elif json_upload[u'status'] == 'pending':
            print 'upload success'
            print 'result url :  ' + json_upload[u'url']
            return json_upload[u'url']

if __name__ == '__main__':
    arglen = len(sys.argv)
    if arglen < 2:
        _usage()
        sys.exit(0)
    arg = sys.argv
    webdir = arg[1]

    URL_result = upload_webdir(webdir)

    try:
        r = requests.get(URL_result,timeout=5)
    except requests.RequestException as e:
        print(e)
    else:
        json_data = r.json()
        print '+'*50
        #print json_data
        if json_data[0][u'status'] == "done":

            num = json_data[0][u'cnt']
            r_data = json_data[0][u'data']
            for i in range(num):
                if r_data[i][u'descr'] != "N/A":

                    print 'path :' + r_data[i][u'path'] + '   descr:' + r_data[i][u'descr'] + '   sandbox:' + r_data[i][u'sandbox']
        else:
            print 'undone or return none'
