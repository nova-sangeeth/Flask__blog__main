from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'  #   /// means a relative path, //// means it is a absolute path.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
#creating the database file
db = SQLAlchemy(app)


#models ------ classes
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256),
                      nullable=False)  # this is a required field.
    content = db.Column(db.Text, nullable=False)  # this is a required field.
    author = db.Column(db.String(128), nullable=False, default='N/A')
    date_created = db.Column(db.DateTime,
                             nullable=False,
                             default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post' + str(self.id)


# always add a comma to seperate the content in the dictionary.

# all_posts = [
#     {
#         'title': 'Post 1',
#         'content': 'This is the content of post 1',
#         'author': 'Nova Sangeeth'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'This is the content of post 2'
#     }


# ]
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,
                            content=post_content,
                            author=post_author)
        db.session.add(
            new_post)  # session.add only saves the data for temporary use.
        db.session.commit()  # to save the data always commit the database.
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_created).all()
    return render_template('posts.html', posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)




@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title,
                            content=post_content,
                            author=post_author)
        db.session.add(
            new_post)  # session.add only saves the data for temporary use.
        db.session.commit()  # to save the data always commit the database.
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_created).all()
    return render_template('new_post.html')


if __name__ == "__main__":
    app.run(debug=True)
