import mysql.connector as mc
import os
import werkzeug

from dotenv import load_dotenv
from flask import Flask, render_template, url_for, request, redirect, flash

# Load env variables from `.env` file
load_dotenv()

# Initialize Flask App
app = Flask(__name__)

# Set the secret key
app.secret_key = os.getenv('SECRET_KEY')

# Setup MySQL database
db = mc.connect(
    host='localhost',
    user=os.getenv("MYSQL_USERNAME"),
    password=os.getenv("MYSQL_PASSWORD"),
)
curs = db.cursor(dictionary=True) # curs meaning Cursor
cursE = curs.execute # Just because Im too lazy to type `curs.execute` every single time you know

# Initialize the database and table if it doesn't already exist
cursE('CREATE DATABASE IF NOT EXISTS cs50_final')
cursE('USE cs50_final')
cursE('''CREATE TABLE IF NOT EXISTS `blogs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` text,
  `content` text,
  `draft` tinyint(1) NOT NULL DEFAULT '1',
  `pub_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_mod` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)''')

@app.route("/")
def index():
    banner_img = url_for('static', filename='images/banner.jpg')
    curs.execute("SELECT * FROM blogs WHERE NOT draft ORDER BY pub_date DESC LIMIT 5")
    articles = curs.fetchall()
    return render_template("index.html", banner_img=banner_img, articles=articles, heading="Blog")

@app.route('/posts/post_<post_id>')
def post(post_id):
    cursE(f"SELECT * FROM blogs WHERE id={post_id}")
    article = curs.fetchone()
    banner_img = url_for('static', filename=f"images/banner.jpg")
    return render_template('post.html', article=article, banner_img=banner_img, heading=article['title'])

def construction():
    banner_img = url_for('static', filename="images/construction.jpg")
    return render_template("base.html", banner_img=banner_img, banner_full=True)

@app.route("/archive")
def archive():
    cursE("SELECT * FROM blogs WHERE NOT draft ORDER BY pub_date desc")
    articles = curs.fetchall()
    banner_img = url_for('static', filename='images/archive.jpg')
    return render_template("archive.html", heading='Archive', articles=articles, banner_img=banner_img)

@app.route("/new-post", methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        title = request.form.get('title').replace('\'', '\\\'')
        content = request.form.get('content').replace('\'', '\\\'')
        draft = bool(request.form.get('draft'))

        try:
            cursE(f"INSERT INTO blogs (title, content, draft) VALUES ('{title}', '{content}', {int(draft)})")
        except Exception as e:
            print(e)
            db.rollback()
            flash("Sorry, we couldn't post it")
        else:
            db.commit()
            flash('Post Drafted' if draft else 'Post Published')

        return redirect('/')
    else:
        banner_img = url_for('static', filename="images/banner.jpg")
        return render_template('new-post.html', banner_img=banner_img, heading="New Post")

@app.route('/edit/post_<post_id>', methods=["POST", "GET"])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content').replace('\'', '\\\'')
        draft = bool(request.form.get('draft'))

        try:
            cursE(f"UPDATE blogs set title='{title}', content='{content}', draft={int(draft)} WHERE id={post_id}")
        except Exception as e:
            print(e)
            db.rollback()
            flash("Sorry, we couldn't update it")
        else:
            db.commit()
            flash('Post updated and Drafted' if draft else 'Post Updated')

        return redirect('/')
    else:
        cursE(f"SELECT * FROM blogs WHERE id={post_id}")
        article = curs.fetchone()
        banner_img = url_for('static', filename="images/banner.jpg")
        return render_template('edit_post.html', article=article, banner_img=banner_img)

@app.route('/delete', methods=["POST"])
def delete():
    post_id = request.form.get('id')
    try:
        cursE(f"DELETE FROM blogs WHERE id={post_id}")
    except Exception as e:
        print(e)
        db.rollback()
        flash("Sorry, we couldn't delete it")
    else:
        db.commit()
        flash('Post Deleted')

    return redirect('/')

@app.errorhandler(werkzeug.exceptions.HTTPException)
def page_not_found(e):
    banner_img = url_for('static', filename=f"images/{e.code}.png")
    return render_template("error.html", banner_img=banner_img, banner_full=True), e.code


if __name__=="__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
    db.close()