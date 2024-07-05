from flask import Flask, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])

@app.route('/articles/<int:id>')
def show_article(id):
    article = db.session.get(Article, id)

    if article is None:
        return jsonify({'message': 'Article not found'}), 404

    # Increment page views
    if 'page_views' not in session:
        session['page_views'] = 0
    session['page_views'] += 1

    # Check page view limit
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401

    return jsonify(article.to_dict())

if __name__ == '__main__':
    app.run(port=5555)



