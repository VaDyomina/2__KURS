from flask import Flask
from flask import request, render_template
from mystem_words import stage_1
from lenta_cl import opening
import json
import os
import re
import urllib.request
import html
from operator import itemgetter

app = Flask(__name__) #импорт фласка

@app.route('/') # декоратор, добавляем к хосту "/"
def getting_temp(t=None):
    t = ""
    request = urllib.request.Request('https://www.gismeteo.ru/weather-skopje-3253/now/') # запрос страницы
    with urllib.request.urlopen(request) as response:
       code = response.read().decode('utf-8') # получили код
    regTemp = re.compile("\s(.*)<span class=\"tab-weather__value_m\">\,.<\/span>") # регулярка вычленяет темпу
    temp = regTemp.findall(code) # на выходе массив
    for t in temp:
        return render_template('f.html', t=html.unescape(t.replace(" ", ""))) # избавляемся от массива, пробелов, html-символов, вызов шаблона страницы

@app.route('/answer') # декоратор, добавляем к хосту "/answer'"
def getting_answer(res=None):
    req = str(request.args["word"]) # считываем то, что внес пользователь в форму
    res = stage_1(req) # запускаем другую программу, переводим слово в дорев. орфографию
    return render_template('form_res.html', res=res) # шаблон, передаем слово в дореф. орфографии


@app.route('/site') # декоратор, добавляем к хосту "/site"
def making_site(d=None, a=None):
    opening() # закачиваем сайт
    a = []
    d = dict()
    with open("1.txt", "r", encoding="utf-8") as f: # здесь сохранен код сайта
        a = [i for i in f.read().split()] # в массив добавляем по слову из кода
    for req in a:
            r = stage_1(req) # запускаем другую программу, переводим слово в дорев. орфографию
            if r: # если r не None (ничего)
                if r in d:
                    d[r] += 1 # счетчик слов в словаре
                else:
                    d[r] = 1
    d_sorted = sorted(d.items(), key=itemgetter(1), reverse=True) # сортируем словарь
    a = d_sorted[:11] # вычленяем первые 10 частотных слов
    with open("d_sort.txt", "w", encoding="utf-8") as f:
        f.write(str(sorted(d.items(), key=itemgetter(1), reverse=True))) # сохраняем весь отсортированный словарь
    with open("d.txt", "w", encoding="utf-8") as f:
        f.write(str(d)) # сохраняем просто словарь
    return render_template('form_site.html', d=d, a=a) # шаблон, передаем словарь со словами в дореф. орфографии и топ-10 слов


@app.route('/test') # декоратор, добавляем к хосту '/test'
def test(d=None):
    d = {"убежище":"убѣжище", "веко":"вѣко", "полено":"полѣно", "железо":"желѣзо", "манера":"манѣра",
         "прореха":"прорѣха", "колея":"колѣя", "недра":"нѣдра", "цепь":"цѣпь", "сусек":"сусѣкъ"} # словарь с вариантами слов для теста 
    return render_template('form_test.html', d=d) # шаблон, передаем словарь со словами


@app.route('/results') # декоратор, добавляем к хосту '/results'
def results(total=None):
    total=0
    if 'убежище' in request.args: # если пользователь ответил на этот вопрос и ответ есть в переменной 
        if "убежище" != request.args['убежище']: # то ...
            total += 1 # если правильно
        else:
            total=total # если нет
    else:
        total=total # если ничего не ответил, кол-во баллов не меняется
    if 'веко' in request.args:
        if  'веко' != request.args['веко']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'полено' in request.args:
        if  'полено' == request.args['полено']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'железо' in request.args:
        if  'железо' == request.args['железо']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'манера' in request.args:
        if  'манера' == request.args['манера']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'прореха' in request.args:
        if  'прореха' != request.args['прореха']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'колея' in request.args:
        if  'колея' == request.args['колея']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'недра' in request.args:
        if  'недра' != request.args['недра']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'цепь' in request.args:
        if  'цепь' != request.args['цепь']:
            total += 1
        else:
            total = total
    else:
        total = total
    if 'сусек' in request.args:
        if  'сусек' != request.args['сусек']:
            total += 1
        else:
            total = total
    else:
        total = total
    return render_template('form_results.html', total=str(total)) # шаблон, передаем итог в виде строки


if __name__ == '__main__':
    app.run(debug=True)
