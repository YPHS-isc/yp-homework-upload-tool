import requests 
import bs4 
import pprint
import datetime

login_page_path = "tea/tua.aspx"
index_page_path="tea/tua-1.aspx"
base_page_url ="http://www.yphs.tp.edu.tw/"
account=""
password=""
claas=""
access_cookie=dict()

def login():
    res = requests.get(base_page_url+login_page_path)
    soup=bs4.BeautifulSoup(res.text,"html.parser")
    viewstate=soup.find_all("input")[0]["value"]
    viewstategenerator=soup.find_all("input")[1]["value"]
    eventvalidation=soup.find_all("input")[2]["value"]
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"tbox_acc":account,"tbox_pwd":password,"tbox_cls":claas,"but_login":"登　　入"}
    cookies={"AspxAutoDetectCookieSupport":"1"}
    respond=requests.post(base_page_url+login_page_path,allow_redirects=False,data=data,cookies=cookies)
    
    #save sessionId??
    global access_cookie
    access_cookie={'ASP.NET_SessionId':respond.cookies["ASP.NET_SessionId"]}

def new_post(title,content):

    # add a new one
    res=requests.get(base_page_url+index_page_path,cookies=access_cookie)
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    viewstate=soup.find_all("input")[0]["value"]
    viewstategenerator=soup.find_all("input")[1]["value"]
    eventvalidation=soup.find_all("input")[2]["value"]
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"but_add":"新增"}
    
    #save the new post
    respond=requests.post(base_page_url+index_page_path,data=data,cookies=access_cookie)
    soup=bs4.BeautifulSoup(respond.text,'html.parser')
    viewstate=soup.find_all("input")[0]["value"]
    viewstategenerator=soup.find_all("input")[1]["value"]
    eventvalidation=soup.find_all("input")[2]["value"]
    date=soup.find('input',{"id":"tbox_purport"})["value"]
    if title==" ":
        title=date
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"but_save":"儲存","tbox_purport":title,"tbox_content":content,"tbox_link":"https://csrc.nist.gov/Projects/post-quantum-cryptography/Email-List"}
    requests.post(base_page_url+index_page_path,data=data,cookies=access_cookie)
    
def main():
    login()
    new_post(" ","這篇適用python requests submit der")
    
main()

