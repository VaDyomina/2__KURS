from dictionnary import main
import json
import os
import re


REGWORD = re.compile("{(\w*)") # начальная форма
REGPART = re.compile("{\w*=(\w*)") # часть речи
REGCASE = re.compile("\W(\w{2,4}.\w{2})\W") # падеж

VOWELS = ["а", "о", "э", "и", "у", "ы", "е", "ё", "ю", "я"]
CONSONANTS = ["б", "в", "г", "д", "ж", "з", "к", "л", "м", "н", "п", "р", "с", "т", "ф", "х", "ц", "ч", "ш", "щ"]


def stage_1(req):
    try:
        file = open('data.json') # проверяем, есть ли скачанный словарь
    except:
        main() # если нет, то качаем
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f) # открываем
    if req in data: # есть ли заданное пользователем слово в той же форме в словаре
        r = data[req] # изи, готово!
    elif req == "." or req == "—" or req == "": # избавяемся от пунктуации
        r = None # скидываем ее
    else:
        r = stage_2(req, data) # если нет в словае, то этап 2
    return r


def stage_2(req, data):
    res1 = ""
    with open("a.txt", "w", encoding="utf-8") as f: # создаем файл и записываем туды слово пользователя
        f.write(req)
    os.system("/Users/Ya.Klop/Desktop/additional_FLASK/mystem -ig a.txt res.txt") # майстемим
    with open("res.txt", "r", encoding="utf-8") as f: # открываем файл, созданный майстемом
        result = f.read() # читаем его разбор
    if REGWORD.search(result): # есть ли начальная форма?
        res1 = REGWORD.search(result).group(1) # вычленняем начальную форму из разбора
    if res1 in data: # если есть начальная форма в словаре, то
        a = stage_3(result, req) # этап 3
    else:
        a = stage_4(result, req) # если нет, то этап 4
    return a


def stage_3(result, req):
    res_1 = ""
    if REGPART.search(result):
        if  "S" == REGPART.search(result).group(1): # существительное?
            try:
                case = REGCASE.search(result).group(1) # есть падеж в разборе?
                if  case == "дат,ед":
                    res_1 = req[:-1] + "ѣ"
                elif  case == "пр,ед":
                    res_1 = req[:-1] + "ѣ"
                elif req[-1] in CONSONANTS:
                    res_1 = req + "ъ"
                else:
                    res_1 = req # другой падеж, идем дальше
            except:
                res_1 = req # нет падежа, идем дальше
        elif "A" == REGPART.search(result).group(1): # прилагательное?
            if req.endswith("ие"):
                res_1 = req.replace("ие", "iя") # меняем окончания
            elif req.endswith("ые"):
                res_1 = req.replace("ые", "ыя")
            elif req.endswith("иеся"):
                res_1 = req.replace("иеся", "iяся")
            else:
                res_1 = req # не такое окончание, идем дальше
        else:
            res_1 = req # не прил, и не сущ
    return res_1


def stage_4(result, req):
    res_2 = ""
    if REGPART.search(result): # начало такое же
        if  "S" == REGPART.search(result).group(1):
            try:
                case = REGCASE.search(result).group(1)
                if  case == "дат,ед":
                    res_2 = req[:-1] + "ѣ"
                elif  case == "пр,ед":
                    res_2 = req[:-1] + "ѣ"
                else:
                    res_2 = req
            except:
                res_2 = req
        elif "A" == REGPART.search(result).group(1):
            if req.endswith("ие"):
                res_2 = req.replace("ие", "iя")
            elif req.endswith("ые"):
                res_2 = req.replace("ые", "ыя")
            elif req.endswith("иеся"):
                res_2 = req.replace("иеся", "iяся")
            else:
                res_2 = req
        else:
            res_2 = req
    else:
        res_2 = req # вот до сюда
    for j in range (len(res_2)): # смотрим на буквы в слове и их индекс
        if res_2[j] == "и": # если попалась "и",
            try:
                if res_2[j+1] in VOWELS: # то за ней тоже гласная?
                    res_2 = res_2[:j]+"i"+res_2[j+1:] # тогда меняем "и">"i"
            except:
                continue # если не гласная после "и", то ничего не делаем и продолжаем
    if res_2[-1] in CONSONANTS:
        res_2 = res_2 + "ъ"
    if res_2.startswith("бес"): # если начинаеися с ....
        res_2 = res_2.replace("бес", "без") # то заменяем на ....
    elif res_2.startswith("черес"):
        res_2 = res_2.replace("черес", "через")
    elif res_2.startswith("чрез"):
        res_2 = res_2.replace("чрез", "чрес")
    return res_2


if __name__ == "__main__":
        main()
