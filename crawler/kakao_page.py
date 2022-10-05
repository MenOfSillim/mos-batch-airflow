import json
import requests


webtoon_list_url = 'https://page.kakao.com/graphql'
webtoon_detail_url = 'https://page.kakao.com/_next/data/H-ip4riNzjfxJZlOz0pd2/content/%s.json'


def request_webtoon_list():
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    response = requests.post(url=webtoon_list_url, json={'query': webtoon_list_query % 1}, headers=headers)
    print("response status code: ", response.status_code)
    if response.status_code == 200:
        print("response : ", response.encoding)
        print("response : ", response.content.decode('utf-8', 'replace'))


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