import requests
from bs4 import BeautifulSoup


def do_crawling():
    webtoon_creation_url = 'https://comic.naver.com/webtoon/creation'
    response = requests.get(webtoon_creation_url)
    if response.status_code == 200:
        request_webtoon_list(response)


def request_webtoon_list(response):
    finish_soup = BeautifulSoup(response.text, 'html.parser')

    raw_webtoon_list = finish_soup.select('div.thumb > a')  # title칸의 값 모두 긁어오기

    finish_list = []
    i = 0

    for a in raw_webtoon_list:  # 타이틀 전체를 불러와서 정렬
        i = i + 1
        url = a['href']
        title = a['title']
        title_id = url.split('=')[1]
        webtoon_dict = {
            'seriesId': title_id,
            'title': title,
            'url': url,
            'platform': 'Naver'
        }
        finish_list.append(webtoon_dict)

    print('webtoon count : [%s]' % i)
    # print(finish_list)

