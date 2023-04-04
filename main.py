from frames.appcontainer import AppContainer
import time, json, requests, asyncio, os, sys


def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, relative_path)


def startapp():
    app = AppContainer()
    app.title("Color-Drop Bot")
    app.geometry("430x450")
    app.mainloop()


if __name__ == "__main__":
    startapp()
