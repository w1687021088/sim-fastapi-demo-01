from src import create_app
from settings import app_settings

app = create_app()

if __name__ == '__main__':
    import uvicorn

    # 启动应用
    uvicorn.run(app="main:app", host=app_settings.APP_HOST, port=app_settings.APP_PORT, reload=True)

    # uv run uvicorn main:app --reload

    # uv run python main.py (推荐，可以充分的利用 app_settings 的配置)

    # fastapi dev main.py
