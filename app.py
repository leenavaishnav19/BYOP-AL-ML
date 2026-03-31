from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import pandas as pd
from sklearn.tree import DecisionTreeClassifier


student_data = pd.DataFrame({
    'attendance': [90, 85, 80, 70, 60, 50, 40, 30],
    'performance': ['Good', 'Good', 'Good', 'Average', 'Average', 'Average', 'Poor', 'Poor']
})

X_student = student_data[['attendance']]
y_student = student_data['performance']

student_model = DecisionTreeClassifier()
student_model.fit(X_student, y_student)

stress_data = pd.DataFrame({
    'lectures': [1, 2, 3, 4, 5, 6, 7],
    'stress': ['Relaxed', 'Relaxed', 'Moderate', 'Moderate', 'Moderate', 'Overloaded', 'Overloaded']
})

X_stress = stress_data[['lectures']]
y_stress = stress_data['stress']

stress_model = DecisionTreeClassifier()
stress_model.fit(X_stress, y_stress)
app = Flask(__name__)
app.secret_key = "saanvi_123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class LectureTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    topic = db.Column(db.String(500), nullable=False)
    batch = db.Column(db.String(50), nullable=False) 
    deadline = db.Column(db.Date, nullable=False)
    priority = db.Column(db.Integer, default=3)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    batch = db.Column(db.String(50), nullable=False)
    attendance_records = db.relationship('Attendance', backref='student', lazy=True)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.now(timezone.utc).date())
    status = db.Column(db.String(10), default="Present")

class Wellness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(100))
    stress_rate = db.Column(db.Integer)
    note = db.Column(db.String(500))
    date_created = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


@app.route('/')
def index():
    task_count = LectureTask.query.count()
    latest_wellness = Wellness.query.order_by(Wellness.id.desc()).first()
    stress_level = stress_model.predict([[task_count]])[0]

    return render_template('index.html', task_count=task_count, mood=latest_wellness,  stress_level=stress_level)

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        subject = request.form.get('subject')
        topic = request.form.get('topic')
        batch = request.form.get('batch')
        deadline_str = request.form.get('deadline')
        priority = request.form.get('priority')

        from datetime import datetime
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d').date()

        
        new_lecture = LectureTask(subject=subject, topic=topic, batch=batch, deadline=deadline, priority=priority)
        db.session.add(new_lecture)
        db.session.commit()
        flash('Task added to your schedule!', 'success')        
   
        return redirect(url_for('schedule'))
   
    lectures = LectureTask.query.order_by(LectureTask.deadline).all()
    return render_template('schedule.html', lectures=lectures)

@app.route('/delete_task/<int:id>')
def delete_task(id):
    task_to_delete = LectureTask.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('schedule'))
    except:
        return "There was a problem deleting that task"
    
    

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    batches = db.session.query(Student.batch).distinct().all()
    selected_batch = request.args.get('batch')
    students = Student.query.filter_by(batch=selected_batch).all() if selected_batch else []

    if request.method == 'POST':
        date_str = request.form['date']
        lecture_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        present_ids = request.form.getlist('status') 
        
        for student in students:
            status = "Present" if str(student.id) in present_ids else "Absent"
            record = Attendance.query.filter_by(student_id=student.id, date=lecture_date).first()
            if record: record.status = status
            else:
                db.session.add(Attendance(student_id=student.id, date=lecture_date, status=status))
        db.session.commit()
        return redirect(url_for('attendance', batch=selected_batch))

    return render_template('attendance.html', students=students, batches=batches, selected_batch=selected_batch, today=datetime.now().date())


@app.route('/attendance_report')
def attendance_report():
    batches = db.session.query(Student.batch).distinct().all()
    selected_batch = request.args.get('batch')
    if selected_batch:
        students = Student.query.filter_by(batch=selected_batch).all()
    else:
        students = []
    report = []
    
    for student in students:
        total_days = Attendance.query.filter_by(student_id=student.id).count()
        present_days = Attendance.query.filter_by(student_id=student.id, status='Present').count()
        percentage = (present_days / total_days * 100) if total_days > 0 else 0
        performance = student_model.predict([[percentage]])[0]

        report.append({
        'name': student.name,
        'batch': student.batch,
        'percentage': round(percentage, 1),
        'total': total_days,
        'performance': performance
    })
        
        
    return render_template('report.html', report=report, batches=batches, selected_batch=selected_batch)


@app.route('/wellness', methods=['GET', 'POST'])
def wellness():
    if request.method == 'POST':
        new_entry = Wellness(
            mood=request.form['mood'],
            stress_rate=request.form['stress_rate'],
            note=request.form['note']
        )
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for('wellness'))
    
    logs = Wellness.query.order_by(Wellness.date_created.desc()).all()
    return render_template('wellness.html', logs=logs)

@app.route('/add_student', methods=['POST'])
def add_student():
    db.session.add(Student(name=request.form['name'], batch=request.form['batch']))
    db.session.commit()
    return redirect(url_for('attendance', batch=request.form['batch']))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
