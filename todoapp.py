from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://neondb_owner:npg_Rzfr7dbC8qPM@ep-super-shape-a4mzgvjn.us-east-1.aws.neon.tech/neondb?sslmode=require'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Before first request function to create the database tables
def before_first_request():
    db.create_all()  # This will create the tables for the Todo app

# Define the Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.task}>'

@app.route('/')
def index():
    todos = Todo.query.all()  # Ensure you're passing todos to the template
    return render_template("index.html", todos=todos)

@app.route("/add", methods=["POST"])
def add():
    todo = request.form['todo']
    new_todo = Todo(task=todo, done=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    todo = Todo.query.get_or_404(id)
    if request.method == "POST":
        todo.task = request.form['todo']
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", todo=todo, id = id)

@app.route("/check/<int:id>")
def check(id):
    todo = Todo.query.get_or_404(id)
    todo.done = not todo.done
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
