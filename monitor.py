import requests, time, sys

def ping(url):
  res = requests.get(url)
  return res.status_code == 200

while True:
  try:
    isOnline = ping(str(sys.argv[1]))
    print(isOnline)
  except:
    print('Offline')
  time.sleep(1)