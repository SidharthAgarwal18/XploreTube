import psycopg2
from flask import Flask, render_template, request, url_for, redirect
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

country = 'in'          #default country is india..
order = 'video_id DESC,'
suffix  = 'videos'
gen_attr = 'video_id,title,channel_title,publish_time,description,views,likes,dislikes'

user = "guest"
videos_watched = []
videos_liked = []
videos_disliked = []

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='group_23',
                            user='postgres',
                            password='12345')
    return conn

def returnOrderCountry(in_country,in_order):
    global order
    global country

    if in_country=="Canada":
        country = "ca"
    elif in_country=="Denmark":
        country = "de"
    elif in_country=="France":
        country = "fr"
    elif in_country=="India":
        country = "in"
    elif in_country=="USA":
        country = "us"

    if order[-1]!=',':
        order += ','

    if in_order=="Most Viewed" and "views" not in order:
        order = "views DESC," + order;
    elif in_order=="Most Viewed":
        order = order.replace("views DESC,","")

    elif in_order=="Most Liked" and "likes" not in order:
        order = "likes DESC," +order;
    elif in_order=="Most Liked":
        order = order.replace("likes DESC,","")

    elif in_order=="Most Comments" and "comment_count" not in order:
        order = "comment_count DESC," +order;
    elif in_order=="Most Comments":
        order = order.replace("comment_count DESC,","")

    elif in_order=="Date of upload" and "publish_time" not in order:
        order = "publish_time DESC," + order;
    elif in_order=="Date of upload":
        order = order.replace("publish_time DESC,","")

    if len(order)>0 and order[-1]==',':
        order = order[0:len(order)-1]
    elif len(order)==0:
        order = "video_id DESC"

    app.logger.info(order)

    return country,order

@app.route('/')
def base():
    return redirect(url_for('index'))

@app.route('/index')
def index():

    global order
    global country

    conn = get_db_connection()
    cur = conn.cursor()

    in_country = request.args.get("country")
    in_order = request.args.get("filter")

    country,order = returnOrderCountry(in_country,in_order)

    cur.execute('SELECT '+ gen_attr + ' FROM ' + country+suffix+' ORDER BY '+order+' LIMIT 50;')
    videos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', videos=videos)


@app.route('/query')
def query():
    conn = get_db_connection()
    cur = conn.cursor()

    action = request.args.get("selected_event")
    videoId = "'%"+request.args.get("videoid") + "%'"

    update = 0
    if action=='Watch':
        action = "views"
        update = 1

        if videoId not in videos_watched:
            videos_watched.append(videoId)
        else:
            update = -1
            videos_watched.remove(videoId)
        
    elif action=='Like' and videoId not in videos_disliked:
        action = "likes"
        update = 1

        if videoId not in videos_liked:
            videos_liked.append(videoId)
        else:
            update = -1
            videos_liked.remove(videoId)

    elif videoId not in videos_liked:
        action = 'dislikes'
        update = 1

        if videoId not in videos_disliked:
            videos_disliked.append(videoId)
        else:
            update = -1
            videos_disliked.remove(videoId)

    if update!=0:
        cur.execute('UPDATE '+country+suffix+' SET '+action+'='+action+'+ '+str(update)+' WHERE video_id LIKE '+videoId+';')
    
    cur.execute('SELECT '+ gen_attr + ' FROM ' + country+suffix+' WHERE video_id LIKE '+videoId+' ORDER BY '+order+' LIMIT 50;')
    videos = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()

    return render_template('index.html', videos=videos)
    

if __name__ == '__main__':
    app.debug = True
    app.run()