# -*- coding: utf-8 -*-
import urllib2
import urllib
import re

class Article:
    def __init__(self, rank, board_link, board, article_link, title, author_link, author):
        self.rank = rank
        self.board_link = board_link
        self.board = board
        self.article_link = article_link
        self.title = title
        self.author_link = author_link
        self.author = author

class Lily_Top10_Spider:
    def __init__(self):
        self.top10 = []
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent' : self.user_agent}
        

    # 获取十大信息，添加到列表中并返回列表
    def get_top10article(self):
        top10_url = 'http://bbs.nju.edu.cn/bbstop10'
        bbs_url = 'http://bbs.nju.edu.cn/'
        
        req = urllib2.Request(top10_url, headers = self.headers)
        response = urllib2.urlopen(req)
        top10_page = response.read()
        #print top10_page
        
        #unicode_top10_page = top10_page.decode('utf-8')
        pattern_str = '<tr.*?bgcolor=.*?><td>(.*?)<td><a.*?href=(.*?)>(.*?)</a><td><a.*?href="(.*?)">(.*?)\n</a><td><a.*?href=(.*?)>(.*?)</a><td>(.*?)\n'
        pattern = re.compile(pattern_str)
        #pattern = re.compile(r'<tr.*?bgcolor=.*?><td>(.*?)<td><a.*?href=(.*?)>(.*?)</a><td><a.*?href="(.*?)">(.*?)</a><td><a.*?href=(.*?)>(.*?)</a>')
        top10_retrive_infos = pattern.findall(top10_page)
        for info in top10_retrive_infos:
            article = Article(info[0], bbs_url + info[1], info[2], bbs_url + info[3], info[4], bbs_url + info[5], info[6])
            self.top10.append(article)
            #print info
            

        for a in self.top10:
            print a.title, a.author, a.board, a.article_link

    def get_article(self, url):
        # url + '&start=-1' 显示本主题全部帖子
        all_article_url = url + '&start=-1'
        req = urllib2.Request(all_article_url, headers = self.headers)
        response = urllib2.urlopen(req)
        article_content = response.read()
        #print article_content
        

        # use regular experssion to find out all the reply article content
        pattern_str = '<textarea.*?id=.*?class=hide>(.*?)--\n.*?</textarea>'
        pattern = re.compile(pattern_str, re.S)
        all_replies_content = pattern.findall(article_content)

        f = open('all_replies_content.txt', 'w')
        #print all_replies

        result_content = []
        for reply in all_replies_content:
            f.write(reply)
            result_content.append(reply)
            #print reply
        return result_content
        #return self.top10
        
   
ls = Lily_Top10_Spider()
ls.get_top10article()

print '#1 article content:'
article_content = ls.get_article(ls.top10[9].article_link)
for s in article_content:
    print s
print 'print end.'
            
