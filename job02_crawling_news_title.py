# 브라우저 열어서 브라우저 기반 타이틀

from selenium import webdriver   ##드라이버 운용
from selenium.common.exceptions import NoSuchFrameException, StaleElementReferenceException #에러종류
import pandas as pd
import re
import time

category = ['Politics', 'Economic', 'Social', 'Culture', 'World', 'It']
pages = [110, 110, 110, 78, 110, 66]  ##페이지수, 너무 높은건 좀 낮춰서 맞춤

url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100#&date=%2000:00:00&page=1'

options = webdriver.ChromeOptions()
options.add_argument('lang=ko_KR') #브라우저 언어설정을 한국어로
options.add_argument('--no-sandbox') #보컬시스템 필요옵션
options.add_argument('--disable-dev-shm-usage') #리눅스
options.add_argument('disable-gpu')
driver = webdriver.Chrome('./chromedriver', options=options) #크롬부라우저를 운영하는 부라우저가 하나 만들어짐
df_titles = pd.DataFrame()

for i in range(0, 6):
    titles = []
    for j in range(1,pages[i]+1):
        url = 'https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=10{}#&date=%2000:00:00&page=1{}'.format(i,j)
        driver.get(url)
        time.sleep(0.2)   # 초단위 슬립  , 머무름 아무것도 안하고

        for k in range(1, 5):
            for l in range(1, 6):
                x_path = '// *[ @ id = "section_body"] / ul[{}] / li[{}] / dl / dt[2] / a'.format(k, l)
                try:
                    title = driver.find_element_by_xpath(x_path).text
                    title = re.compile('[^가-힣 ]').sub('',title)
                    titles.append(title)
                except NoSuchFrameException as e:
                    time.sleep(0.5)
                    try:
                        title = driver.find_element_by_xpath(x_path).text
                        title = re.compile('[^가-힣 ]').sub('',title)
                        titles.append(title)
                    except:
                        print('no such enlement')
                        try:
                            x_path = '// *[ @ id = "section_body"] / ul[{}] / li[{}] / dl / dt / a'.format(k, l)
                            title = re.compile('[^가-힣 ]').sub('', title)
                            titles.append(title)
                        except:
                            print('no such enlement')

                except StaleElementReferenceException as e:
                    print(e)
                    print(category[i], j, 'page', k * l)
                except:
                    print('error')
        if j % 30 == 0: #30으로 나눈 나머지가 0이면
            df_section_titles = pd.DataFrame(titles, columns=['titles'])
            df_section_titles['category'] = category[i]
            df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
            df_titles.to_csv('./crawling_data_{}_{}.csv'.format(category[i], j), index=False)
            titles = []
    df_section_titles = pd.DataFrame(titles, columns=['titles'])
    df_section_titles['category'] = category[i]
    df_titles = pd.concat([df_titles, df_section_titles], ignore_index=True)
    df_titles.to_csv('./crawling_data_{}_{}.csv'.format(category[i, j]), index=False)
    titles = []
driver.close()

# df_titles.to_csv('./crawling_data', index=False)
# driver.get(url)

        #화살표 제목에서 > 카피 > 엑스패스
        # // *[ @ id = "section_body"] / ul[1] / li[1] / dl / dt[2] / a

