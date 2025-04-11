from flask import Flask, request
from db import get_visit_by_id, add_visit, get_all_visits, init_db, format_visit_history
from rendering import format_visit_details, format_welcome_message, format_hello_greeting
from html_utils import to_error_message
from datetime import datetime

app = Flask(__name__)

#beroende av flask, rendering och db
@app.route('/')
def root():
    visit = add_visit(request.remote_addr, request.headers.get('User-Agent', 'unknown'))
    return format_welcome_message(visit)

#kollar visits mellan mellan viss datum- beroende av flask, db
@app.route("/visits")
def visits():
    from_param = request.args.get("from")
    to_param = request.args.get("to")
    history = get_all_visits()

    if from_param:
        try:
            from_dt = datetime.fromisoformat(from_param)
            history = [v for v in history if v["timestamp"] >= from_dt]
        except ValueError:
            return to_error_message("Invalid 'from' date format. Use ISO format (YYYY-MM-DD)."), 400

    if to_param:
        try:
            to_dt = datetime.fromisoformat(to_param)
            history = [v for v in history if v["timestamp"] <= to_dt]
        except ValueError:
            return to_error_message("Invalid 'to' date format. Use ISO format (YYYY-MM-DD)."), 400

    return format_visit_history(history)

#hämtar visit id- beroende av flask, db, rendering
@app.route("/visit/<int:visit_id>")
def visit(visit_id):
    visit = get_visit_by_id(visit_id)
    if visit is None:
        return to_error_message("Visit not found"), 404
    return format_visit_details(visit)

#skickar ett välkomst medddelande med namn -beroende av flask, rendering
@app.route("/hello")
def hello():
    name = request.args.get("name", "").strip()
    return format_hello_greeting(name)

#Skapar en label med imput för namn och skicka knapp som är kopplad till /hello med variabel name- beroende av flask och /hello
@app.route("/hello-form", methods=["GET"])
def hello_form():
    return '''
        <h1>Say Hello</h1>
        <form method="GET" action="/hello">
            <label for="name">Your name:</label><br>
            <input type="text" id="name"><br><br>
            <button type="submit">Say Hello</button>
        </form>
    '''

#initierar db och kör appen på port 5000
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)