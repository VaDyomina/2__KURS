import re
import html
import urllib.request


REGTAG = re.compile('<.*?>', flags=re.U | re.DOTALL) # реги, чтобы очистить код и оставить только текст
REGSCRIPT = re.compile('<script>.*?</script>', flags=re.U | re.DOTALL)
REGSCRIPT1 = re.compile('<style>.*?</style>', flags=re.U | re.DOTALL) 
REGSCRIPT2 = re.compile('<script type.*?>.*?</script>', flags=re.U | re.DOTALL)
REGSCRIPT3 = re.compile('<style type.*?>.*?</style>', flags=re.U | re.DOTALL) 
REGCOMMENT = re.compile('<!--.*?-->', flags=re.U | re.DOTALL)
REGSPACES = re.compile('\s{2,}', flags=re.U | re.DOTALL)
REGTIME = re.compile("\d{1,2}(:|\.)\d{1,2}", flags=re.U | re.DOTALL)
REGPUNC = re.compile("[\"...\",\\:«»]", flags=re.U | re.DOTALL)


def opening():
    page = urllib.request.urlopen("https://lenta.ru") # открываем новостной сайт
    text = page.read().decode('utf-8') # читаем, декодируем
    clean_t = cleaning(text) # очищаем
    with open("1.txt", "w", encoding="utf-8") as f: # записываем
        f.write(html.unescape(clean_t))
        

def cleaning(text):                          
        clean_t = REGSCRIPT.sub(" ", text) # очистка текста
        clean_t = REGSCRIPT1.sub(" ", clean_t)
        clean_t = REGSCRIPT2.sub(" ", clean_t)
        clean_t = REGSCRIPT3.sub(" ", clean_t)
        clean_t = REGCOMMENT.sub(" ", clean_t)
        clean_t = REGTAG.sub(" ", clean_t)
        clean_t = REGSPACES.sub(" ", clean_t)
        clean_t = clean_t.replace("\t", " ")
        clean_t = clean_t.replace("\n", " ")
        clean_t = REGTIME.sub("@", clean_t)
        clean_t = REGPUNC.sub("", clean_t)
        clean_t = clean_t.replace("@", ".")
        return clean_t


opening()
