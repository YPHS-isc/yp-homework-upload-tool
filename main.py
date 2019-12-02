import requests 
import bs4 

login_page_url = "tea/tua.aspx"
base_page_url ="http://www.yphs.tp.edu.tw/"
account=""
password=""
claas=""

def login():
    res = requests.get(base_page_url+login_page_url)
    soup=bs4.BeautifulSoup(res.text)
    viewstate=soup.find_all("input")[0]["value"]
    viewstategenerator=soup.find_all("input")[1]["value"]
    eventvalidation=soup.find_all("input")[2]["value"]
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"tbox_acc":account,"tbox_pwd":password,"tbox_cls":claas,"but_login":"登　　入"}
    cookies={"AspxAutoDetectCookieSupport":"1"}
    respond=requests.post(base_page_url+login_page_url,allow_redirects=True,data=data,cookies=cookies)
    print(respond.text)

def main():
    login()

main()
