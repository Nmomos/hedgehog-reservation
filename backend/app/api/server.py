from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import config, tasks # 追加
from app.api.routes import router as api_router

def get_application():
    app = FastAPI(title=config.PROJECT_NAME, version=config.VERSION) # 変更

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_event_handler("startup", tasks.create_start_app_handler(app)) # 追加
    app.add_event_handler("shutdown", tasks.create_stop_app_handler(app)) # 追加

    app.include_router(api_router, prefix="/api")

    return app

app = get_application()
