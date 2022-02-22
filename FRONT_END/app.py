import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

country = 'in'          #default country is india..
suffix  = 'videos'
gen_attr = 'video_id,title,channel_title,publish_time,description,views,likes,dislikes'

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='group_23',
                            user='postgres',
                            password='12345')
    return conn


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT '+ gen_attr + ' FROM ' + country+suffix+' ORDER BY views DESC,likes DESC, dislikes LIMIT 30;')
    videos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', videos=videos)



if __name__ == '__main__':
    app.debug = True
    app.run()