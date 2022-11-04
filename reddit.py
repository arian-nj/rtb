import time
from datetime import datetime
import praw
import sqlite3


con = sqlite3.connect('memes.db')
c = con.cursor()

try:
    c.execute("""CREATE TABLE meme (
    id TEXT,
    tite TEXT,
    score REAL,
    pub INT,
    url TEXT);
   """)
except:
    pass
# WARNING fill thi part
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    user_agent="",
)


sub_list = []
sub_number = []
while True:
    for x in range(0,2):
        for submission in reddit.subreddit(sub_list[x]).hot(limit=sub_number[x]):
            if submission.stickied == False: 
                x = submission.url.split('.')[-1]
                if x=='gif' or x == 'giv' or x=='png' or x== 'jpg':
                    c.execute(f"SELECT * FROM meme WHERE id = '{submission.id}'")
                    if c.fetchall() == []:
                        c.execute("INSERT INTO meme VALUES (?, ?, ?, ?, ?)",(str(submission.id),str(submission.title),int(submission.score),0,str(submission.url)))
                        con.commit()
    print(f"Updated in {datetime.now()}")
    time.sleep(3600)

con.close()
