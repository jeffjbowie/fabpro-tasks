from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
import sqlite3


app = Flask(__name__)
app.secret_key = 'fabpro_A18ADHz!--AZf9104hjap3519AK'


@app.route('/')
def index():

    con = sqlite3.connect('tasks.sqlite')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from tasks")
    rows = cur.fetchall()
    if rows:
        return render_template('view.html', rows=rows)
    else:
        return render_template('no_results.html')


@app.route('/task/create', methods=['get', 'post'])
def create_task():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        # store post details in SQL.
        title = request.form.get('title')
        description = request.form.get('description')
        con = sqlite3.connect('tasks.sqlite')
        cur = con.cursor()
        sql = "INSERT INTO tasks (title,description) VALUES (?,?)"
        cur.execute(sql, (title, description))
        con.commit()
        return redirect(url_for('index'))


@app.route('/task/delete/<int:task_id>')
def delete_task(task_id):
    con = sqlite3.connect('tasks.sqlite')
    cur = con.cursor()
    sql = "DELETE FROM tasks WHERE id = ?"
    cur.execute(sql, (task_id,))
    con.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
