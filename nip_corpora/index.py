import csv
import html
import os
import re
import urllib.request


COMMONURL = 'http://www.n-i-p.ru/news/'

REGSCRIPT = re.compile('<script>.*?</script>', flags = re.U | re.DOTALL)
REGSCRIPT1 = re.compile('<style>.*?</style>', flags = re.U | re.DOTALL)
REGSCRIPT2 = re.compile('<script type.*?</script>', flags = re.U | re.DOTALL)
REGCOMMENT = re.compile('<!--.*?-->', flags = re.U | re.DOTALL)
REGTAG = re.compile('<.*?>', flags = re.U | re.DOTALL) #находит теги
REGCATEGORY = re.compile('Категории:</h3><ul><li><a href=\"/news/\?category=.*?\" rel=\"nofollow\">(.*?)</a>', re.DOTALL)
REGNAME = re.compile('<meta name="title" content=\"(.*?)\"/>', re.DOTALL)
REGDATE = re.compile('<span class=\"date\">(\d{2}\.\d{2}.\d{4})</span>', re.DOTALL)


def download_page (pageUrl):
    try:
        page = urllib.request.urlopen(pageUrl) #весь текст, найденный текст 
        text = page.read().decode ('utf-8')
        print(pageUrl)
        clean_t = cleaning(text)
        details(text,pageUrl,clean_t)
    except:
        print('Error at', pageUrl)
        return

    
def cleaning(text):
    clean_t = REGSCRIPT.sub("", text)
    clean_t = REGSCRIPT1.sub("", clean_t)
    clean_t = REGCOMMENT.sub("", clean_t)
    clean_t = REGSCRIPT2.sub("", clean_t)
    clean_t = REGTAG.sub("", clean_t)
    return clean_t


def details(text, pageUrl, clean_t):
    date = REGDATE.search(text).group(1)
    day, month, year = date.split('.')
    name = REGNAME.search(text).group(1)
    category = REGCATEGORY.search(text).group(1)
    name2 = name.replace(' ', '_')
    name3 = re.sub("[.,!?()\"-\/]", "",  name2)
    making_plain(name3, clean_t, year, month)
    marking_xml(year, month, name2, name3)
    marking_plain(year, month, name2, name3)
    making_plain2(name2, name3, date, category, pageUrl, clean_t, year, month)
    path = "Наша_иртышская_правда{}plain{}{}{}{}{}{}.txt".format(os.sep,os.sep,year,os.sep,month,os.sep,name)
    with open (os.path.join('Наша_иртышская_правда', 'metadata.csv'), 'a', encoding = 'utf-8') as f:
       output = csv.writer(f, delimiter='\t')
       output.writerow(["\n{}\t\t\t\t{}\t{}\tпублицистика\t\t\t{}\tнейтральный\tн-возраст\tн-уровень\tрайонная\t{}\tНаша иртышская правда\t\t{}\tгазета\tРоссия\tОмская область\tru".format(path,name,date,category,pageUrl,year)])
    return


def making_plain(name3, clean_t, year, month):
    path = "Наша_иртышская_правда/plain/{}/{}".format(year, month)
    folder = os.path.join("{}/{}.txt".format(path, name3))
    if not os.path.exists(path):
        os.makedirs(path)
    with open(folder, 'w', encoding = 'utf-8') as f:
        f.write(html.unescape(clean_t))


def marking_xml(year, month, name2, name3):
    path_output = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/mystem-xml/{}/{}/".format(year, month)
    file_i = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/plain/{}/{}/{}.txt".format(year, month, name3)
    file_o = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/mystem-xml/{}/{}/{}.xml".format(year, month, name3)
    if not os.path.exists(path_output):
        os.makedirs(path_output)
    os.system("/Users/Ya.Klop/Downloads/mystem -idn --format xml " + file_i + " " + file_o)
    print(1)
    

def marking_plain(year, month, name2, name3):
    path_output = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/mystem-plain/{}/{}/".format(year, month)
    file_i = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/plain/{}/{}/{}.txt".format(year, month, name3)
    file_o = "/Users/Ya.Klop/Desktop/Наша_иртышская_правда/mystem-plain//{}/{}/{}.txt".format(year, month, name3)
    if not os.path.exists(path_output):
        os.makedirs(path_output)
    os.system("/Users/Ya.Klop/Downloads/mystem -idn " + file_i + " " + file_o)
    print(2)
      
    
def making_plain2(name2, name3, date, category, pageUrl, clean_t, year, month):
    extra = "@au \n@ti {}\n@da {}\n@topic {}\n@url {}\n{}".format(name2, date, category, pageUrl, clean_t) 
    path = "Наша_иртышская_правда{}plain{}{}{}{}".format(os.sep,os.sep,year,os.sep,month)
    folder = os.path.join("{}{}{}.txt".format(path, os.sep, name3))
    with open(folder, 'w', encoding = 'utf-8') as f:
        f.write(html.unescape(extra))
            
       
def main():
    if not os.path.exists("/Users/Ya.Klop/Desktop/Наша_иртышская_правда"):
        os.mkdir("Наша_иртышская_правда")
    with open (os.path.join('Наша_иртышская_правда', 'metadata.csv'), 'a', encoding = 'utf-8') as f:
        output = csv.writer(f, delimiter='\t')
        header = ['path' + '\t' + 'author' + '\t' + 'sex' +' \t' + 'birthday' + 'header' + '\t' + 'created' + '\t' + 'sphere' + '\t' + 'genre_fl' + '\t' + 'type' + '\t' + 'topic' + '\t' + 'chronotop' + '\t' + 'style' + '\t' + 'audience_age' + '\t' + 'audience_level' + '\t' + 'audience_size' + '\t' + 'source' + '\t' + 'publication' + '\t' + 'publisher' + '\t'  + 'publ_year' + '\t' + 'medium' + '\t' + 'country' + '\t' + 'region' + '\t' + 'language' + '\n']
        output.writerow(header)
    for i in range(179914, 1, -1):  
        pageUrl = COMMONURL + str(i)  #записывает адрес + номер
        download_page(pageUrl)


main()
