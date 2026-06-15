from flask import Flask, render_template, request
from skills import SKILLS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']

    import PyPDF2

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()

    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    score = (len(found_skills) / len(SKILLS)) * 100

    missing_skills = []

    for skill in SKILLS:

        if skill not in found_skills:

            missing_skills.append(skill)
    suggestions = []

    if "aws" in missing_skills:
        suggestions.append("Learn AWS Cloud Fundamentals")

    if "git" in missing_skills:
        suggestions.append("Create and maintain a GitHub portfolio")

    if "react" in missing_skills:
        suggestions.append("Build a React project")

    if "sql" in missing_skills:
        suggestions.append("Practice SQL queries and database concepts")

    if "python" in missing_skills:
        suggestions.append("Strengthen Python programming skills")        

    return render_template(
    'result.html',
    score=round(score),
    found_skills=found_skills,
    missing_skills=missing_skills,
    suggestions=suggestions
)    

if __name__ == '__main__':
    app.run(debug=True)