# 🚀 Routine Pro – A Smart Teacher Management System

## 📌 Overview
Routine Pro is a web-based AI-powered application designed to help teachers manage lecture schedules, track student attendance, and monitor wellness — all in one place.

---

## ✨ Key Features

### 📅 Lecture Scheduling
- Add and manage lecture tasks
- Set deadlines and priorities
- Track pending work

### 👨‍🏫 Attendance Management
- Add students batch-wise
- Mark daily attendance
- Store attendance history

### 📊 AI Attendance Analytics
- Calculate attendance percentage
- Predict student performance (Good / Average / Poor)

### 🌱 Wellness Tracking
- Log mood and stress level
- Maintain daily journal
- View past entries

### 🤖 AI Stress Prediction (NEW)
- Predicts teacher stress level based on workload
- Displays insights on dashboard

---

## 🧠 Machine Learning Integration

- **Model Used:** Decision Tree Classifier
- **Predictions:**
  - Student performance (based on attendance %)
  - Teacher stress (based on workload)

---

## 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML, CSS, Bootstrap
- **ML Library:** Scikit-learn

---

## 📂 Project Structure

```
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── schedule.html
│   ├── attendance.html
│   ├── report.html
│   ├── wellness.html
├── static/
│   ├── css/
│   ├── images/
```

---

## ▶️ How to Run

1. Clone the repository
```
git clone <your-repo-link>
cd routine-pro
```

2. Install dependencies
```
pip install flask flask_sqlalchemy pandas scikit-learn
```

3. Run the application
```
python app.py
```

4. Open in browser
```
http://127.0.0.1:5000/
```

---

## 📈 Future Enhancements

- Login & authentication system
- Role-based dashboard
- Graphical analytics (charts)
- Cloud deployment (Render / AWS)
- Mobile responsiveness

---

## 👨‍💻 Author

Developed by **Leena Vaishnav**

---

## ⭐ Note
This project demonstrates integration of **AI + Web Development**, making it more than just a CRUD application.
