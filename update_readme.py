import os
import urllib.request
import json
from datetime import datetime

# 네이버 API 인증 정보 (자신의 정보로 변경)
client_id = "0YFjpdAFkR_fisp_my1n"
client_secret = "_kDkw7KWaN"

# 검색할 해시태그 리스트
hashtags = [
    "#우리FIS아카데미",
    "#우리FISA",
    "#AI엔지니어링",
    "#K디지털트레이닝",
    "#우리에프아이에스",
    "#글로벌소프트웨어캠퍼스"
]

def search_naver_blog(query):
    """네이버 블로그 검색 API 호출"""
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/blog?query={encText}&display=3"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    
    try:
        response = urllib.request.urlopen(request)
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            return json.loads(response_body.decode('utf-8'))
        else:
            print(f"Error Code: {rescode}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# 각 해시태그 검색 실행
results = {}
for tag in hashtags:
    results[tag] = search_naver_blog(tag)

# README.md 업데이트
readme_content = """# 🚀 실시간 네이버 블로그 검색 결과

이 페이지는 GitHub Actions를 사용하여 **5분마다 자동 갱신**됩니다.

마지막 업데이트: **📅 {}**

---

## 🔍 검색 대상 해시태그
- #우리FIS아카데미
- #우리FISA
- #AI엔지니어링
- #K디지털트레이닝
- #우리에프아이에스
- #글로벌소프트웨어캠퍼스

---

## 📝 최근 블로그 검색 결과
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

for tag, data in results.items():
    if data:
        readme_content += f"\n### 🔹 {tag} 검색 결과\n"
        for item in data['items']:
            readme_content += f"- [{item['title']}]({item['link']})\n"
    else:
        readme_content += f"\n### 🔹 {tag} 검색 결과 없음\n"

# README.md 파일 저장
with open("README.md", "w", encoding="utf-8") as file:
    file.write(readme_content)

print("✅ README.md 업데이트 완료!")
