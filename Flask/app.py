from flask import Flask, request, render_template


app = Flask(__name__)

@app.route('/')
def root():
    return "This is the home page."

@app.route('/highfive')
@app.route('/highfive/<user>', methods=['GET', 'POST'])
def high_five(user=None):
    if request.method == 'GET':
        return render_template("high_five.html", user=user)

if __name__ == "__main__":
    app.run()
