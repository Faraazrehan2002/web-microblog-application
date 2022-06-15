import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient 

def create_app():
    app = Flask(__name__)

    client = MongoClient("mongodb+srv://faraaz:msdhoni07@microblog-application.pajpp.mongodb.net/test")
    app.db = client.microblog
    
    @app.route('/', methods = ['POST', 'GET'])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%y-%m-%d")
            app.db.entries.insert_one({"content" : entry_content, "date" : formatted_date})
        
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries = entries_with_date)
    return app

if __name__ == '__main__':
    create_app.run(debug = False, host = '0.0.0.0')