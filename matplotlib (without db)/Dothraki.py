import json
import re
import urllib.request
import matplotlib.pyplot as plt


PAGE = "http://wiki.dothraki.org/Vocabulary"

REGWORD = re.compile('<ul><li><b>(\w*?)<\/b>.*?(<dd><i>.*?<\/i>\w*?<\/dd>)*<\/dl>', re.DOTALL)
REGPART = re.compile('<i>(\w*\.)( \w*\.)?</i>', re.DOTALL)


def downloading_page():
        d = {}
        user = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(PAGE, headers={'User-Agent':user})
        with urllib.request.urlopen(req) as response:
            text = response.read().decode('utf-8')
        return text


def data(text):
        if REGWORD.findall(text):
                words = REGWORD.findall(text)
        else:
                words = ""
        if REGPART.findall(text):
                parts = REGPART.findall(text)
        else:
                parts = ""
        return words, parts


def d1(words, letters):
        for word in words:
                word = word[0].lower()
                if word[:1] in letters:
                        letters[word[:1]] += 1
                else:
                        letters[word[:1]] = 1
        return letters


def d2(parts, parts_of_speech):
        parts_of_speech = {}
        for part in parts:
                part = part[0]
                if part == 'n.' or part == 'na.' or part == 'ni.' or part == 'np.' or part == 'prop.':
                        if "noun" in parts_of_speech:
                                parts_of_speech["noun"] += 1
                        else:
                                parts_of_speech["noun"] = 1
                elif part == 'v.' or part == 'vin.' or part == 'vtr.':
                        if "verb" in parts_of_speech:
                                parts_of_speech["verb"] += 1
                        else:
                                parts_of_speech["verb"] = 1
                else:
                        if part in parts_of_speech:
                                parts_of_speech[part] += 1
                        else:
                                parts_of_speech[part] = 1
        return parts_of_speech


def graph_1(letters):
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    x3 = []
    y3 = []
    for k, v in letters.items():
        if len(x1) <= 9: 
                x1.append(k)
                y1.append(v)
        elif len(x2) <= 9:
                x2.append(k)
                y2.append(v)
        else:
                x3.append(k)
                y3.append(v)
    plt.rc('xtick', labelsize=7) # каждая bar chart с буквами вмешает в себя только 10 столбиков почему-то 
    plt.bar(x1, y1, color = "#137e6d") # поэтому сделала 3 таблички для букв (их всего 21)
    plt.title("Letters 1 part") # возможно, их можно было как-то вместить в одну табличку,
    plt.xlabel("letter") # но я быстрее сделала так
    plt.ylabel("quantity")
    plt.savefig('plot_1_1.png')
    plt.figure()
    plt.bar(x2, y2, color = "#cb7723")
    plt.title("Letters 2 part")
    plt.xlabel("letter")
    plt.ylabel("quantity")
    plt.savefig('plot_1_2.png')
    plt.figure()
    plt.bar(x3, y3, color = "#9e003a")
    plt.title("Letters 3 part")
    plt.xlabel("letter")
    plt.ylabel("quantity")
    plt.savefig('plot_1_3.png')
    plt.figure()


def graph_2(parts_of_speech):
    x = []
    y = []
    for k, v in parts_of_speech.items():
        x.append(k)
        y.append(v)
    plt.rc('xtick', labelsize=7) 
    plt.bar(x, y, color = "#fbdd7e")
    plt.title("Parts of speech")
    plt.xlabel("part")
    plt.ylabel("quantity")
    plt.savefig('plot_2.png')
    plt.figure()


def main():
        text = downloading_page()
        words, parts = data(text)
        letters = {}
        letters = d1(words, letters)
        parts_of_speech = {}
        parts_of_speech = d2(parts, parts_of_speech)
        graph_1(letters)
        graph_2(parts_of_speech)
        

if __name__ == "__main__":
        main()
