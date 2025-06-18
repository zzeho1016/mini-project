from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

SECTION_DICT = {
    "정치":"100",
    "경제":"101",
    "사회":"102",
    "생활/문화":"103",
    "IT/과학":"105",
    "세계":"104"
}

def fetch_with_selenium(section_id):
    url = f"https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1={section_id}"
    
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("disable-gpu")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)

    time.sleep(2) # 로딩대기

    elements = driver.find_elements(By.CSS_SELECTOR, "strong.sa_text_strong")
    headlines = [el.text for el in elements[:5]]
    driver.quit()
    return headlines

def save_to_file(result_dict):
    today = datetime.now().strftime("%Y%m%d")
    filename = f"naver_news_sections_{today}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        for idx, (section, headlines) in enumerate(result_dict.items(), 1):
            f.write(f"{idx}. {section}\n")
            for title in headlines:
                f.write(f" - {title}\n")
            f.write("\n")

    print(f"\n 뉴스가 {filename} 파일로 저장되었습니다.")

def main():
    print("네이버 섹션별 헤드랑니 수집 중 ... \n")
    result = {}

    for section, sid in SECTION_DICT.items():
        print(f"[{section}]")
        headlines = fetch_with_selenium(sid)
        result[section] = headlines
        for i, title in enumerate(headlines, 1):
            print(f" {i}.{title}")
        print()

    save_to_file(result)

if __name__ == "__main__":
    main()