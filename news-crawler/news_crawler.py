import requests
from bs4 import BeautifulSoup # html 파싱을 위한 라이브러리
from datetime import datetime

# 섹션별 ID
SECTION_DICT = {
    "정치":"100",
    "경제":"101",
    "사회":"102",
    "생활/문화":"103",
    "IT/과학":"105",
    "세계":"104"
}

BASE_URL = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1="

HEADERS = {
    "User-Agent": "Mozilla/5.0"  # 요청 차단 방지용 헤더
}

def fetch_headlines_by_section(section_name, section_id):
    url = BASE_URL + section_id
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()  # 오류 발생 시 예외 발생 (404, 500 등)
    soup = BeautifulSoup(response.text, "html.parser") #HTML 파싱

    # 주요 헤드라인 요소 찾기
    items = soup.select("div.cluster_body a[href].cluster_text_headline")
    headlines = [item.get_text(strip=True) for item in items[:5]]

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
        headlines = fetch_headlines_by_section(section, sid)
        result[section] = headlines
        for i, title in enumerate(headlines, 1):
            print(f" {i}.{title}")
        print()

    save_to_file(result)

if __name__ == "__main__":
    main()