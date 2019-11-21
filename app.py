from flask import Flask,render_template

app = Flask(__name__)

# always add a comma to seperate the content in the dictionary. 
all_posts = [
    {
        'title': 'Post 1',
        'content': 'This is the content of post 1',
        'author': 'Nova Sangeeth'
        
    },
    {
        'title': 'Post 2',
        'content': 'This is the content of post 2'
    }

]
@app.route('/')

def home():
    return render_template('index.html')


@app.route('/posts')
def posts():
    return render_template('posts.html' ,posts = all_posts)

if __name__ == "__main__":
    app.run(debug=True) 