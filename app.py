from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------------
# Database Models
# -------------------------

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'))
    completed = db.Column(db.Integer, default=0)

class Config(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_day = db.Column(db.Integer, default=1)
    end_day = db.Column(db.Integer, default=30)

# -------------------------
# Initialize Database
# -------------------------

with app.app_context():
    db.create_all()

    if Config.query.first() is None:
        db.session.add(Config(start_day=1, end_day=30))
        db.session.commit()

# -------------------------
# Home Page
# -------------------------

@app.route("/", methods=["GET", "POST"])
def index():
    config = Config.query.first()
    days = list(range(config.start_day, config.end_day + 1))
    habits = Habit.query.all()

    if request.method == "POST":
        for habit in habits:
            for day in days:
                checkbox = request.form.get(f"habit_{habit.id}_{day}")
                entry = Entry.query.filter_by(habit_id=habit.id, day=day).first()

                if not entry:
                    entry = Entry(habit_id=habit.id, day=day)

                entry.completed = 1 if checkbox else 0
                db.session.add(entry)

        db.session.commit()
        return redirect(url_for("index"))

    return render_template("index.html", habits=habits, days=days, config=config)

# -------------------------
# Add Habit
# -------------------------

@app.route("/add_habit", methods=["POST"])
def add_habit():
    name = request.form.get("habit_name")
    if name:
        db.session.add(Habit(name=name))
        db.session.commit()
    return redirect(url_for("index"))

# -------------------------
# Delete Habit
# -------------------------

@app.route("/delete_habit/<int:habit_id>")
def delete_habit(habit_id):
    Habit.query.filter_by(id=habit_id).delete()
    Entry.query.filter_by(habit_id=habit_id).delete()
    db.session.commit()
    return redirect(url_for("index"))

# -------------------------
# Update Day Range
# -------------------------

@app.route("/update_range", methods=["POST"])
def update_range():
    start = int(request.form.get("start_day"))
    end = int(request.form.get("end_day"))

    config = Config.query.first()
    config.start_day = start
    config.end_day = end
    db.session.commit()

    return redirect(url_for("index"))

# -------------------------
# Analysis Page
# -------------------------

@app.route("/analysis")
def analysis():
    config = Config.query.first()
    days = list(range(config.start_day, config.end_day + 1))
    habits = Habit.query.all()

    habit_totals = []
    habit_names = []

    daily_totals = []

    for day in days:
        day_total = 0
        for habit in habits:
            entry = Entry.query.filter_by(habit_id=habit.id, day=day).first()
            if entry and entry.completed:
                day_total += 1
        daily_totals.append(day_total)

    for habit in habits:
        total = Entry.query.filter_by(habit_id=habit.id, completed=1).count()
        habit_totals.append(total)
        habit_names.append(habit.name)

    overall_completed = sum(habit_totals)
    total_possible = len(days) * len(habits)

    return render_template(
        "analysis.html",
        days=days,
        daily_totals=daily_totals,
        habit_totals=habit_totals,
        habit_names=habit_names,
        overall_completed=overall_completed,
        total_possible=total_possible
    )

# -------------------------
# Run App
# -------------------------

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)


