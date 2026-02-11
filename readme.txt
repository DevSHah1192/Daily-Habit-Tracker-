
Dynamic Habit Tracker
Full Stack Flask Web Application

PROJECT OVERVIEW

The Dynamic Habit Tracker is a full-stack web application built using Python (Flask) and SQLite. It helps users build discipline through structured daily tracking with flexible date ranges and performance analytics.

The application allows users to create, remove, and manage habits dynamically. Users can define a custom start and end day, making the system adaptable for 7-day, 30-day, or long-term habit cycles.

All habit data is stored persistently using SQLAlchemy ORM with a relational database structure.

FEATURES

• Flexible start day and end day configuration
• Add new habits dynamically
• Remove habits anytime
• Submit daily task completion
• Persistent database storage
• Interactive analytics dashboard
• Line chart (daily completion trend)
• Bar chart (habit-wise totals)
• Pie chart (overall completion rate)
• Accessible on laptop and mobile devices (same WiFi network)

TECH STACK

Backend:

Python

Flask

Flask-SQLAlchemy

SQLite

Frontend:

HTML

CSS

Jinja Templates

Chart.js

HOW TO RUN LOCALLY

Navigate to the project folder:
cd habit-tracker

Install dependencies:
pip install flask flask_sqlalchemy

Run the application:
python app.py

Open in browser:
http://127.0.0.1:5000

To access on mobile (same WiFi):

Change app.run() to:
app.run(host="0.0.0.0", port=5000, debug=True)

Use your laptop's IPv4 address in browser.

PROJECT PURPOSE

This project demonstrates practical knowledge of:

Flask application architecture

SQLAlchemy ORM relationships

Dynamic form handling

Database persistence

Data visualization

Full-stack integration

It focuses on solving a real-world productivity problem by building a structured system for discipline and consistency.

Developer: Dev Shah

Status: Active Development
