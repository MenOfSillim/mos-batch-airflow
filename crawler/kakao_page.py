import multiprocessing
import requests
from multiprocessing import Pool

webtoon_detail_hash = 'GQ6i3oIUv1yffrSpxjRGE'
webtoon_list_url = 'https://page.kakao.com/graphql'
webtoon_detail_url = 'https://page.kakao.com/_next/data/' + webtoon_detail_hash + '/content/%s.json'


def do_paraller_crawler(start, end):
    manager = multiprocessing.Manager()
    cpu_count = multiprocessing.cpu_count()
    webtoon = manager.list()
    pool = Pool(cpu_count)
    response = pool.starmap(request_webtoon_list, [(i,  webtoon) for i in range(start, end)])

    print('============ 결과 ===============')
    return list(response.pop(0))


def request_webtoon_list(index, webtoon):
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}

    page = index + 1
    response = requests.post(url=webtoon_list_url, json={'query': webtoon_list_query % int(page)}, headers=headers)
    if response.status_code == 200:
        content = response.json()
        make_model_items(content, webtoon)

    return webtoon


def make_model_items(content, webtoon):
    items = content['data']['staticLandingGenreSection']['groups'][0]['items']

    for i in items:
        webtoon_dict = {
            'seriesId': i['seriesId'],
            'title': i['title'],
            'age_grade': i['ageGrade'],
            'url': 'https://page.kakao.com/content/%s' % i['seriesId'],
            'platform': 'Kakao-Page'
        }

        res_datail = request_webtoon_detail(webtoon_dict['seriesId'])
        # dictionary 병합
        webtoon_dict.update(res_datail)

        print(webtoon_dict)
        webtoon.append(webtoon_dict)



def request_webtoon_detail(series_id):
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    detail_json = requests.get(url=webtoon_detail_url % series_id, headers=headers).json()
    return make_model_detail(detail_json)


def make_model_detail(detail_json):
    detail_json = detail_json['pageProps']['metaInfo']
    webtoon_dict = {
        'keywords': detail_json['keywords'],
        'description': detail_json['description'],
        'author': detail_json['author'],
        'thumbnail': 'https:' + detail_json['image']
    }
    return webtoon_dict


webtoon_list_query = '''
query staticLandingGenreSection {
  staticLandingGenreSection(sectionId: 10, param: {categoryUid:10,subcategoryUid:"0",sortType:"update",page:%g}) {
      __typename
    ...Section
  }
}

fragment Section on Section {
  __typename
  id
  type
  title
  groups {
    ...Group
    __typename
  }
}

fragment Group on Group {
  __typename
  id
  type
  items {
    __typename
    ...Item
  }
}

fragment Item on Item {
  id
  type
  ...PosterViewItem
}

fragment EventLogFragment on EventLog {
  eventMeta {
    id
    name
    subcategory
    category
    series
    provider
    series_id
    type
    __typename
  }
}


fragment PosterViewItem on PosterViewItem {
  id
  type
  seriesId
  showPlayerIcon
  scheme
  title
  thumbnail
  badgeList
  ageGradeBadge
  subtitleList
  rank
  torosFileHashKey
  torosImgId
  ageGrade
  eventLog {
    ...EventLogFragment
    __typename
  }

}
'''
