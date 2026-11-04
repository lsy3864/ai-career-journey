import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("MY_API_KEY")

print(api_key)

if api_key is None:
    raise ValueError("MY_API_KEY가 설정되지 않음")

print(f"키 로드 성공:{api_key[:4]}****")
