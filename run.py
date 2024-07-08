from uvicorn import run
from config.config import FASTAPI


def main():
    run(app="api:app", reload=FASTAPI.DEBUG, host=FASTAPI.HOST, port=FASTAPI.PORT)


if __name__ == "__main__":
    main()
