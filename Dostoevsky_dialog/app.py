# -*- coding: utf-8 -*-

import re
import os
from flask import Flask, request, render_template, url_for, json
from random import uniform
from collections import defaultdict

model = {}
app = Flask(__name__)
r_alphabet = re.compile(u'(?!\-\-)[А-яЁё0-9-]+|[.,:;?!]+')

# flask routes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/sentence_gen", methods=['POST'])
def sentence_gen():
    received = request.form['sentence'].strip('.!?,;:\'\"\/\\').split()
    first_word = received[len(received)-1].lower()
    if re.match('[^А-яЁё]', first_word) != None:
        return json.dumps({'answer': 'Я - русский писатель! (Введите фразу на русском)'}, ensure_ascii=False)
    sentence = generate_sentence(model, first_word)
    return json.dumps({'answer': sentence}, ensure_ascii=False)

# helpers


def gen_lines(corpus):
    data = open(corpus, 'r', encoding="utf-8")
    for line in data:
        yield line.lower()


def gen_tokens(lines):
    for line in lines:
        for token in r_alphabet.findall(line):
            yield token


def gen_trigrams(tokens):
    t0, t1 = '$', '$'
    for t2 in tokens:
        yield t0, t1, t2
        if t2 in '.!?':
            yield t1, t2, '$'
            yield t2, '$', '$'
            t0, t1 = '$', '$'
        else:
            t0, t1 = t1, t2


def train(corpus):
    lines = gen_lines(corpus)
    tokens = gen_tokens(lines)
    trigrams = gen_trigrams(tokens)

    bi, tri = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)

    for t0, t1, t2 in trigrams:
        bi[t0, t1] += 1
        tri[t0, t1, t2] += 1

    model = {}
    for (t0, t1, t2), freq in tri.items():
        if (t0, t1) in model:
            model[t0, t1].append((t2, freq/bi[t0, t1]))
        else:
            model[t0, t1] = [(t2, freq/bi[t0, t1])]
    return model


def generate_sentence(model, first_word):
    phrase = '' + first_word
    t0, t1 = '$', first_word

    first_pair = False
    for (model_item_1, model_item_2) in model:
        if first_word == model_item_1:
            first_pair = (model_item_1, model_item_2)
            break
    while 1:
        try:
            t0, t1 = t1, unirand(model[t0, t1])
            print("word was found in the beginning of sentence")
        except:
            if first_pair != False:
                t0, t1 = first_pair[0], first_pair[1]
                phrase += ' '
                print("pair with word was found")
            else:
                t0, t1 = '$', unirand(model['$', '$'])
                phrase += ' '
                print("word isn't found")
        if t1 == '$':
            break
        if t1 in ('.!?,;:') or t0 == '$':
            phrase += t1
        else:
            phrase += ' ' + t1

    return phrase.capitalize()


def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

# run app


if __name__ == '__main__':
    model = train('static/dicts/dostoevsky.txt')
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port, host='0.0.0.0', debug=True)
