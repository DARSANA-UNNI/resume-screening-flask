from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "resume_screening_secret"

# ================= SKILL DICTIONARY =================
job_skills = {

    # ================= TECH =================
    "Data Scientist": [
        "python", "machine learning", "sql", "statistics",
        "pandas", "numpy", "data analysis", "visualization"
    ],

    "Web Developer": [
        "html", "css", "javascript", "react",
        "frontend", "backend", "api", "bootstrap"
    ],

    "Software Engineer": [
        "java", "python", "data structures", "algorithms",
        "oops", "git", "problem solving"
    ],

    "Cyber Security Analyst": [
        "cyber security", "network security", "ethical hacking",
        "firewall", "risk analysis", "incident response"
    ],

    "AI Engineer": [
        "artificial intelligence", "deep learning",
        "python", "neural networks", "tensorflow", "pytorch"
    ],

    # ================= HEALTHCARE =================
    "Doctor": [
        "diagnosis", "patient care", "medical knowledge",
        "clinical skills", "healthcare", "treatment"
    ],

    "Nurse": [
        "nursing", "patient care", "medical",
        "emergency care", "healthcare", "communication"
    ],

    "Optometrist": [
        "optometry", "eye care", "vision testing",
        "optical instruments", "patient care"
    ],

    "Pharmacist": [
        "pharmacy", "medicines", "drug safety",
        "prescription", "healthcare"
    ],

    "Physiotherapist": [
        "physiotherapy", "rehabilitation",
        "exercise therapy", "patient recovery"
    ],

    # ================= EDUCATION =================
    "Teacher": [
        "teaching", "lesson planning", "classroom management",
        "assessment", "communication", "subject knowledge"
    ],

    "Professor": [
        "research", "teaching", "academic writing",
        "mentoring", "curriculum development"
    ],

    "School Counselor": [
        "counseling", "student guidance",
        "psychology", "communication", "career guidance"
    ],

    # ================= COMMERCE & BUSINESS =================
    "Accountant": [
        "accounting", "finance", "taxation",
        "tally", "auditing", "bookkeeping"
    ],

    "Business Analyst": [
        "business analysis", "excel", "sql",
        "data analysis", "documentation"
    ],

    "Marketing Executive": [
        "marketing", "seo", "digital marketing",
        "branding", "content creation", "analytics"
    ],

    "Sales Executive": [
        "sales", "negotiation", "customer handling",
        "communication", "lead generation"
    ],

    "Human Resource Manager": [
        "recruitment", "hr policies", "employee engagement",
        "training", "performance management"
    ],

    "Banking Professional": [
        "banking", "finance", "customer service",
        "risk management", "compliance"
    ],

    # ================= CREATIVE =================
    "Graphic Designer": [
        "photoshop", "illustrator", "creativity",
        "visual design", "branding"
    ],

    "UI/UX Designer": [
        "ui design", "ux research", "wireframing",
        "prototyping", "figma", "user experience"
    ],

    "Content Writer": [
        "writing", "content creation", "seo",
        "blogging", "editing", "research"
    ],

    # ================= LAW & MEDIA =================
    "Lawyer": [
        "legal research", "advocacy",
        "legal drafting", "case analysis"
    ],

    "Journalist": [
        "reporting", "news writing",
        "research", "communication", "ethics"
    ],

    # ================= ENGINEERING =================
    "Architect": [
        "autocad", "design", "planning",
        "construction", "3d modeling"
    ],

    "Civil Engineer": [
        "construction", "structural design",
        "project management", "site supervision"
    ],

    "Mechanical Engineer": [
        "mechanical design", "manufacturing",
        "thermodynamics", "maintenance"
    ],

    "Electrical Engineer": [
        "electrical systems", "circuit design",
        "power systems", "maintenance"
    ],

    # ================= GOVERNMENT =================
    "Government Officer": [
        "administration", "public service",
        "policy implementation", "communication"
    ],

    "Police Officer": [
        "law enforcement", "public safety",
        "investigation", "discipline"
    ],

    "Defence Personnel": [
        "discipline", "leadership",
        "physical fitness", "strategy"
    ]
}

# ================= CSV (CLOUD SAFE) =================
DATA_FILE = "/tmp/data.csv"

COLUMNS = [
    "skills", "education", "experience",
    "projects", "job_role", "score"
]

if not os.path.exists(DATA_FILE):
    pd.DataFrame(columns=COLUMNS).to_csv(DATA_FILE, index=False)

# ================= LOGIC =================
def calculate_match(text, role):
    skills = job_skills.get(role, [])
    matched = [s for s in skills if s in text]
    score = (len(matched) / len(skills)) * 100 if skills else 0
    return round(score, 2), matched

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":

        if not request.form.get("consent"):
            flash("Please read and accept the note before submitting.")
            return redirect(url_for("index"))

        skills = request.form["skills"].lower()
        education = request.form["education"].lower()
        experience = request.form["experience"]
        projects = request.form["projects"]
        job_role = request.form["job_role"]

        combined_text = skills + " " + education
        score, matched = calculate_match(combined_text, job_role)

        df = pd.read_csv(DATA_FILE)
        df.loc[len(df)] = [
            skills, education, experience,
            projects, job_role, score
        ]
        df.to_csv(DATA_FILE, index=False)

        status = (
            "✅ Good Match" if score >= 70 else
            "⚠️ Partial Match" if score >= 40 else
            "❌ Not Suitable"
        )

        result = {
            "score": score,
            "status": status,
            "matched": matched,
            "projects": projects
        }

        flash("Your response has been submitted successfully!")

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run()
