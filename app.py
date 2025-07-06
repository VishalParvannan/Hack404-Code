from flask import Flask, jsonify, render_template, request, redirect, url_for

app = Flask(__name__)

event_list = [
    {
        "name": "Automations with AI workshop",
        "time": "9:00 PM",
        "location": "MY360"
    },
    {
        "name": "Microhack 5: Web",
        "time": "8:00 PM",
        "location": "MY330"
    },
    {
        "name": "Microhack 4: 3D Modelling",
        "time": "6:00 PM",
        "location": "Main Lobby"
    }
]

announcement_list = [
    {
        "title": "Automations with AI workshop HAPPENING NOW",
        "content": "Join the Nodalli workshop happening now in MY360!"
    },
    {
        "title": "Nodalli workshop!",
        "content": "The Nodalli workshop will be starting in 10 minutes at MY360"
    },
    {
        "title": "Designing Hack404 starting in 2 minutes!",
        "content": "Come to room MY360 to learn about design! Also get a chance to win a $50 Uber Eats gift card!"
    }
]

@app.route("/")
def index():
    return "Gurt Yo"

@app.route("/events", methods=["GET"])
def events():
    return jsonify(event_list)

@app.route("/announcements", methods=["GET"])
def announcements():
    return jsonify(announcement_list)

@app.route("/dashboard", methods=["GET"])
def dashboard():
    return render_template("dashboard.html", events=event_list, announcements=announcement_list)

@app.route("/create_announcement", methods=["GET", "POST"])
def create_announcement():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        if title and content:
            announcement_list.append({
                "title": title,
                "content": content
            })
            return redirect(url_for('dashboard'))  # After creating, go back to dashboard

    return render_template("create_announcement.html")  # Show form if GET
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=8000)