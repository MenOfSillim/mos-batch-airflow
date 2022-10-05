# import json
# import requests
from datetime import datetime
from crawler.kakao_page import request_webtoon_list
from airflow import DAG
from airflow.operators.python import PythonOperator

from config.database_config import DBHandler

# DAG 설정
dag = DAG(
    dag_id='test_dag',
    start_date=datetime(2022, 9, 17),
    catchup=False,
    tags=['crawling'],
    schedule_interval='@once')

# graphql
# https://intrepidgeeks.com/tutorial/sending-graphql-requests-from-the-command-line-using-curl
# 카카오페이지 :13054개
# https://page.kakao.com/menu/10/screen/14

def send_api(path, method):

    request_webtoon_list()
    # API_HOST = "https://gateway-kw.kakao.com"
    # url = API_HOST + path
    # headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    # body = {
    #     "key1": "value1",
    #     "key2": "value2"
    # }
    #
    # try:
    #     if method == 'GET':
    #         response = requests.get(url, headers=headers)
    #     elif method == 'POST':
    #         response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
    #
    #     # print("response status %r" % response.status_code)
    #     # print("response text %r" % response.text)
    # except Exception as ex:
    #     print(ex)
    # print('한국말 보고싶어')
    # # 이미지는 확장자 webp 붙여야됨
    # # 썸네일 이미지 featuredCharacterImageA
    # # 썸네일 이미지 featuredCharacterImageB
    # resultJson = response.json()
    # sections = resultJson['data']['sections']
    #
    # print(sections[0]['cardGroups'][0]['cards'][0]['content'])
    # # for i in sections:
    # #     print(i)


# https://popcorn16.tistory.com/122


def conn_mongo():
    mongo = DBHandler('crawling', 'webtoon')
    print('=============================== Test ===============================')

    # print(mongo.insert_item_one({"crawler": 1}, 'crawling', 'webtoon'))
    result = mongo.find_item(None)
    for a in result:
        print(a)

    print('=============================== Test ===============================')


def http_call():
    print("2번째")


# DAG Task 작성
send_api = PythonOperator(
    task_id='send_api',
    # python_callable param points to the function you want to run
    python_callable=send_api,
    op_args=['/section/v2/pages/rank', 'GET'],
    # dag param points to the DAG that this task is a part of
    dag=dag
)

http_call = PythonOperator(
    task_id='http_call',
    # python_callable param points to the function you want to run
    python_callable=http_call,
    # dag param points to the DAG that this task is a part of
    dag=dag
)

conn_mongo = PythonOperator(
    task_id='conn_mongo',
    python_callable=conn_mongo,
    dag=dag
)

# send_api >> http_call
conn_mongo


# 탑툰 : 태그 크롤링
# curl 'https://page.kakao.com/graphql' \
# -X POST \
# -H 'content-type: application/json' \
# --data '{"query":"query staticLandingGenreSection($sectionId: ID!, $param: StaticLandingGenreParamInput!) {\n  staticLandingGenreSection(sectionId: $sectionId, param: $param) {\n    ...Section\n    __typename\n  }\n}\n\nfragment Section on Section {\n  id\n  type\n  title\n  ... on DependOnLoggedInSection {\n    loggedInTitle\n    loggedInScheme\n    __typename\n  }\n  ... on SchemeSection {\n    scheme\n    __typename\n  }\n  ... on MetaInfoTypeSection {\n    metaInfoType\n    __typename\n  }\n  ... on TabSection {\n    sectionMainTabList {\n      uid\n      title\n      isSelected\n      scheme\n      additionalString\n      subTabList {\n        uid\n        title\n        isSelected\n        groupId\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  ... on ThemeKeywordSection {\n    themeKeywordList {\n      uid\n      title\n      scheme\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingDayOfWeekSection {\n    isEnd\n    totalCount\n    displayAd {\n      sectionUid\n      bannerUid\n      treviUid\n      momentUid\n      __typename\n    }\n    param {\n      categoryUid\n      businessModel {\n        name\n        param\n        __typename\n      }\n      subcategory {\n        name\n        param\n        __typename\n      }\n      dayTab {\n        name\n        param\n        __typename\n      }\n      page\n      size\n      __typename\n    }\n    businessModelList {\n      name\n      param\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    dayTabList {\n      name\n      param\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingTodayNewSection {\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n        __typename\n      }\n      __typename\n    }\n    categoryTabList {\n      name\n      param\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingTodayUpSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n        __typename\n      }\n      page\n      __typename\n    }\n    categoryTabList {\n      name\n      param\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingRankingSection {\n    isEnd\n    rankingTime\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n        __typename\n      }\n      rankingType {\n        name\n        param\n        __typename\n      }\n      page\n      __typename\n    }\n    categoryTabList {\n      name\n      param\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    rankingTypeList {\n      name\n      param\n      __typename\n    }\n    displayAd {\n      ...DisplayAd\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingGenreSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n        __typename\n      }\n      sortType {\n        name\n        param\n        __typename\n      }\n      page\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    sortTypeList {\n      name\n      param\n      __typename\n    }\n    displayAd {\n      ...DisplayAd\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingFreeSeriesSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      tab {\n        name\n        param\n        __typename\n      }\n      page\n      __typename\n    }\n    tabList {\n      name\n      param\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingEventSection {\n    isEnd\n    totalCount\n    param {\n      categoryUid\n      page\n      __typename\n    }\n    categoryTabList {\n      name\n      param\n      __typename\n    }\n    __typename\n  }\n  ... on StaticLandingOriginalSection {\n    isEnd\n    totalCount\n    originalCount\n    param {\n      categoryUid\n      subcategory {\n        name\n        param\n        __typename\n      }\n      sortType {\n        name\n        param\n        __typename\n      }\n      isComplete\n      page\n      __typename\n    }\n    subcategoryList {\n      name\n      param\n      __typename\n    }\n    sortTypeList {\n      name\n      param\n      __typename\n    }\n    recommendItemList {\n      ...Item\n      __typename\n    }\n    __typename\n  }\n  groups {\n    ...Group\n    __typename\n  }\n}\n\nfragment DisplayAd on DisplayAd {\n  sectionUid\n  bannerUid\n  treviUid\n  momentUid\n}\n\nfragment Item on Item {\n  id\n  type\n  ...BannerItem\n  ...OnAirItem\n  ...CardViewItem\n  ...CleanViewItem\n  ... on DisplayAdItem {\n    displayAd {\n      ...DisplayAd\n      __typename\n    }\n    __typename\n  }\n  ...PosterViewItem\n  ...StrategyViewItem\n  ...SimplePosterViewItem\n  ...ListViewItem\n  ...RankingListViewItem\n  ...NormalListViewItem\n  ...MoreItem\n  ...EventBannerItem\n}\n\nfragment BannerItem on BannerItem {\n  bannerType\n  bannerViewType\n  thumbnail\n  videoUrl\n  badgeList\n  titleImage\n  title\n  metaList\n  caption\n  scheme\n  seriesId\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment EventLogFragment on EventLog {\n  click {\n    layer1\n    layer2\n    setnum\n    ordnum\n    copy\n    imp_id\n    imp_provider\n    __typename\n  }\n  eventMeta {\n    id\n    name\n    subcategory\n    category\n    series\n    provider\n    series_id\n    type\n    __typename\n  }\n  viewimp_contents {\n    type\n    name\n    id\n    imp_area_ordnum\n    imp_id\n    imp_provider\n    imp_type\n    layer1\n    layer2\n    __typename\n  }\n  customProps {\n    landing_path\n    view_type\n    toros_imp_id\n    toros_file_hash_key\n    toros_event_meta_id\n    content_cnt\n    event_series_id\n    event_ticket_type\n    play_url\n    __typename\n  }\n}\n\nfragment OnAirItem on OnAirItem {\n  thumbnail\n  videoUrl\n  titleImage\n  title\n  subtitleList\n  caption\n  scheme\n}\n\nfragment CardViewItem on CardViewItem {\n  title\n  thumbnail\n  titleImage\n  scheme\n  badgeList\n  ageGradeBadge\n  ageGrade\n  torosImgId\n  torosFileHashKey\n  subtitleList\n  caption\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment CleanViewItem on CleanViewItem {\n  id\n  type\n  showPlayerIcon\n  scheme\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  subtitleList\n  rank\n  torosFileHashKey\n  torosImgId\n  ageGrade\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment PosterViewItem on PosterViewItem {\n  id\n  type\n  showPlayerIcon\n  scheme\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  subtitleList\n  rank\n  torosFileHashKey\n  torosImgId\n  ageGrade\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n  seriesId\n}\n\nfragment StrategyViewItem on StrategyViewItem {\n  id\n  title\n  count\n  scheme\n}\n\nfragment SimplePosterViewItem on SimplePosterViewItem {\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  ageGrade\n  scheme\n}\n\nfragment ListViewItem on ListViewItem {\n  id\n  type\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  ageGrade\n  subtitleList\n  descriptionList\n  scheme\n  ageGrade\n  torosImgId\n  torosFileHashKey\n  caption\n  seriesId\n  alarm\n}\n\nfragment RankingListViewItem on RankingListViewItem {\n  title\n  thumbnail\n  badgeList\n  ageGradeBadge\n  ageGrade\n  metaList\n  descriptionList\n  scheme\n  torosImgId\n  torosFileHashKey\n  rank\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment NormalListViewItem on NormalListViewItem {\n  id\n  type\n  ticketUid\n  thumbnail\n  badgeList\n  ageGradeBadge\n  ageGrade\n  isAlaramOn\n  row1\n  row2\n  row3 {\n    id\n    metaList\n    __typename\n  }\n  row4\n  row5\n  scheme\n  continueScheme\n  nextProductScheme\n  continueData {\n    ...ContinueInfoFragment\n    __typename\n  }\n  torosImpId\n  torosFileHashKey\n  seriesId\n  isCheckMode\n  isChecked\n  isReceived\n  showPlayerIcon\n  rank\n  isSingle\n  singleSlideType\n  ageGrade\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n  giftEventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment ContinueInfoFragment on ContinueInfo {\n  title\n  isFree\n  productId\n  lastReadProductId\n  scheme\n  continueProductType\n}\n\nfragment MoreItem on MoreItem {\n  id\n  scheme\n  title\n}\n\nfragment EventBannerItem on EventBannerItem {\n  bannerType\n  thumbnail\n  videoUrl\n  titleImage\n  title\n  subtitleList\n  caption\n  scheme\n  eventLog {\n    ...EventLogFragment\n    __typename\n  }\n}\n\nfragment Group on Group {\n  id\n  ... on ListViewGroup {\n    meta {\n      title\n      count\n      __typename\n    }\n    __typename\n  }\n  type\n  dataKey\n  groups {\n    ...GroupInGroup\n    __typename\n  }\n  items {\n    ...Item\n    __typename\n  }\n}\n\nfragment GroupInGroup on Group {\n  id\n  type\n  dataKey\n  items {\n    ...Item\n    __typename\n  }\n  ... on ListViewGroup {\n    meta {\n      title\n      count\n      __typename\n    }\n    __typename\n  }\n}\n","operationName":"staticLandingGenreSection","variables":{"sectionId":"static-landing-Genre-section-Layout-10-0-update","param":{"categoryUid":10,"subcategoryUid":"0","sortType":"update","page":1}}}'