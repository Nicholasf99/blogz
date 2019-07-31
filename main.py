from flask import Flask, request, redirect, render_template, session, flash
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

@app.route('/')
def index():

    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():
 

    if request.args.get('id'):
        blog_id = int(request.args.get('id'))
        blog_post = Blog.query.get(blog_id)
        return render_template('blogpage.html', title=blog_post.title, body=blog_post.body)
    else:
        blogs = Blog.query.all()    
        return render_template('blog.html', title='Build a Blog', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost(): 
    

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
                
        if title != "" and body != "":
            blog_post = Blog(title, body)
            db.session.add(blog_post)
            db.session.commit() 
            return render_template('blogpage.html', title=title, body=body)
        
        if title =="":
           flash("Please fill in the title.")
            
        if body =="":
            flash("Please fill in the body.")
            redirect("/blog?id=blog_post.id")
    return render_template('newpost.html', title='Add a Blog Entry')
  
    
        
if __name__ == '__main__':
    app.run()