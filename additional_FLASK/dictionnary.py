import json
import html
import re
import urllib.request

PAGE = "http://www.dorev.ru/ru-index.html" # глобально задаем адреса страниц
URL = "http://www.dorev.ru/"

REGPAGE = re.compile("bgcolor=\"#CCCCCC\"><a href=\"(.{18})", flags=re.U | re.DOTALL) # рег для ссылок на все буквы 

REG1 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{2,15})</td><td align=\"center\">", flags=re.U | re.DOTALL) # рег для слов на сайте-словаре
REG2 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{1,9})<span.*\"u1\">(\w{1}).*</span>(\w{1,7})</td>", flags=re.U | re.DOTALL)
REG3 = re.compile("<td class=\"uu\">(\w{2,15})</td><td></td><td class=\"uu\">(\w{1,9})<span.*\"u1\">(\w{1}).*</span>(\w{1,9})(</td>| \(|, )", flags=re.U | re.DOTALL)


def download_main_page(PAGE):
        page = urllib.request.urlopen(PAGE) # получаем главную страницу
        text = page.read().decode('windows-1251') # читаем, декодируем
        if REGPAGE.findall(text):
                res = REGPAGE.findall(text)  # ищем ссылки на все буквы 
        else:
                res = "" # если сайт не пускает...., то и словаря не будет
        return res      


def download_page(pageUrl):
        page = urllib.request.urlopen(pageUrl) # запрашиваем каждую страницу
        text = page.read().decode('windows-1251').replace("color", "\n") # делаем замену,  чтобы потом было удобно сплитить
        text = text.split("\n") # сплитим
        return text


def getting_text(text, d, dictionary):
        for i in text:
                if REG1.search(i):  # выцепляем слова
                        res = REG1.search(i).group(1) # слово 1 наша орф
                        res2 = REG1.search(i).group(2) # слово 2 дорев орф
                        d = {res : res2}# создаем словарную строку, предыдущая стирается (можно сделать по-другому, легче, но я не помню как точно) 
                        dictionary.update(d) # добавляем ее в другой словарь
                elif REG2.search(i):  # выцепляем слова
                        res = REG2.search(i).group(1) # слово 1 наша орф
                        res2 = REG2.search(i).group(2)+REG2.search(i).group(3)+REG2.search(i).group(4) # слово 2 дорев орф (есть ударение -- избавляемся)
                        d = {res : res2}
                        dictionary.update(d)
                elif REG3.search(i):  # выцепляем слова
                        res = REG3.search(i).group(1) # слово 1 наша орф
                        res2 = REG3.search(i).group(2)+REG3.search(i).group(3)+REG3.search(i).group(4) # слово 2 дорев орф (есть ударение -- избавляемся)
                        d = {res : res2}
                        dictionary.update(d)
                else:
                        continue
        return dictionary

                
def main():
        d = dict()
        dictionary = dict()
        res = download_main_page(PAGE)
        for i in res: # перебираем ссылки на бувы словаря
                pageUrl = URL + i # добавляем их к изначальному юэрэлу
                text = download_page(pageUrl) 
                getting_text(text, d, dictionary)
        j = json.dumps(dictionary, ensure_ascii=False, indent = 4) # закидываем словарь в json (очень удобно)
        with open("data.json", 'w', encoding="utf-8") as f: # записываем json
                f.write(j)
                                       

if __name__ == "__main__":
        main()
