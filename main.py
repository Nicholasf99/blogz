from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:espn99@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
app.secret_key = 'fjity4i3fjejfjdt'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/newpost')
def display():
    return render_template('newpost.html')

@app.route('/newpost', methods=['POST'])
def validate():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        title_error = ''
        body_error = ''

        if int(len(title)) <= 0:
            title_error = 'Please fill in the title'
    
        if int(len(body)) <= 0:
            body_error = 'Please fill in the body'

        if title_error or body_error:
            return render_template('newpost.html', title_error=title_error, body_error=body_error,
            title=title, body=body)
        else:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blogpost/' + str(new_blog.id))

@app.route('/blog')
def index():

    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route('/blogpost/<int:blog_id>')
def blog(blog_id):
    blogId = blog_id
    
    blogpost = Blog.query.filter(Blog.id == blogId).first()
    return render_template('blogpost.html', blogpost=blogpost)

   


if __name__ == '__main__':
    app.run()