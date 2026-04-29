import email

from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime
import bcrypt
from reportlab.pdfgen import canvas
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.units import inch
import uuid

app = Flask(__name__)
app.secret_key = "quiz_secret"


# DATABASE CONNECTION
def db():
    conn = sqlite3.connect("quiz.db")
    conn.row_factory = sqlite3.Row
    return conn


# HOME
@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        con = db()

        con.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed)
        )

        con.commit()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"].encode()

        con = db()

        user = con.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        ).fetchone()

        if user and bcrypt.checkpw(password, user["password"]):

            session["user"] = email

            return redirect("/dashboard")

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    email = session["user"]
    con = db()

    user = con.execute(
        "SELECT name FROM users WHERE email=?",
        (email,)
    ).fetchone()

    results = con.execute(
        "SELECT id, score, date FROM results WHERE email=?",
        (email,)
    ).fetchall()

    scores = [r["score"] for r in results]

    total_attempts = len(scores)
    best_score = max(scores) if scores else 0
    avg_score = round(sum(scores)/len(scores), 2) if scores else 0

    # 🔥 ADD THIS
    streak = calculate_streak(results)

    return render_template(
        "dashboard.html",
        name=user["name"],
        results=results,
        total_attempts=total_attempts,
        best_score=best_score,
        avg_score=avg_score,
        scores=scores,   # 🔥 for chart
        streak=streak    # 🔥 for streak
    )

from datetime import datetime

def calculate_streak(results):
    dates = sorted([r["date"] for r in results], reverse=True)
    streak = 0
    prev = None

    for d in dates:
        d = datetime.strptime(d, "%d-%m-%Y")

        if prev is None:
            streak += 1
        else:
            if (prev - d).days == 1:
                streak += 1
            else:
                break

        prev = d

    return streak
#ajax delete result
from flask import jsonify

# DELETE SINGLE
@app.route("/delete_result/<int:id>", methods=["POST"])
def delete_result(id):

    if "user" not in session:
        return jsonify({"success": False})

    con = db()
    con.execute("DELETE FROM results WHERE id=?", (id,))
    con.commit()

    return jsonify({"success": True})


# DELETE ALL
@app.route("/delete_all_results", methods=["POST"])
def delete_all_results():

    if "user" not in session:
        return jsonify({"success": False})

    email = session["user"]
    con = db()

    con.execute("DELETE FROM results WHERE email=?", (email,))
    con.commit()

    return jsonify({"success": True})



# GET UPDATED STATS
# GET UPDATED STATS (AJAX)
@app.route("/get_stats")
def get_stats():

    if "user" not in session:
        return jsonify({})

    email = session["user"]
    con = db()

    results = con.execute(
        "SELECT score FROM results WHERE email=?",
        (email,)
    ).fetchall()

    scores = [r["score"] for r in results]

    return jsonify({
        "total": len(scores),
        "best": max(scores) if scores else 0,
        "avg": round(sum(scores)/len(scores), 2) if scores else 0
    })

# QUIZ PAGE
@app.route("/quiz")
def quiz():
    con = db()
    all_questions = con.execute("SELECT * FROM questions").fetchall()

    # Pick 10 random questions
    import random
    selected_questions = random.sample(all_questions, 10)

    # Store their IDs in session for reference
    session['quiz_qids'] = [q['id'] for q in selected_questions]

    return render_template("quiz.html", questions=selected_questions)


# SUBMIT QUIZ
@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        return redirect("/login")

    con = db()

    # Get only the 10 question IDs stored in session
    quiz_qids = session.get('quiz_qids', [])
    if not quiz_qids:
        return redirect("/quiz")  # fallback if no quiz session

    # Fetch only these questions
    placeholders = ",".join("?" for _ in quiz_qids)
    query = f"SELECT * FROM questions WHERE id IN ({placeholders})"
    questions = con.execute(query, quiz_qids).fetchall()

    score = 0
    correct = 0
    results = []

    for q in questions:
        qid = str(q['id'])
        user_ans = request.form.get(qid)
        correct_ans = q['answer']

        if user_ans:
            if user_ans == correct_ans:
                score += 1
                correct += 1
                status = "correct"
            else:
                score -= 0.25
                status = "wrong"
        else:
            status = "skipped"

        results.append({
            "question": q['question'],
            "user_ans": user_ans,
            "correct_ans": correct_ans,
            "status": status
        })

    score = max(score, 0)
    total = len(questions)
    percentage = round((correct / total) * 100, 2)

    # Save result in DB etc.
    email = session["user"]
    date = datetime.now().strftime("%d-%m-%Y")
    con.execute(
        "INSERT INTO results(email,score,percentage,date) VALUES(?,?,?,?)",
        (email, score, percentage, date)
    )
    con.commit()

    name = con.execute("SELECT name FROM users WHERE email=?", (email,)).fetchone()["name"]
    certificate = generate_certificate(name, score, percentage) if percentage >= 50 else None

    return render_template(
        "result.html",
        score=score,
        total=total,
        percentage=percentage,
        name=name,
        certificate=certificate,
        results=results
    )
# CERTIFICATE GENERATOR
import uuid
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

def generate_certificate(name, score, percentage):

    cert_id = str(uuid.uuid4())[:8]

    # ensure certificates folder exists
    os.makedirs("certificates", exist_ok=True)

    safe_name = name.replace(" ", "_")
    filename = f"{safe_name}_certificate.pdf"
    filepath = os.path.join("certificates", filename)

    c = canvas.Canvas(filepath, pagesize=landscape(A4))

    width, height = landscape(A4)

    # Background
    c.drawImage("static/images/certificate_bg.jpg", 0, 0, width=width, height=height)


    # Title
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(width/2, height-180, "Certificate of Achievement")

    # Subtitle
    c.setFont("Helvetica", 20)
    c.drawCentredString(width/2, height-240, "This certificate is proudly awarded to")

    # Student Name
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(width/2, height-300, name)

    # Description
    c.setFont("Helvetica", 18)
    c.drawCentredString(width/2, height-350,
        "For successfully completing the Online Aptitude Quiz")

    # Score
    c.drawCentredString(width/2, height-390,
        f"Score: {score}   |   Percentage: {percentage}%")

    # Certificate ID
    c.setFont("Helvetica", 12)
    c.drawString(60, 80, f"Certificate ID: {cert_id}")

    from datetime import datetime
    date = datetime.now().strftime("%d %B %Y")

    c.drawRightString(width-60, 80, f"Date: {date}")

    # Signature
    c.drawImage("static/images/signature.png", width-250, 120, width=180, height=60)
    c.setFont("Helvetica", 14)
    c.drawString(width-230, 100, "Exam Authority")

    c.save()

    return filename
# LEADERBOARD
@app.route("/leaderboard")
def leaderboard():

    con = db()

    players = con.execute("""
        SELECT users.name,
        MAX(results.score) as top,
        MAX(results.date) as date
        FROM results
        JOIN users ON users.email = results.email
        GROUP BY results.email
        ORDER BY top DESC
    """).fetchall()

    return render_template(
        "leaderboard.html",
        players=players
    )


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

#download certificate
from flask import send_from_directory

@app.route("/download/<filename>")
def download_certificate(filename):
    return send_from_directory("certificates", filename, as_attachment=True)

# RUN SERVER
if __name__ == "__main__":

    app.run(debug=True)