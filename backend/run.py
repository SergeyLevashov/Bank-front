import uvicorn


def main():
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # только локально
        port=9000,         # новый порт, не 8000/8001
        reload=False,      # для надёжности отключим reload
    )


if __name__ == "__main__":
    main()
