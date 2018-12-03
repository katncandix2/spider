import requests
import csv
from bs4 import BeautifulSoup

def get_one_page(url):
    if len(url) <=0:
        return None

    headers = {
        'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    }

    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        return response.text

    return None

def get_urls(html):
    soup = BeautifulSoup(html,'lxml')

    res = {}
    offset = 0

    for item in soup.find_all('article'):
        curHeader = item.find_all('a')
        curUrl = 'https://tech.meituan.com' + curHeader[0]['href']
        curUserInfo = item.find_all('span')
        urlArray = {}
        urlArray['url']       = curUrl
        urlArray['title']     = curHeader[0].string
        urlArray['userName']  = curUserInfo[0].string
        urlArray['date']      = curUserInfo[1].string
        res[offset] = urlArray
        offset = offset + 1

    return res

def write_to_file(filename,file):

    with open(filename,'a+',encoding='utf-8') as f:
            writer = csv.writer(f)
            #先写入columns_name
            writer.writerow(["标题","作者","日期",'地址'])

            # 写入内容
            for offset in file:
                writer.writerow([
                        file[offset]['title'],
                        file[offset]['userName'],
                        file[offset]['date'],
                        file[offset]['url']
                    ])

def main():
    url = 'https://tech.meituan.com/archives'
    html = get_one_page(url)
    res = get_urls(html)
    write_to_file('data.csv',res)

main()
