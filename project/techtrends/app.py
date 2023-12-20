import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    app.config["connection_count"] += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT id, created, title, content FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config["connection_count"] = 0

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      logging.debug("post_id %s not exist", post_id)
      return render_template('404.html'), 404
    else:
      logging.debug("get_post: %s", post["title"])
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    logging.debug("about page")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()

            logging.debug("created: %s", title)
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route("/healthz")
def healthz():
    return {"result": "OK - healthy"}

@app.route("/metrics")
def metrics():
    connection = get_db_connection()
    ids = connection.execute("SELECT id FROM posts").fetchall()
    connection.close()
    result = {"db_connection_count": app.config['connection_count'], "post_count": len(ids)}
    return result

# start the application on port 3111
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)s:%(name)s:%(asctime)s  %(message)s')
    app.run(host='0.0.0.0', port='3111')
