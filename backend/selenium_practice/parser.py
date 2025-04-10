import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import django
import datetime
from bs4 import BeautifulSoup

# 콘솔 출력 인코딩을 UTF-8로 변경
sys.stdout.reconfigure(encoding="utf-8")

# 현재 파일이 있는 폴더 (parser.py가 위치한 곳)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Django 프로젝트의 최상위 폴더(SELENIUM/)를 sys.path에 추가
sys.path.append(BASE_DIR)

# Django 프로젝트 설정 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selenium_practice.settings")
django.setup()

# 이제 Django ORM 사용 가능!
from articles.models import Article

# Chrome 웹 브라우저 옵션 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# 크롬 드라이버로 원하는 url 접속
want_day = ""
if want_day:
    driver.get(f"https://m.entertain.naver.com/ranking?rankingDate={want_day}")
    time.sleep(2)
else:
    driver.get(f"https://m.entertain.naver.com/ranking")

# 스크래핑
for i in range(4):
    print(f"{i+1}번째 기사 스크래핑중...")

    articles = driver.find_elements(By.CLASS_NAME, "NewsItem_news_item__fhEmd")
    # i 번째 기사 클릭
    article_link = articles[i].find_element(By.TAG_NAME, "a")
    # article_link.click()
    driver.execute_script("arguments[0].scrollIntoView(true);", article_link)
    time.sleep(1)
    driver.execute_script("arguments[0].click();", article_link)
    time.sleep(2)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

    # 최대 10초 대기하면서 title text 로 가져오기
    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "NewsEndMain_article_title__kqEzS")
        )
    )
    title = title_element.text
    print(f"제목 : {title}")

    # 날짜 돌린 일자로 자동 저장 
    if want_day:
        date = datetime.datetime.strptime(want_day, "%Y%m%d")
        weekday = date.strftime("%A")  
        
    # 본문과 이미지를 순서대로 저장할 리스트
    content_list = []

    try:
        # 기사 본문 가져오기
        article_content = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_article_content"))
        )

        # JavaScript를 사용하여 전체 HTML 가져오기
        full_html = driver.execute_script(
            "return arguments[0].outerHTML;", article_content
        )
        soup = BeautifulSoup(full_html, "html.parser")

        # JavaScript로 모든 이미지 src 가져오기
        img_tags = driver.execute_script(
            "return Array.from(document.querySelectorAll('._article_content img')).map(img => img.src);"
        )

        # 첫 번째 이미지를 썸네일로 저장
        thumbnail = img_tags[0] if img_tags else ""

        for elem in soup.descendants:  # `descendants` 사용
            if isinstance(elem, str):  # 순수 텍스트 (HTML 태그가 아님)
                text = elem.strip()
                if text:
                    content_list.append(text)

            elif elem.name == "img":  # 직접 img 태그인 경우
                content_list.append(elem["src"])

    except Exception as e:
        print("오류 발생:", e)

    print(f"썸네일 : {thumbnail}")
    print(" ")

    # 데이터베이스에 저장
    if want_day:
        Article.objects.create(title=title, content=content_list, thumbnail=thumbnail, day_of_week_category=weekday)
    else:
        Article.objects.create(title=title, content=content_list, thumbnail=thumbnail)


    # 뒤로가기 실행하여 이전 페이지로 돌아감
    driver.execute_script("window.history.go(-1)")
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )

# 크롬 드라이버 창 닫기
driver.quit()
