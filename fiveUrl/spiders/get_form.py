# coding:utf-8
import requests
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool


class Form:
    def __init__(self,url,data,method):
        self.url = url
        self.method = method
        self.data = data

    def __str__(self):
        return str([self.url,self.method,self.data])


def get_sth(text):
    soup = BeautifulSoup(text,'lxml')
    forms = []
    for i in soup.find_all('form'):
        action = i['action']
        data = [j['name'] for j in i.find_all('input')]
        method = i['method']
        forms.append(Form(action,data,method))
    return forms
if __name__ == '__main__':
    urls = [i.strip() for i in open('sdu.edu.cn').readlines()]
    for url in urls:
        try:
            pool = Pool(processes=40)
        except Exception as e:
            print url,e