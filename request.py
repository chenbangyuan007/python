import requests
import time
from requests.adapters import HTTPAdapter

headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Host': 'info.win0168.com',
           # 'If-Modified-Since': 'Sat, 17 Nov 2018 03:53:06 GMT',
           'Referer': 'http://info.win0168.com/info/index_cn.htm',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=3))
s.mount('https://', HTTPAdapter(max_retries=3))
def sendRequest(url,host='info.win0168.com'):
    if host!=None:
        headers['Host']=host
    r=None;
    try:
        r = s.get(url, headers=headers)
    except:
        time.sleep(2)
        r = s.get(url, headers=headers,timeout=1)
    if(r.status_code!=200):
        time.sleep(2)
        r=s.get(url, headers=headers,timeout=1)
        if(r.status_code!=200):
            print(r.status_code)
            raise Exception("请求状态错误")
    html_doc = str(r.content, 'utf-8')
    return html_doc;

