from flask import Flask, render_template, request
from skills import SKILLS

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    file = request.files['resume']

    job_description = request.form['job_description']

    import PyPDF2

    pdf_reader = PyPDF2.PdfReader(file)

    text = ""

    for page in pdf_reader.pages:
        text += page.extract_text()


    found_skills = []

    for skill in SKILLS:

        if skill.lower() in text.lower():

            found_skills.append(skill)


    jd_skills = []

    for skill in SKILLS:

        if skill.lower() in job_description.lower():

            jd_skills.append(skill)


    matched_skills = []

    for skill in jd_skills:

        if skill in found_skills:

            matched_skills.append(skill)

        missing_jd_skills = []

    for skill in jd_skills:

        if skill not in found_skills:

            missing_jd_skills.append(skill)    

    if len(jd_skills) > 0:

        match_score = (
            len(matched_skills)
            / len(jd_skills)
        ) * 100

    else:

        match_score = 0

    score = (
        len(found_skills)
        / len(SKILLS)
    ) * 100

    missing_skills = []

    for skill in SKILLS:

        if skill not in found_skills:

            missing_skills.append(skill)

    # Suggestions

    suggestions = []

    if "aws" in missing_jd_skills:
        suggestions.append(
            "Learn AWS Cloud Fundamentals"
        )

    if "git" in missing_jd_skills:
        suggestions.append(
            "Create and maintain a GitHub portfolio"
        )

    if "react" in missing_jd_skills:
        suggestions.append(
            "Build a React project"
      )

    if "sql" in missing_jd_skills:
        suggestions.append(
            "Practice SQL queries and database concepts"
    )

    if "python" in missing_jd_skills:
        suggestions.append(
            "Strengthen Python programming skills"
    )

    return render_template(
        'result.html',
        match_score=round(match_score),
        matched_skills=matched_skills,
        missing_jd_skills=missing_jd_skills,
        suggestions=suggestions
    )


if __name__ == '__main__':
    app.run(debug=True)