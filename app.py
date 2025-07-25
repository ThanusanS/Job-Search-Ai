from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# DB Setup
def init_db():
    conn = sqlite3.connect('jobmatcher.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    skills TEXT,
                    cv_text TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# Simulated AI: Suggest Jobs
def generate_job_suggestions(skills):
    suggestions = {
        "Python": ["Backend Developer", "Data Analyst"],
        "JavaScript": ["Frontend Developer", "Full Stack Developer"],
        "SQL": ["Data Engineer", "Database Administrator"],
        "HTML": ["Frontend Developer"],
        "CSS": ["UI Developer", "Frontend Developer"],
        "Java": ["Android Developer", "Software Engineer"]
    }
    result = []
    for skill in skills.split(","):
        skill = skill.strip()
        if skill in suggestions:
            result.extend(suggestions[skill])
    return list(set(result))

# Simulated AI: Cover Letter Generator
def generate_cover_letter(name, job):
    return f"""Dear Hiring Manager,

My name is {name}, and I am writing to express my strong interest in the {job} position at your esteemed organization. With a passion for technology and a solid foundation in software development, I believe I can make a valuable contribution to your team.

Throughout my academic and project experiences, I have developed skills in problem-solving, teamwork, and writing clean, efficient code. I am eager to apply these strengths to real-world challenges and continue growing in a collaborative environment.

What excites me most about this opportunity is the chance to work in a dynamic company where innovation and creativity are valued. I am confident that my enthusiasm and commitment to learning will allow me to thrive in this role.

Thank you for considering my application. I would welcome the opportunity to further discuss how I can contribute to your team.

Best regards,
{name}"""


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["GET","POST"])
def submit():
    name = request.form['name']
    email = request.form['email']
    skills = request.form['skills']
    cv_text = request.form['cv']

    conn = sqlite3.connect('jobmatcher.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email, skills, cv_text) VALUES (?, ?, ?, ?)",
              (name, email, skills, cv_text))
    conn.commit()
    conn.close()

    suggestions = generate_job_suggestions(skills)
    letters = [generate_cover_letter(name, job) for job in suggestions]

    return render_template("results.html", name=name, suggestions=suggestions, letters=letters)

if __name__ == "__main__":
    app.run(debug=True)
