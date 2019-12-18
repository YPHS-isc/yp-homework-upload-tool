import requests 
import bs4 
import pprint
import datetime
import flask
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters ,CommandHandler

login_page_path = "tea/tua.aspx"
index_page_path="tea/tua-1.aspx"
base_page_url ="http://www.yphs.tp.edu.tw/"
account=""
password=""
claas=""
access_cookie=dict()
bot_token=""//put your token

bot = telegram.Bot(token=bot_token)

def login():
    res = requests.get(base_page_url+login_page_path)
    soup=bs4.BeautifulSoup(res.text,"html.parser") #lxml->faster
    viewstate=soup.find_all("input")[0]["value"]
    viewstategenerator=soup.find_all("input")[1]["value"]
    eventvalidation=soup.find_all("input")[2]["value"]
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"tbox_acc":account,"tbox_pwd":password,"tbox_cls":claas,"but_login":"登　　入"}
    cookies={"AspxAutoDetectCookieSupport":"1"} # to detect whether the user's browser supports cookies(if not, then it won't let you go on)
    respond=requests.post(base_page_url+login_page_path,allow_redirects=False,data=data,cookies=cookies)
    
    #save sessionId
    global access_cookie
    access_cookie={'ASP.NET_SessionId':respond.cookies["ASP.NET_SessionId"]}

def new_post(title,content):

    # add a new post
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
    if len(title)==0:
        title=date
    data={"__VIEWSTATE":viewstate,"__VIEWSTATEGENERATOR":viewstategenerator, "__EVENTVALIDATION":eventvalidation,"but_save":"儲存","tbox_purport":title,"tbox_content":content,"tbox_link":""}
    requests.post(base_page_url+index_page_path,data=data,cookies=access_cookie)
    
app=flask.Flask(__name__)
@app.route('/webhook/homework_upload',methods=["POST"])
def webhook(): #the function handle at https:://lee-tw.me/webhook/homework_upload
    update = telegram.Update.de_json(flask.request.get_json(force=True), bot)#pipe what we got in chat and pipe it into python-telegram-bot(module)
    dispatcher.process_update(update)
    return "temp ok"

dispatcher=Dispatcher(bot, None) #create a new dispatcher

def post_handler(bot, update):
    login()
    x=update.message.text#.split(" ")[1].spilt("$")
    try :
        x=x.split(' ')[1].split('$')
        print(x[0],x[1])
        new_post(x[0],x[1].replace('\\n','\n'))
        update.message.reply_text("post_done\n標題:"+x[0]+"\n內文:"+x[1].replace('\\n','\n'))
    except:
        update.message.reply_text("You might forget '$' or login failed")

def debug_handler(bot,update):
    update.message.reply_text("webhook ok")

'''
def modify_handler(bot, update):
    pass
def main():
    login()
    new_post(" ","這篇適用python requests submit der")
    dispatcher.add_handler(CommandHandler("modify", modify_handler))
''' 

dispatcher.add_handler(CommandHandler("post", post_handler))
dispatcher.add_handler(CommandHandler("debug", debug_handler))

if __name__=="__main__":
    app.run(port=5001)


