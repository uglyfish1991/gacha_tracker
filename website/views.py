from flask import Flask, Blueprint, render_template, request, redirect, url_for
from .models import Todo
from . import db
# import matplotlib
# matplotlib.use("Agg")
# import matplotlib.pyplot as plt


my_view = Blueprint("my_view", __name__)

@my_view.route("/")
def home():
    todo_list = Todo.query.all()
    complete = Todo.query.filter_by(complete=True).all()
    not_complete = Todo.query.filter_by(complete=False).all()
    print(todo_list)
    message = request.args.get('message', None)
    # plt.style.use('ggplot')

    # plt.bar(["Complete", "Not Complete"],[len(complete), len(not_complete)])
    # plt.title("Completed Tasks")
    # plt.xlabel("Status")
    # plt.ylabel("Amount")
    # plt.savefig('website/static/images/main_plot.png')
    # plt.clf()
    return render_template("index.html", todo_list = todo_list, message = message)

@my_view.route("/complete")
def complete():
    todo_list = Todo.query.filter_by(complete=True).all()
    print(todo_list)
    message = request.args.get('message', None)
    return render_template("index.html", todo_list = todo_list, message = message)

@my_view.route("/add", methods=["POST"])
def add():
    try:
        task = request.form.get("task")
        new_todo=Todo(task=task)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('my_view.home'))
    except:
        # let them know there was an error
        message = "There was an error adding your task"
        # take them back to the homepage to try again
        return redirect(url_for('my_view.home', message=message))

@my_view.route("/update/<todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("my_view.home"))


@my_view.route("/delete/<todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("my_view.home"))