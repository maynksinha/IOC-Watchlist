import uvicorn

from main import create_app
from app.connections import env_config

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=env_config.HOST,
        port=env_config.PORT,
        reload=not env_config.IS_PROD,
    )
