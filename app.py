from unittest import result

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
    print(missing_skills)    

    return render_template(
    'result.html',
    score=round(score),
    found_skills=found_skills,
    missing_skills=missing_skills
)    

if __name__ == '__main__':
    app.run(debug=True)