from flask import Flask, render_template, request, redirect, url_for, send_file
import csv
import os

app = Flask(__name__)

# Define the report file name and ensure it is created in the app's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(BASE_DIR, "todo_report.csv")

# In-memory task list
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    if task:
        tasks.append({'task': task, 'status': 'Pending'})
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]['status'] = 'Completed'
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

@app.route('/report')
def generate_report():
    # Generate CSV report
    with open(REPORT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['task', 'status'])
        writer.writeheader()
        writer.writerows(tasks)
    
    # Serve the report file
    return send_file(REPORT_FILE, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
