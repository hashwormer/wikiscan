#!/usr/bin/env python
#-*- coding:utf-8 -*-
#author:Darkpot

import requests
import json
import re
import yagmail
import argparse

class MyClass:
    
    parser = argparse.ArgumentParser(description='wiki 敏感信息扫描')
    parser.add_argument("-l", help="wiki url，If not input, it is global scan and auto send alarm email", type=str)
    parser.add_argument("-c", help="search result counts", type=int)
    args = parser.parse_args()
    input1 = args.l
    count =  args.c
    def globalScan(self,count):
        try:      
        #请求参数头设置
            keydict = ['siteSearch+~+"password"','siteSearch+~+"密码"','siteSearch+~+"pwd"','siteSearch+~+"Authorization"']
            url = 'http://wiki.com/rest/searchv3/1.0/cqlSearch'
            headers = {'cookie':'wiki.sso.cookie='}
            alist = []
            keywords=[]
            keyword_suffix=[]
        #白名单
            whitelist=['/pages/viewpage.action?pageId=12345']
        #根据关键词将搜索结果uri全部收集起来
            for b in keydict:
                params = {"cql":b,"start":0,"limit":count,"includeArchivedSpaces":"false"}
                req = requests.get(url,params=params,headers=headers)
                a = req.text
                middle = json.loads(a)
                size = middle["size"]
                for i in range(size):
                    href = middle["results"][i]["url"]
                    if href not in (alist+whitelist):
                        alist.append(href)
        #将xml等数据格式的直接挑出来，其他的正则匹配关键字
        #正则匹配样例：password= “”、password “”、password=12345、<password>123</password>
            for q in alist:
                url1='http://wiki.com'+q
                houzui = re.findall(r"(\.txt|\.xml|\.csv|\.xsl|\.log|\.py|\.php|\.go|\.java|\.jsp)$",url1)
                if houzui:
                    keyword_suffix.append(url1)
                else:
                    req1 =requests.get(url1,headers=headers)
                    text =req1.text
                    password = re.findall(r"(?i)(password(s)?|pwd(s)?)\s*(={0,1}\s*(\&quot;|')((?!密码|'|,)\S)+(\&quot;|')|=\s*((?!密码|\&quot)\S)+(,|\b))",text)
                    password1 = re.findall(r"(?i)\-p\s+(((?!密码|\&quot|123456)\S)+(,|\b)|(\&quot;|')((?!密码|123456)\S)+(\&quot;|'))",text)
                    password2 = re.findall(r"密码:((?!密码)\S)+(,|\b)",text)
                    password3 = re.findall(r"(?i)\&lt;password(s)?\&gt;((?!密码)\S)+\&lt;/password(s)?\&gt;",text)
                    password6 = re.findall(r"\&quot;\s*(password(s)?|pwd(s)?|Authorization)\s*\&quot;:\&quot;\s*((?!密码)\w)+\s*\&quot;",text)
                    password10 = re.findall(r"\s+(password(s)?|pwd(s)?|Authorization)\s*(:|：)\s*((?!密码|\&quot)\S)+(,|\b)",text)
                    password12 = re.findall(r"\&quot;(password(s)?|pwd(s)?)\&quot;\s*(,\s*\[\&quot;((?!密码)\S)+\&quot;\]|=&gt;\s*\&quot;((?!密码)\S)+\&quot;,)",text)
                    if password:
                        keywords.append(url1)                   
                    elif password1:
                        keywords.append(url1)                    
                    elif password2:
                        keywords.append(url1)                   
                    elif password3:
                        keywords.append(url1)
                    elif password6:
                        keywords.append(url1)
                    elif password10:
                        keywords.append(url1)
                    elif password12:
                        keywords.append(url1)
            yag = yagmail.SMTP(user = 'You_email@163.com', password = 'password', host = 'smtp.163.com')
            yag.send(to = ['receiver@email.com'], subject = 'wiki 敏感信息扫描', contents = ['关键词正则匹配:\n',str(keywords),'关键词+数据文件后缀匹配:\n',str(keyword_suffix)])

        except:
            print("\n程序执行失败\n")

    def singlePage(self,wiki):
        try:
            keywords0=[]
            keyword_suffix0=[]
            headers = {'cookie':'wiki.sso.cookie='}
            houzhui = re.findall(r"(\.txt|\.xml|\.csv|\.xsl|\.log|\.py|\.php|\.go|\.java|\.jsp)$",wiki)
            if houzhui:
                keyword_suffix0.append(wiki)
            else:
                req0 =requests.get(wiki,headers=headers)
                text0 =req0.text
                password0 = re.findall(r"(?i)(password(s)?|pwd(s)?)\s*(={0,1}\s*(\&quot;|')((?!密码|'|,)\S)+(\&quot;|')|=\s*((?!密码|\&quot)\S)+(,|\b))",text0)
                password7 = re.findall(r"(?i)\-p\s+(((?!密码|\&quot|123456)\S)+(,|\b)|(\&quot;|')((?!密码|123456)\S)+(\&quot;|'))",text0)
                password8 = re.findall(r"密码:((?!密码)\S)+(,|\b)",text0)
                password9 = re.findall(r"(?i)\&lt;password(s)?\&gt;((?!密码)\S)+\&lt;/password(s)?\&gt;",text0)
                password5 = re.findall(r"\&quot;\s*(password(s)?|pwd(s)?|Authorization)\s*\&quot;:\&quot;\s*((?!密码)\w)+\s*\&quot;",text0)
                password4 = re.findall(r"\s+(password(s)?|pwd(s)?|Authorization)\s*(:|：)\s*((?!密码|\&quot)\S)+(,|\b)",text0)
                password11 = re.findall(r"\&quot;(password(s)?|pwd(s)?)\&quot;\s*(,\s*\[\&quot;((?!密码)\S)+\&quot;\]|=&gt;\s*\&quot;((?!密码)\S)+\&quot;,)",text0)
                if password0:
                    keywords0.append(wiki)          
                elif password7:
                    keywords0.append(wiki)      
                elif password8:
                    keywords0.append(wiki)          
                elif password9:
                    keywords0.append(wiki)
                elif password5:
                    keywords0.append(wiki)
                elif password4:
                    keywords0.append(wiki)
                elif password11:
                    keywords0.append(wiki)
            print("关键词正则匹配:\n"+str(keywords0))
            print("关键词数据文件后缀匹配:\n"+str(keyword_suffix0))
        except:
            print("\n程序执行失败\n")	
        
x = MyClass()

if x.input1:
    x.singlePage(x.input1)
else:
    x.globalScan(x.count)

	
