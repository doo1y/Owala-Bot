from frames.appcontainer import AppContainer
import time, json, requests

session = requests.session()

app = AppContainer(session)
app.title("Color-Drop Bot")
app.geometry("430x450")
app.mainloop()
