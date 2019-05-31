import requests, sqlite3
from bs4 import BeautifulSoup

url = 'https://news.google.com/topics/CAAqJQgKIh9DQkFTRVFvSUwyMHZNR3QwTlRFU0JYcG9MVlJYS0FBUAE?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'

def cleanup(dom):
  title = [tt.getText() for tt in dom.find_all('a', 'DY5T1d')]
  source = [s.getText() for s in dom.find_all('a', class_= 'wEwyrc AVN2gc uQIVzc Sksgp')]
  time = [t.get('datetime') for t in dom.find_all('time', class_='WW6dff uQIVzc Sksgp')]
  return title, source, time

def to_sql(title, source, time):
  conn = sqlite3.connect('1041656_hw1.db')
  conn.execute('''CREATE TABLE IF NOT EXISTS news(title TEXT NOT NULL, source TEXT NOT NULL, time DATETIME);''')

  count = len(title)
  for idx in range(count):
    try:
      conn.execute("""INSERT INTO news (title,source,time) VALUES(?, ?, ?)""", (title[idx], source[idx], time[idx]))
    except IndexError:
      conn.execute("""INSERT INTO news (title,source) VALUES(?, ?)""", (title[idx], source[idx]))

  conn.commit()
  conn.close()

if __name__ == '__main__':
  s = requests.Session()
  req = s.get(url)
  
  dom = BeautifulSoup(req.text, 'html.parser')
  title, source, time = cleanup(dom)
  
  s.close()

  to_sql(title, source, time)