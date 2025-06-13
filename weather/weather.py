import os
import requests
import urllib.parse
from dotenv import load_dotenv

# .env 파일에서 API 키 로드
load_dotenv()
API_KEY = os.getenv("OPENAPI_WEATHER_KEY")

def get_weather(city_name):
    city_name_encoded = urllib.parse.quote(city_name)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name_encoded}&appid={API_KEY}&units=metric&lang=kr"
    
    print("요청URL:", url)
    try:
        response = requests.get(url)
        response.raise_for_status() # 에러 발생시 예외 발생
        data = response.json()

        print(f"📍 도시: {data['name']}")
        print(f"현재 온도: {data['main']['temp']}°C")
        print(f"습도: {data['main']['humidity']}%")
        print(f"날씨: {data['weather'][0]['description']}")
        print(f"풍속:{data['wind']['speed']}m/s")

    except requests.exceptions.HTTPError as errh:
        print(f"[오류] HTTP 에러 발생: {errh}")
        print("응답코드",response.status_code)
        print("응답내용:", response.text)
    except requests.exceptions.RequestException as err:
        print(f"[오류] 요청 실패: {err}")
    except KeyError:
        print("[오류] 도시 정보를 불러오는데 실패했습니다.")

# 예시 실행
if __name__ == "__main__":
    print("API_KEY:", API_KEY)
    city = input("날씨를 확인할 도시명을 입력하세요:")
    get_weather(city)