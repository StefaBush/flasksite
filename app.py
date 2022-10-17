from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(40), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r' %self.id


@app.route('/') #переход
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/posts') #переход
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>') #переход
def posts_detail(id):
    article = Article.query.get(id)
    return render_template('post_det.html', article=article)

@app.route('/posts/<int:id>/del') #переход
def posts_del(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/posts/<int:id>/upd', methods=['POST', 'GET']) #переход
def post_upd(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title'] #fields
        article.author = request.form['author']
        article.text = request.form['text']

        #article = Article(title=title, author=author, text=text) #object

        try:
            #db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При обновлении статьи произошла ошибка'
    else:
        article = Article.query.get(id)
        return render_template('post_upd.html', article=article)


@app.route('/about') #переход
def about():
    return render_template('about.html')


@app.route('/create-article', methods=['POST', 'GET']) #переход
def create_article():
    if request.method == 'POST':
        title = request.form['title'] #fields
        author = request.form['author']
        text = request.form['text']

        article = Article(title=title, author=author, text=text) #object

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create-article.html')


if __name__ == '__main__':
    app.run(debug=True)