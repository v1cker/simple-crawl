# coding:utf-8
import requests
from bs4 import BeautifulSoup
class form:
    def __init__(self,url,data,method):
        self.url = url
        self.method = method
        self.data = data
    def __str__(self):
        return str([self.url,self.method,self.data])
def get_sth(url):
    if 'http' not in url:
        url='http://'+url
    try:
        req = requests.get(url)
    except Exception as e:
        print e
        return
    forms = []
    soup = BeautifulSoup(req.text,'lxml')
    for i in soup.find_all('form'):
        action = i['action']
        data = [j['name'] for j in i.find_all('input')]
        method = i['method']
        forms.append(form(action,data,method))
    for i in forms:
        print url,'------------',i
    if not forms:
        print 'no forms here'
if __name__=='__main__':
    urls = ['www.gradms.sdu.edu.cn/login','www.bksms.sdu.edu.cn/login','student.sdu.edu.cn/login','www.zzzs.sdu.edu.cn/login','sv12.wljy.sdu.edu.cn:8080/login','jobms.sdu.edu.cn/login','ykt.wh.sdu.edu.cn/cas/login']
    for url in urls:
        get_sth(url)