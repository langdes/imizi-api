import logging
import os

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer
from sqlalchemy import text

from app.middlewares.access_control import AccessControl
from app.middlewares.trusted_hosts import TrustedHostMiddleware
from config import get_env
from app.db.connection import db
from app.api.user_api import user
from app.api.image_api import image

HTTP_BEARER = HTTPBearer(auto_error=False)

def start_app():
    '''
    app = FastAPI(debug=True)
    env = get_env()     # config 모듈(화일)에서 get_env 를 import 했다.
    db.init_db(app=app, **env.dict())
    # get_session = db.session
    # session = next(get_session)
    # print(session.query(text("select 1")))

    app.add_middleware(AccessControl)
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=env.TRUSTED_HOSTS, except_path=["/"])
    app.include_router(user, prefix="/users", tags=["Users"])
    app.include_router(image, prefix="/images", tags=["Images"], dependencies=[Depends(HTTP_BEARER)])
    '''

    app = FastAPI()
    env = get_env()
    for i in env.__dict__.items():
        print(i)

    # 우측 상단 Edit Configuration 메뉴 > Environment Variables 에 환경변수를 지정해서 아래와 같이 불러올수도 있다.
    print(os.getenv("FASTAPI_ENV"))     # 'prd' 가 출력된다.

    return app


app = start_app()

if __name__ == "__main__":
    uvicorn.run("main:start_app", host="0.0.0.0", port=8000, reload=True, factory=True)
