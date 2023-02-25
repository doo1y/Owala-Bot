from frames.appcontainer import AppContainer
import time, json, requests, asyncio


def startapp():
    app = AppContainer()
    app.title("Color-Drop Bot")
    app.geometry("430x450")
    app.mainloop()


startapp()
