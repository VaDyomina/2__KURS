# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, url_for, json

from pymystem3 import Mystem
m = Mystem()

from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

import random

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/sentence_gen", methods=['POST'])
def sentence_gen():
	received = request.form['sentence'].split();
	tags_list = get_info(received)

	wordlist = get_wordlist()
	grammems = get_grammems(wordlist)

	answer = []
	for single_tag in tags_list:
		rand = random.choice(grammems[single_tag['pos']])
		inflected = inflect_word(rand, single_tag['inflect'])
		print(inflected)
		answer.append(inflected)

	print(answer)
	return json.dumps({'answer': ' '.join(answer)})

def get_info(words):
	tags = []
	for word in words:
		ana = morph.parse(word)[0]
		if ana.tag.POS:
			temp_tags = []
			temp_tags.append({'animacy': ana.tag.animacy})
			temp_tags.append({'aspect': ana.tag.aspect})
			temp_tags.append({'case': ana.tag.case})
			temp_tags.append({'gender': ana.tag.gender})
			temp_tags.append({'involvement': ana.tag.involvement})
			temp_tags.append({'mood': ana.tag.mood})
			temp_tags.append({'number': ana.tag.number})
			temp_tags.append({'person': ana.tag.person})
			temp_tags.append({'tense': ana.tag.tense})
			temp_tags.append({'transitivity': ana.tag.transitivity})
			temp_tags.append({'voice': ana.tag.voice})
			tags.append({'pos': ana.tag.POS, 'inflect': temp_tags})
		else:
			continue
	return tags

def inflect_word(word, tags):
	ana = morph.parse(word)[0]
	print(ana)
	if ana.normalized.tag.animacy:
		ana.inflect({tags[0]['animacy']})
	if ana.normalized.tag.aspect:
		ana.inflect({tags[1]['aspect']})
	if ana.normalized.tag.case:
		ana.inflect({tags[2]['case']})
	if ana.normalized.tag.gender:
		ana.inflect({tags[3]['gender']})
	if ana.normalized.tag.involvement:
		ana.inflect({tags[4]['involvement']})
	if ana.normalized.tag.mood:
		ana.inflect({tags[5]['mood']})
	if ana.normalized.tag.number:
		ana.inflect({tags[6]['number']})
	if ana.normalized.tag.person:
		ana.inflect({tags[7]['person']})
	if ana.normalized.tag.tense:
		ana.inflect({tags[8]['tense']})
	if ana.normalized.tag.transitivity:
		ana.inflect({tags[9]['transitivity']})
	if ana.normalized.tag.voice:
		ana.inflect({tags[10]['voice']})
	print(ana)
	return ana.word

def get_wordlist():
	result = []
	with open ('static/dicts/wordforms.txt', 'r', encoding='utf-8') as file:
		text = file.read().lower().split()
		for word in text:
			if not word.isdecimal():
				result.append(word)
	return result

def get_grammems(wordlist):
	grammems = {}
	# with open ('static/dicts/wordforms_grammems.txt', 'a', encoding='utf-8') as file:
	for i in range(2000):
		ana = morph.parse(wordlist[i])[0]
		if ana.tag.POS:
			if ana.tag.POS in grammems:
				grammems[ana.tag.POS].append(ana.word)
			else:
				grammems[ana.tag.POS] = []
				grammems[ana.tag.POS].append(ana.word)
		else:
			continue
		# file.write(json.dumps(grammems, ensure_ascii=False))
	return grammems

if __name__ == '__main__':
	app.run()
