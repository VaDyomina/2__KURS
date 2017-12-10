# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import json
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'survey.db')

db = SQLAlchemy(app)

cols = ['id', 'name', 'sex', 'age', 'city', 'education', 'occupation']

class Survey(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(255))
	sex = db.Column(db.Boolean)
	age = db.Column(db.Integer)
	city = db.Column(db.String(255))
	education = db.Column(db.Integer)
	occupation = db.Column(db.Integer)

class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	q1 = db.Column(db.String(255))
	q2 = db.Column(db.String(255))
	q3 = db.Column(db.String(255))
	q4 = db.Column(db.String(255))
	q5 = db.Column(db.String(255))
	q6 = db.Column(db.String(255))
	q7 = db.Column(db.String(255))
	q8 = db.Column(db.String(255))
	q9 = db.Column(db.String(255))
	q10 = db.Column(db.String(255))
	q11 = db.Column(db.String(255))
	q12 = db.Column(db.String(255))


@app.route("/", methods=['POST', 'GET'])
def survey_1():
	return render_template("survey_1.html")

@app.route("/survey_2", methods=['POST', 'GET'])
def survey_2():
	return render_template("survey_2.html")

@app.route("/submited_1", methods=['POST'])
def submited_1():
	survey = Survey( \
		name = request.form['name'], \
		sex = request.form['sex'], \
		age = request.form['age'], \
		city = request.form['city'], \
		education = request.form['education'], \
		occupation = request.form['occupation'])

	db.session.add(survey)
	db.session.commit()

	return redirect(url_for('survey_2'))

@app.route("/submited_2", methods=['POST'])
def submited_2():
	test = Test( \
		q1 = request.form['q1'], \
		q2 = request.form['q2'], \
		q3 = request.form['q3'], \
		q4 = request.form['q4'], \
		q5 = request.form['q5'], \
		q6 = request.form['q6'], \
		q7 = request.form['q7'], \
		q8 = request.form['q8'], \
		q9 = request.form['q9'], \
		q10 = request.form['q10'], \
		q11 = request.form['q11'])

	db.session.add(test)
	db.session.commit()

	return redirect(url_for('survey_1'))

@app.route("/stats_1")
def stats_1():
	survey = Survey.query.all()

	return render_template("stats_1.html", survey=survey)

@app.route("/stats_2")
def stats_2():
	test = Test.query.all()

	return render_template("stats_2.html", test=test)

@app.route("/json_1")
def json_out_1():
	survey = Survey.query.all()
	result = [{col: getattr(single, col) for col in cols} for single in survey]

	return json.dumps(result, ensure_ascii=False)

@app.route("/json_2")
def json_out_2():
	test = Test.query.all()
	result = [{col: getattr(single, col) for col in cols} for single in test]

	return json.dumps(result, ensure_ascii=False)
	
@app.route("/search_1")
def search_1():
	return render_template("search_1.html")

@app.route("/search_2")
def search_2():
	return render_template("search_2.html")

@app.route("/results_1", methods=["POST"])
def results_1():
	target_cols = []
	for col in request.form:
		if request.form[col]:
			target_cols.append(col)

	if 'name' in target_cols:
		survey = Survey.query.filter_by(name=request.form['name']).all()
	if 'sex' in target_cols:
		survey = Survey.query.filter_by(sex=request.form['sex']).all()
	if 'age' in target_cols:
		survey = Survey.query.filter_by(age=request.form['age']).all()
	if 'city' in target_cols:
		survey = Survey.query.filter_by(city=request.form['city']).all()
	if 'education' in target_cols:
		survey = Survey.query.filter_by(education=request.form['education']).all()
	if 'occupation' in target_cols:
		survey = Survey.query.filter_by(occupation=request.form['occupation']).all()
	if not target_cols:
		survey = Survey.query.all()

	survey_obj = [{col: getattr(single, col) for col in cols} for single in survey]

	return render_template("results_1.html", survey_obj=survey_obj)

@app.route("/results_2", methods=["POST"])
def results_2():
	target_cols = []
	for col in request.form:
		if request.form[col]:
			target_cols.append(col)

	if 'q1' in target_cols:
		test = Test.query.filter_by(q1=request.form['q1']).all()
	if 'q2' in target_cols:
		test = Test.query.filter_by(q2=request.form['q2']).all()
	if 'q3' in target_cols:
		test = Test.query.filter_by(q3=request.form['q3']).all()
	if 'q4' in target_cols:
		test = Test.query.filter_by(q4=request.form['q4']).all()
	if 'q5' in target_cols:
		test = Test.query.filter_by(q5=request.form['q5']).all()
	if 'q6' in target_cols:
		test = Test.query.filter_by(q6=request.form['q6']).all()
	if 'q7' in target_cols:
		test = Test.query.filter_by(q7=request.form['q7']).all()
	if 'q8' in target_cols:
		test = Test.query.filter_by(q8=request.form['q8']).all()
	if 'q9' in target_cols:
		test = Test.query.filter_by(q9=request.form['q9']).all()
	if 'q10' in target_cols:
		test = Test.query.filter_by(q10=request.form['q10']).all()
	if 'q11' in target_cols:
		test = Test.query.filter_by(q11=request.form['q11']).all()	
	if 'q12' in target_cols:
		test = Test.query.filter_by(q12=request.form['q12']).all()		
	if not target_cols:
		test = Test.query.all()

	test_obj = [{col: getattr(single, col) for col in cols} for single in test]

	return render_template("results_2.html", test_obj=test_obj)

if __name__ == '__main__':
	app.run()
