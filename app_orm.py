from flask import Flask, request, jsonify, abort
from werkzeug.exceptions import HTTPException
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = Path(__file__).parent

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{BASE_DIR / 'main.db'}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class QuoteModel(db.Model):
    __tablename__ = "quotes"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(32), unique=False)
    text = db.Column(db.String(255), unique=False)

    def __init__(self, author, text):
        self.author = author
        self.text = text

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text
        }


# Обработка ошибок и возврат сообщения в виде JSON
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"message": e.description}), e.code

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

@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    quote = QuoteModel(new_quote["author"], new_quote["text"])
    db.session.add(quote)
    db.session.commit()
    return jsonify(quote.to_dict()), 201

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


if __name__ == "__main__":
    app.run(debug=True)
