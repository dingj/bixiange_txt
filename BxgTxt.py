import requests
from bs4 import BeautifulSoup
import sys

'抓取笔仙阁小说'


# 头文件
head = {}
head[
    'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36'
# 待抓取小说目录页面
book_url = 'http://www.bixiange.net/xxx/xxx'


def main():
    # 获取书名和目录
    def bookmenu():
        book_html = requests.get(book_url, headers=head)
        book_html.encoding = 'gbk'
        # 创建BeautifulSoup对象
        listmain_soup = BeautifulSoup(book_html.text, 'lxml')
        # 获取书名
        bookname = listmain_soup.find_all('h1')[0].get_text() + '.txt'
        # 获取目录列表
        chapters = listmain_soup.find_all('ul', class_='clearfix')
        download_soup = BeautifulSoup(str(chapters), 'lxml')
        downloadmenu = []
        for link in download_soup.find_all('a'):
            download_url = "http://www.bixiange.net" + link.get('href')
            downloadmenu.append(download_url)
        # 计算章节个数
        numbers = len(downloadmenu)
        return bookname, numbers, downloadmenu

    # 下载章节文本
    def downloader(download_url):
        download_html = requests.get(download_url, headers=head)
        soup_texts = BeautifulSoup(download_html.text, 'lxml')
        texts = soup_texts.find_all(class_='content', id='mycontent')
        txt = str(texts).replace('[<div class="content" id="mycontent">',
                                 '').replace('<br/><br/>', '\n').replace(
                                     '</div>]', '\n')
        return txt

    bookname, numbers, downloadmenu = bookmenu()
    file = open(bookname, 'w', encoding='utf-8')
    index = 1
    for durl in downloadmenu:
        txt = downloader(durl)
        file.write(txt)
        # 计算爬虫进度
        sys.stdout.write("已下载:%.3f%%" % float(index / numbers * 100) + '\r')
        sys.stdout.flush()
        index += 1
    file.close


# 主函数
if __name__ == '__main__':
    main()
