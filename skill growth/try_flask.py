from flask import Flask, jsonify, request, abort

app = Flask(__name__)

students = {"Access time": 1}

@app.route('/students', methods=['POST'])
def create_student():
    new_student = request.args.get('name')
    if new_student in students:
        abort(404)
    students[new_student] = "Created!!!"
    return jsonify(students)

@app.route('/students', methods=['GET'])
def get_all_students():
    students["Access time"] += 1
    return jsonify(students)

@app.route('/students/<id>', methods=['PUT'])
def update_student_data(id):
    new_value = request.args.get('value')
    students[id] = new_value
    return jsonify({"Result": students})

@app.route('/students/<id>', methods=['DELETE'])
def del_student_data(id):
    del students[id]
    return jsonify({"Result": students})

@app.route('/')
def hello_world():
    return "A site with students"


if __name__ == '__main__':
    app.run()