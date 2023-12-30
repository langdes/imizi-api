import os
from os import path
from platform import system
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):   # pydantic 의 BaseSettings 를 상속받아 Settings 클래스 생성
    BASE_DIR: str = path.dirname((path.abspath(__file__)))      # BASE_DIR : 프로젝트의 루트 경로
    LOCAL_MODE: bool = (
        True if system().lower().startswith("darwin") or system().lower().startswith("windows") else False
    )
    app_name: str = "Imizi API"
    TEST_MODE: bool = False

    ALLOW_SITE = ["*"]      # 지금 만들고 있는 것은 API 서버이다. 모두 허용할것인지, 특정 사이트에서 오는 요청만 받을 것인 예) ALLOW_SITE = ["abc.com"]
    TRUSTED_HOSTS = ["*"]   # 특정 호스트의 접근만 허용할것인지 예) TRUSTED_HOSTS = ["11.11.11.11", "app.imizi.app"]
    JWT_ALGORITHM = "HS256"
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "imizi-secret")    # SECRET_KEY를 환경변수 JWT_SECRET 에서 받아와라, 없다면 "imizi-secret" 을 쓰라는 의미
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 1  # one day        # 엑세스 토근의 만료시간 설정
    REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 60  # sixty day

    DB_URL: str = ""
    DB_POOL_RECYCLE: Optional[int] = 900    # 디비의 세션 풀을 900초마 리사이클 하라는 의미
    DB_ECHO: Optional[bool] = True
    DB_POOL_SIZE: Optional[int] = 1
    DB_MAX_OVERFLOW: Optional[int] = 1

    AWS_REGION = "ap-northeast-2"
    AWS_BUCKET_NAME = "fastcampus-imizi"
    AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY", "")
    AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY", "")


class DevSettings(Settings):        # 위 Settings 을 다시 상속받은 DevSettings 클래스 생성. 개발용 서버 세팅인듯하다.
    DB_URL = f"mysql+pymysql://{os.getenv('DB_INFO')}/imizi?charset=utf8mb4"
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10


class TestSettings(Settings):
    TEST_MODE = True
    DB_URL = "mysql+pymysql://imizi_app:imizi_app_dev1@localhost:3306/imz_test?charset=utf8mb4"
    DB_POOL_SIZE = 1
    DB_MAX_OVERFLOW = 0


class ProdSettings(Settings):
    DB_URL = "mysql+pymysql://imizi_app:imizi_app_dev1@localhost:3306/imizi?charset=utf8mb4"
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10


def get_env():
    cfg_cls = dict(
        prd=ProdSettings,
        dev=DevSettings,
        test=TestSettings,
    )
    # os.getenv("FASTAPI_ENV", "dev") : os환경변수에서 'FASTAPI_ENV' 찾아서 가져온다. 만약 없다면 'dev' 를 읽는다.
    # cfg_cls['dev'] 와 같이 cfg_cls 에서 읽어온다. 어떤 서버에 접속할것인지 읽어오는 값으로 보인다.
    # DevSettings 을 읽어와 바로 인스턴스화. class DevSettings 클래스의 DevSettings() 인스턴스화 해준다.
    env = cfg_cls[os.getenv("FASTAPI_ENV", "dev")]()

    return env


settings = get_env()
