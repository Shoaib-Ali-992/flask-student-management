from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

students = {}
subjects = ['math', 'physic', 'computer']

@app.route("/")
def index():
    return render_template("index.html", students=students)

@app.route("/add", methods=["POST"])
def add_student():
    std_id = request.form["std_id"].strip()
    std_name = request.form["std_name"].strip().title()
    std_class = request.form["std_class"].strip()

    if not std_id or std_id in students:
        return "Invalid or duplicate ID!"

    record = {"std_name": std_name, "std_class": std_class}

    for sub in subjects:
        marks = request.form.get(sub, "0")
        record[sub] = int(marks)

    record['std_subjects'] = subjects
    students[std_id] = record
    return redirect(url_for("index"))

@app.route("/delete/<std_id>")
def delete_student(std_id):
    if std_id in students:
        del students[std_id]
    return redirect(url_for("index"))

@app.route("/update/<std_id>", methods=["GET", "POST"])
def update_student(std_id):
    if std_id not in students:
        return "Student not found!"

    if request.method == "POST":
        record = students[std_id]
        record['std_name'] = request.form["std_name"].strip().title() or record['std_name']
        record['std_class'] = request.form["std_class"].strip() or record['std_class']

        for sub in subjects:
            marks = request.form.get(sub)
            if marks:
                record[sub] = int(marks)
        students[std_id] = record
        return redirect(url_for("index"))

    return render_template("index.html", students=students, update_id=std_id)

if __name__ == "__main__":
    app.run(debug=True)
