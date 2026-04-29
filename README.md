# 🎯 Online Aptitude Practice Portal

## 📌 Overview

The **Online Aptitude Practice Portal** is a Flask-based web application that allows users to practice aptitude questions in a timed environment. It includes authentication, randomized quizzes, automatic scoring, certificate generation, and a leaderboard system to track user performance.

This project demonstrates full-stack development using Python, Flask, and front-end technologies.

---

## 🚀 Features

* 🔐 **User Authentication**

  * Secure registration and login system using hashed passwords (bcrypt)

* 🧠 **Random Quiz Generation**

  * Each quiz dynamically selects 10 random questions from the database

* ⏱️ **Timer-Based Quiz**

  * Countdown timer implemented using JavaScript

* 📊 **Automatic Result Calculation**

  * Instant score evaluation after quiz submission

* 🏆 **Leaderboard**

  * Displays user rankings based on scores

* 📈 **Progress Tracking**

  * Tracks user performance over time

* 📜 **Certificate Generation**

  * Generates PDF certificates using ReportLab

---

## 🛠️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** SQLite
* **Libraries:**

  * Flask
  * bcrypt
  * reportlab

---

## 📂 Project Structure

```
quiz_portal/
│── app.py                  # Main Flask application
│── init_db.py              # Database initialization
│── import_questions.py     # Script to load questions
│── questions.sql           # SQL file for questions
│── quiz.db                 # SQLite database
│── requirements.txt        # Dependencies
│
├── templates/              # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   ├── result.html
│   ├── leaderboard.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── exam.js
│   ├── images/
│
├── certificates/           # Generated certificates
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**

   ```
   git clone https://github.com/your-username/quiz_portal.git
   ```

2. **Navigate to project folder**

   ```
   cd quiz_portal
   ```

3. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Initialize the database**

   ```
   python init_db.py
   python import_questions.py
   ```

5. **Run the application**

   ```
   python app.py
   ```

6. **Open in browser**

   ```
   http://127.0.0.1:5000/
   ```

---

## 📸 Screenshots

<img width="1257" height="692" alt="image" src="https://github.com/user-attachments/assets/2c4b728f-7e2e-45e9-a8f5-e9c508f255cc" />
<img width="1896" height="908" alt="image" src="https://github.com/user-attachments/assets/c71a2bb8-28c9-40aa-800c-810d6f0dfa9d" />
<img width="1910" height="528" alt="image" src="https://github.com/user-attachments/assets/a0d8f6d3-b3f2-4006-a477-e1d464589242" />
<img width="696" height="496" alt="image" src="https://github.com/user-attachments/assets/a3a2f847-5458-41f6-a965-c99777ea14b1" />


---



## 🔮 Future Improvements

* Admin panel to manage questions
* Multiple quiz categories
* Better UI/UX design
* Timer improvements
* Deployment (Render / Heroku)

---


## 👨‍💻 Author

Developed by Rutuja Patil

---

## 📄 License

This project is open-source and available under the MIT License.
