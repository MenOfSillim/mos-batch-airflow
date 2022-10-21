import random
import requests
import time

from bs4 import BeautifulSoup

url_prefix = 'https://comic.naver.com'
webtoon_creation_url = 'https://comic.naver.com/webtoon/creation'


def do_crawling():
    webtoon = []
    response = request_webtoon_list(webtoon)

    return list(response.pop(0))


def request_webtoon_list(webtoon):
    response = requests.get(webtoon_creation_url)
    if response.status_code == 200:
        i = 0
        finish_soup = BeautifulSoup(response.text, 'html.parser')

        raw_webtoon_list = finish_soup.select('div.thumb > a')  # title칸의 값 모두 긁어오기

        for a in raw_webtoon_list:  # 타이틀 전체를 불러와서 정렬
            if i % 50 == 0:
                time.sleep(random.uniform(1, 3))

            i = i + 1
            url = url_prefix + a['href']
            title = a['title']
            title_id = url.split('=')[1]
            webtoon_dict = {
                'seriesId': title_id,
                'title': title,
                'url': url,
                'platform': 'Naver'
            }
            webtoon_dict.update(request_webtoon_detail(url=url))
            webtoon.append(webtoon_dict)
            if i % 5 == 0:
                print('Index : [%g] ' % i)
            # Test
        return webtoon

        # # 50개까지만 하고 스탑
        # if i == 50:
        #     print(webtoon)
        #     return webtoon


def request_webtoon_detail(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/81.0.4044.141 Safari/537.36",
        "Connection": "close"}
    response = requests.get(headers=headers, url=url)
    response_tag = BeautifulSoup(response.text, 'html.parser')

    thumbnail = response_tag.select_one('div.comicinfo > div.thumb > a > img')['src']
    description = response_tag.select_one('div.comicinfo > div.detail > p:not(.detail_info)').text
    genre = response_tag.select_one('div.comicinfo > div.detail > p.detail_info > span.genre').text
    author = response_tag.select_one('div.comicinfo > div.detail > h2 > span.wrt_nm').text

    # age tag 체크
    check_age_grade = response_tag.find('span', attrs={'class': 'age'})
    age_grade = '전체연령가'
    if check_age_grade is not None:
        age_grade = response_tag.select_one('div.comicinfo > div.detail > p.detail_info > span.age').text

    webtoon_detail_dict = {
        'author': author.strip(),
        'thumbnail': thumbnail,
        'description': description,
        'age_grade': age_grade,
        'genre': genre
    }

    return webtoon_detail_dict

# print(finish_list)
