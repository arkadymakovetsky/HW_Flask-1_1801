from flask import Flask, request, jsonify
from random import choice


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

RATING_DEF_VALUE = 5

quotes = [
   {
       "id": 3,
       "author": "Rick Cook",
       "text": "Программирование сегодня — это гонка разработчиков программ, стремящихся писать программы с большей и лучшей идиотоустойчивостью, и вселенной, которая пытается создать больше отборных идиотов. Пока вселенная побеждает.",
       "rating": 5,
   },
   {
       "id": 5,
       "author": "Waldi Ravens",
       "text": "Программирование на С похоже на быстрые танцы на только что отполированном полу людей с острыми бритвами в руках.",
       "rating": 5,
   },
   {
       "id": 6,
       "author": "Mosher's Law of Software Engineering",
       "text": "Не волнуйтесь, если что-то не работает. Если бы всё работало, вас бы уволили.",
       "rating": 5,
   },
   {
       "id": 8,
       "author": "Yoggi Berra",
       "text": "В теории, теория и практика неразделимы. На практике это не так.",
       "rating": 5,
   },
   {
       "id": 9,
       "author": "Alex",
       "text": "Quote 1 from Alex.",
       "rating": 5,
   },
   {
       "id": 10,
       "author": "Ivan",
       "text": "Quote 1 from Ivan.",
       "rating": 5,
   },
   {
       "id": 11,
       "author": "Ivan",
       "text": "Quote 2 from Ivan.",
       "rating": 4,
   },
   {
       "id": 12,
       "author": "Ivan",
       "text": "Quote 3 from Ivan.",
       "rating": 5,
   },
   {
       "id": 15,
       "author": "Alex",
       "text": "Quote 2 from Alex.",
       "rating": 3,
   },
]

about_me = {
    "name": "Аркадий",
    "surname": "Маковецкий",
    "email": "arkady@test.ru"
}


@app.route("/")
def hello_world():
   return "Hello, World!"

@app.route("/about")
def about():
    return about_me

# Сериализация list --> str
@app.route("/quotes")
def get_all_quotes():
    return quotes

# /quotes/1
# /quotes/3
# /quotes/5
# /quotes/6
@app.route("/quotes/<int:quote_id>")
def get_quote_by_id(quote_id):
    for quote in quotes:
        if quote["id"] == quote_id:
            return quote, 200
    return f"Quote with id={quote_id} not found", 404

# dict --> str
@app.route("/quotes/random", methods=["GET"])
def random_quote():
    return choice(quotes)

# dict --> str
@app.get("/quotes/count")
def quotes_count():
    return {
        "count": len(quotes)
    }

@app.route("/quotes", methods=['POST'])
def create_quote():
    new_quote = request.json
    new_quote.setdefault("rating", RATING_DEF_VALUE)
    new_id = 1
    if quotes:
        last_quote = quotes[-1]
        new_id = last_quote["id"] + 1
    if new_quote["rating"] > 5:
        new_quote["rating"] = RATING_DEF_VALUE
    new_quote["id"] = new_id
    quotes.append(new_quote)
    return new_quote, 201

@app.route("/quotes/<int:quote_id>", methods=["PUT"])
def edit_quote(quote_id):
    new_quote = request.json
    new_quote.setdefault("rating", RATING_DEF_VALUE)
    for quote in quotes:
        if quote["id"] == quote_id:
            for key in new_quote.keys():
                if key in quote:
                    quote[key] = new_quote[key]
            if quote["rating"] > 5:
                quote["rating"] = RATING_DEF_VALUE
            return quote, 200
    return f"Quote with id={quote_id} not found", 404    

@app.route("/quotes/<int:quote_id>", methods=["DELETE"])
def delete_quote(quote_id):
    for id in range(len(quotes)):
        if quotes[id]["id"] == quote_id:
            del quotes[id]
            return f"Quote with id {quote_id} is deleted.", 200
    return f"Quote with id={quote_id} not found", 404

@app.route("/quotes/filter")
def get_quotes_by_filter():
    args = request.args
    # print(f'{args = }')
    result = []
    # Проходимся по цитатам
    for quote in quotes:
        # True, False, True
        if all(args.get(key, type=type(quote[key])) == quote[key] for key in args):
            result.append(quote)
    return jsonify(result), 200


if __name__ == "__main__":
   app.run(debug=True)