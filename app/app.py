from flask import Flask, render_template, request, redirect, url_for
import bd_interface
import parse

app = Flask(__name__)

@app.route('/')
def hello_world():
	films = bd_interface.readFromDB()
	films = sorted(films, key=lambda x : x[2] * 100 / x[1] if x[1] != 0 else x[2], reverse=True)
	return render_template('index.html', films=films)

@app.route('/update-data', methods=['POST'])
def update_db():
	bd_interface.deleteDB()
	parse.parser()
	return redirect('/')

if __name__ == '__main__':
	bd_interface.creareDB()
	app.run(debug=True)