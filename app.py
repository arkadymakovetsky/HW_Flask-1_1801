from flask import Flask, request, jsonify, abort
from pathlib import Path
from werkzeug.exceptions import HTTPException
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

BASE_DIR = Path(__file__).parent

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'quotes.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AuthorModel(db.Model):
    __tablename__ = "authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    quotes = db.relationship('QuoteModel', backref='author', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class QuoteModel(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    #author = db.Column(db.String(32), unique=False)
    author_id = db.Column(db.Integer, db.ForeignKey(AuthorModel.id))
    text = db.Column(db.String(255), unique=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, author, text, rating=1):
        self.author_id = author.id
        self.text = text
        self.rating = rating

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author.to_dict(),
            "text": self.text,
            "rating": self.rating
        }

# Обработка ошибок и возврат сообщения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code


# Resource: Author

@app.route("/authors")
def get_all_authors():
    authors = AuthorModel.query.all()
    return jsonify([author.to_dict() for author in authors]), 200

@app.route("/authors/<int:author_id>")
def get_author_by_id(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404, f"Author with id={author_id} not found")
    return jsonify(author.to_dict()), 200

@app.route("/authors", methods=["POST"])
def create_author():
    author_data = request.json
    author = AuthorModel(author_data["name"])
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_dict()), 201

@app.route("/authors/<int:author_id>", methods=["PUT"])
def edit_author(author_id):
    new_author = request.json
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404, f"Author with id={author_id} not found")
    for key, value in new_author.items():
        setattr(author, key, value)
    db.session.commit()
    return jsonify(author.to_dict()), 200    

@app.route("/authors/<int:author_id>", methods=["DELETE"])
def delete_author(author_id):
    author = AuthorModel.query.get(author_id)
    if author is None:
        abort(404, f"Author with id={author_id} not found")
    db.session.delete(author)
    db.session.commit()
    return jsonify({"message": f"Author with id={author_id} has deleted"}), 200    

@app.route("/authors/<int:author_id>/quotes", methods=["POST"])
def create_quote(author_id):
   author = AuthorModel.query.get(author_id)
   new_quote = request.json
   quote = QuoteModel(author, **new_quote)
   db.session.add(quote)
   db.session.commit()
   return quote.to_dict(), 201

# Resource: Quote

# Сериализация list[quotes] --> list[dict] --> str(JSON)
@app.route("/quotes")
def get_all_quotes():
    quotes = QuoteModel.query.all()
    return jsonify([quote.to_dict() for quote in quotes]), 200

# /quotes/1
# /quotes/3
# /quotes/5
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404, f"Quote with id={quote_id} not found")
    return jsonify(quote.to_dict()), 200

# @app.route("/quotes", methods=['POST'])
# def create_quote():
#     new_quote = request.json
#     quote = QuoteModel(**new_quote)
#     db.session.add(quote)
#     db.session.commit()
#     return jsonify(quote.to_dict()), 201

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def edit_quote(quote_id):
    new_quote = request.json
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404, f"Quote with id={quote_id} not found")
    #quote.text = new_quote["text"]
    for key, value in new_quote.items():
        setattr(quote, key, value)
    db.session.commit()
    return jsonify(quote.to_dict()), 200

@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def delete_quote(quote_id):
    quote = QuoteModel.query.get(quote_id)
    if quote is None:
        abort(404, f"Quote with id={quote_id} not found")
    db.session.delete(quote)
    db.session.commit()
    return jsonify({"message": f"Quote with id={quote_id} has deleted"}), 200
    
@app.route("/quotes/filter")
def get_quotes_by_filter():
    kwargs = request.args
    quotes = QuoteModel.query.filter_by(**kwargs).all()
    return jsonify([quote.to_dict() for quote in quotes]), 200

if __name__ == "__main__":
    app.run(debug=True)
