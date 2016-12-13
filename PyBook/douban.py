#coding:utf-8
import requests
from urllib import quote
import datetime
from bs4 import BeautifulSoup
import HTMLParser
import sys
import hashlib
import memcache

from PyBook.models import Book
reload(sys)
sys.setdefaultencoding('utf8')


def gethotbooks(tag):
    result = []
    result_distinct = []
    count = 0
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    s = requests.session()
    while True:
        lastlen = len(result)
        #tag = quote(tag)
        response = s.get("https://book.douban.com/tag/"+tag+"?start="+str(count*20)+"&type=T", headers=headers)
        if response.status_code == 403:
            print "我擦， 被禁了"
            break
        html_doc = response.text

        soup = BeautifulSoup(html_doc, "html.parser")

        li_list = soup.find_all("li", class_="subject-item")
        for li in li_list:
            book = {}
            title = ""
            for title_part in li.find("div", class_="info").h2.a.stripped_strings:
                title += title_part
            book["title"] = title

            img = li.find("div", class_="pic").a.img["src"]
            book["img"] = img

            rating_tag = li.find("div", class_="star clearfix").find("span", class_="rating_nums")
            if rating_tag is None:
                rating = "-0.0"
            else:
                rating = rating_tag.string
            book["rating"] = rating

            rating_amount = li.find("div", class_="star clearfix").find("span", class_="pl").string.strip()
            book["rating_amount"] = rating_amount

            book["tag"] = tag
            result.append(book)

        if len(result) == lastlen:
            break
        count += 1
    # result去重
    for item in result:
        if item not in result_distinct:
            result_distinct.append(item)

    books = []
    for book in result_distinct:
        my_book = Book(title=book['title'], img=book['img'], rating=book['rating'],
                       rating_amount=book['rating_amount'], tag=book['tag'])
        books.append(my_book)
    Book.objects.bulk_create(books)

def output(books):
    html_parser = HTMLParser.HTMLParser()
    html_doc = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>热门书单</title>
            <!-- 新 Bootstrap 核心 CSS 文件 -->
            <link href="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">
            <!-- 可选的Bootstrap主题文件（一般不使用） -->
            <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/css/bootstrap-theme.min.css"></script>
            <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
            <script src="http://cdn.static.runoob.com/libs/jquery/2.1.1/jquery.min.js"></script>
            <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
            <script src="http://cdn.static.runoob.com/libs/bootstrap/3.3.7/js/bootstrap.min.js"></script>
            <style>
                table th {vertical-align: middle !important; text-align: center; font-size: 20px}
                table td {vertical-align: middle !important; text-align: center; font-family: 楷体; font-size: 18px}
            </style>
        </head>
        <body>
            <nav class="navbar navbar-inverse" role="navigation">
                <div class="container-fluid">
                    <div class="navbar-header">
                        <a class="navbar-brand" href="#">PyStudy | 豆瓣评分最高的20本编程类书籍</a>
                    </div>
                </div>
            </nav>
            <div class="container" style="width: 80%; margin-top:60px; margin-bottom:30px;">
                <table class="table table-condensed table-bordered table-striped">
                    <tr><th>序号</th><th>书名</th><th>图片</th><th>评分</th><th>评价数</th></tr>
                </table>
            </div>
        </body>
    </html>
    """
    soup = BeautifulSoup(html_doc,"html.parser")
    table_tag = soup.body.find("div", class_="container").table
    count = 0
    for book in books:
        tr_tag = "<tr><td>%s</td><td style='width: 40%%'>《%s》</td><td style='width: 20%%'><img src=\"%s\" width=\"90\" /></td><td>%s</td><td>%s</td></tr>" % (count+1, book['title'], book['img'], book['rating'], book['rating_amount'])
        table_tag.append(tr_tag)
        count += 1

    return html_parser.unescape(soup.prettify())


if __name__ == '__main__':
    # if len(sys.argv) < 1:
    #     print 'usage: ' + sys.argv[0] + ' tag [amount]'
    #     exit(0)
    # tag = str(sys.argv[1])
    #
    # tag = tag.decode('GBK').encode('utf-8')
    # amount = int(sys.argv[2])
    # starttime = datetime.datetime.now()
    # books = gethotbooks(tag,amount)
    # output(books)
    # endtime = datetime.datetime.now()
    # output = "总共耗时：" + str((endtime-starttime).seconds) + "秒。"
    # print output
    # print "hello"
    # mc = memcache.Client(['127.0.0.1:12000'], debug=1)
    # mc.set('foo', 'bar')
    # print mc.get('foo')
    # mc.set('dt', {'a':1, 'b':2})
    # print mc.get('dt')
    data = u'你好'
    m = hashlib.md5(data.encode("utf8"))
    print m
    print(m.hexdigest())

