import psycopg2
from flask import Flask, render_template, request, url_for, redirect
import sys
import logging
import time
import datetime

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


country = 'in'          
order = 'video_id DESC'
videoname = ""
channelname = ""
tag = ""

suffix  = 'videos'
gen_attr = 'video_id,title,channel_title,publish_time,description,views,likes,dislikes,tags'
small_attr = 'publish_time,description,views,likes,dislikes,tags'

curr_user = "guest"

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='group_23',
                            user='postgres',
                            password='12345')
    return conn

def createTableforOnce():
    conn = get_db_connection()
    cur = conn.cursor()
    subquery = "((SELECT DISTINCT ON(channel_title)* FROM cavideos) UNION (SELECT DISTINCT ON(channel_title) * FROM frvideos) UNION (SELECT DISTINCT ON(channel_title)* FROM invideos) UNION (SELECT DISTINCT ON(channel_title)* FROM devideos) UNION (SELECT DISTINCT ON(channel_title)* FROM usvideos))"
    cur.execute("CREATE TABLE IF NOT EXISTS history AS (SELECT DISTINCT ON (channel_title) channel_title as curr_user,video_id,channel_title,1 as watched,TRUE as liked,FALSE as disliked FROM "+subquery+" AS TEMP);")

    conn.commit()
    cur.close()
    conn.close()


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

    #app.logger.info(order)

    return country,order



def createSearch(videoname,channelname,tag):
    if videoname==None and channelname==None and tag==None:
        return ""
    search_string = " WHERE "

    if videoname:
        videoname = '\'%' + videoname + '%\''
        search_string += "title LIKE "+videoname + " AND "

    if channelname:
        channelname = '\'%' + channelname + '%\''
        search_string += "channel_title LIKE "+channelname + " AND "

    if tag:
        tag = '\'%' + tag + '%\''
        search_string += "tags LIKE "+tag + " AND "

    search_string = search_string[0:len(search_string)-4]
    return search_string


@app.route('/')
def base():
    global country
    global order
    global videoname
    global channelname
    global tag

    order = 'video_id DESC'
    videoname = ""
    channelname = ""
    tag = ""

    app.logger.info("REACHED HOME")
    app.logger.info(country+','+order)

    return redirect(url_for('index'))

def complete_country(country):

    if country=="ca":
        return "Canada"
    elif country=="de":
        return "Denmark"
    elif country=="fr":
        return "France"
    elif country=="in":
        return "India"
    else:
        return "USA"

@app.route('/index',methods=('GET', 'POST'))
def index():

    global country
    global order
    global videoname
    global channelname
    global tag

    if request.method =='POST':
        videoname = request.form["videoname"]
        channelname = request.form["channelname"]
        tag = request.form["tag"]

    search_string = createSearch(videoname,channelname,tag)    
    
    #app.logger.info(search_string)

    conn = get_db_connection()
    cur = conn.cursor()

    in_country = request.args.get("country")
    in_order = request.args.get("filter")

    country,order = returnOrderCountry(in_country,in_order)

    cur.execute('SELECT '+ gen_attr + ' FROM ' + country+suffix+search_string+' ORDER BY '+order+' LIMIT 50;')
    videos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', videos=videos,country=complete_country(country),
            this_videoname = videoname,this_channelname=channelname,this_tag=tag)


@app.route('/query')
def query():
    conn = get_db_connection()
    cur = conn.cursor()

    temp_videoId = request.args.get("videoid")
    action = request.args.get("selected_event")
    videoId = "'%"+request.args.get("videoid") + "%'"
    channel_title = request.args.get("channel_title")
    page_type = request.args.get("page_type")

    cur.execute("SELECT liked,disliked FROM history WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")
    results = cur.fetchall()

    if len(results)==0:
        cur.execute(f"INSERT INTO history VALUES('{curr_user}','{temp_videoId}','{channel_title}',0,FALSE,FALSE) ON CONFLICT DO NOTHING")
        results = [(False,False)]

    #app.logger.info("\n")
    #app.logger.info(results)
    #app.logger.info("\n")

    update = 0
    if action=='Watch':
        action = "views"
        update = 1
        cur.execute("UPDATE history SET watched = watched + 1 WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")
        
    elif action=='Like' and results[0][1]==False:
        action = "likes"
        update = 1

        if results[0][0]==False:
            app.logger.info("Here")
            cur.execute("UPDATE history SET liked = TRUE WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")
        else:
            update = -1
            cur.execute("UPDATE history SET liked = FALSE WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")

    elif action=='Dislike' and results[0][0]==False:
        action = 'dislikes'
        update = 1

        if results[0][1]==False:
            cur.execute("UPDATE history SET disliked = TRUE WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")
        else:
            update = -1
            cur.execute("UPDATE history SET disliked = FALSE WHERE curr_user LIKE \'%"+curr_user+"%\' AND video_id LIKE "+videoId+";")

    if update!=0:
        cur.execute('UPDATE '+country+suffix+' SET '+action+'='+action+'+ '+str(update)+' WHERE video_id LIKE '+videoId+';')
    
    conn.commit()
    cur.close()
    conn.close()

    app.logger.info("\npage_type:"+str(page_type))

    if page_type=="0":
        return redirect(url_for('index'))
    elif page_type=="1":
        return redirect(url_for('login'))
    elif page_type=="2":
        return redirect(url_for('history'))
    else:
        return redirect(url_for('mypage'))
    
@app.route('/login',methods=('GET', 'POST'))
def login():
    global curr_user
    global country

    account_message = ""

    if request.method =='POST':
        in_user = request.form["username"]
        in_pass = request.form["password"]

        if(in_user!=in_pass and len(in_user)>0):
            account_message = "Invalid Username/Password"
        else:
            account_message = "Account successfully switched to : " + in_user
            curr_user = in_user

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT '+ gen_attr + ' FROM ' + country+suffix+' WHERE channel_title LIKE \'%'+curr_user+'%\' ORDER BY publish_time DESC;')
    videos = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('login.html',username = curr_user,account_message=account_message,videos=videos,country=complete_country(country))


@app.route('/upload',methods=('GET', 'POST'))
def upload():
    global curr_user
    global country

    if request.method =='POST':
        up_country = request.form["country"]
        up_title = request.form["videoname"]
        up_tags = request.form["tags"]
        up_descrip = request.form["description"]
        up_videoID = '!'+str(time.time())
        up_time = str(datetime.datetime.now())
    
        if up_country=="Canada":
            up_country = "ca"
        elif up_country=="Denmark":
            up_country = "de"
        elif up_country=="France":
            up_country = "fr"
        elif up_country=="India":
            up_country = "in"
        elif up_country=="USA":
            up_country = "us"
        else:
            up_country = country

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(f"INSERT INTO {up_country+suffix} VALUES('{up_videoID}','NULL','{up_title}','{curr_user}',NULL,'{up_time}','{up_tags}',0,0,0,0,'NULL',FALSE,FALSE,FALSE,'{up_descrip}') ON CONFLICT DO NOTHING")

        conn.commit()
        cur.close()
        conn.close()
        

    return render_template('upload.html',username=curr_user,country=country)

@app.route('/history')
def history():
    global country
    global curr_user

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT history.video_id,title,history.channel_title,{small_attr},watched,liked,disliked FROM history,{country+suffix} WHERE (history.video_id LIKE {country+suffix}.video_id AND history.curr_user LIKE '%{curr_user}%') ORDER BY watched,publish_time DESC;")
    videos = cur.fetchall()

    app.logger.info(videos)
    cur.close()
    conn.close()

    return render_template('myhistory.html',videos=videos,username=curr_user,title="Your History",personal="True")

@app.route('/mypage')
def mypage():
    global country
    global curr_user

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT DISTINCT temp.video_id,title,temp.channel_title,{small_attr} FROM history,{country+suffix} as temp\
                WHERE (history.curr_user LIKE '%{curr_user}%' AND history.channel_title LIKE temp.channel_title AND temp.channel_title NOT LIKE '%{curr_user}%') \
                ORDER BY publish_time DESC,views DESC,likes DESC LIMIT 50;")
    videos = cur.fetchall()

    app.logger.info(videos)
    cur.close()
    conn.close()

    return render_template('mypage.html',videos=videos,username=curr_user,title="Your Recommendations",personal="False")


if __name__ == '__main__':
    this_time = time.time()
    createTableforOnce();
    print(time.time()-this_time)
    app.debug = True
    app.run()