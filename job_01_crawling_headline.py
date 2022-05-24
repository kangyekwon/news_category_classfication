# 환경 조성 먼저. 여기 프로젝트만에 환경 >보통 다 아나콘다 (환경 조성등만). 패키지 설치등은 pip 인스톨진행.
# pip인스톨 안될경우 > 셋팅 > 툴 > cmd로 설정 현재환경

# 1. numpy를 가장먼저 , 넘피에 맞는 패키지들이 깔리도록 pip install numpy==1.20.2
# 2. matplotlib
# 3. tensorflow
# 4. bs4
# 5. pandas

from bs4 import BeautifulSoup #문서에서 뭐 뽑을때, 필요한 태그만 긁기
import requests # 뭐가져올때
import re  ##자연어처리 . 한글만 남기기
import pandas as pd
import datetime #날짜 가져오기

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'It']

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
# url = https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101

 #크롤링(리쉐스트) 아니다고 증명, 유저라는걸 > 스샷
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36'}
# resp = requests.get(url, headers = headers)  #requests.get.url 하면 싹 가져옴  #\
# # print(resp)
# # print(list(resp))
# # print(type(resp))

# soup = BeautifulSoup(resp.text, 'html.parser')
# print(soup)
df_titles= pd.DataFrame()
for i in range(6):
    url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}'.format(i)
    resp = requests.get(url, headers=headers)  # requests.get.url 하면 싹 가져옴  #\
    # print(resp)
    # print(list(resp))
    # print(type(resp))
    soup = BeautifulSoup(resp.text, 'html.parser')
    # print(soup)

    title_tags = soup.select('.cluster_text_headline') #제목만 긁어오기 #클래스가 적용된 모든것
    print(title_tags[0].text) ## 제목만 나오게하기 #태그그대로 가져오니깐 텍스트

    #태그에서 하나씩 빼오기
    titles=[]  #여기서 리셋
    for title_tag in title_tags:    #^가-힣  정규표현식
        title = re.compile('[^가-힣 ]').sub('',title_tag.text) #모든한글과 띄어쓰기 , ^:제외한다 . sub는 뺸다 (타이틀태그에서),그자리에 '' 추가
        titles.append(title)  # 자연어처리 : 비정형 데이터 중에 ,  ",/ 문장부호들 제거, (학습에 도움이 안됨) 어절 등 단어 나누기. 어학을 알아야함 .형태소 단위로 짤라야함 분류
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], axis='rows',
                          ignore_index=True)

print(df_titles.head())
df_titles.info()
print(df_titles['category'].value_counts())
df_titles.to_csv('./crawling_data/naver_headline_news.csv'.format(
    datetime.datetime.now().strftime('%Y%m%d')),index=False)
