import os
import tkinter as tk
from PIL import Image, ImageTk
from web_scraping_package.scraping import get_rank, get_main_url, get_detail, get_episode_view


def display_info():#點擊搜尋時，觸發的事件
    global image_path
    x = listbox.curselection() #取得點選到的索引
    name_rank = listbox.get(x) #取得該index的內容
    name_rank_split = name_rank.split(":")#分割 取出動漫名稱
    name_rank_split = name_rank_split[1]
    name = name_rank_split.split("總")
    string =  get_detail(x[0],url_list) #在get_detail中 用索引找到 
    content_info.set(string)#將content_info的內容改成抓到的字串
    anime_name.set(name[0])#將anime_name的內容改成抓到的字串
    
    views = get_episode_view(x[0],url_list)  #得到每集觀看數的圖表
    if(views != None):            #如果是在統計中的傳回值是None 將用統計中的圖片顯示       
        im = views
        im = im.resize((600, 300)) 
        im1 = ImageTk.PhotoImage(im)
        imageLabel['image'] = im1
        imageLabel.image = im1
    else:
        image_text.set('尚未進行統計')
        img_filename = 'loading.png'
        im = Image.open(os.path.join(image_path, img_filename)) #打開圖片
        im = im.resize((700,300))
        im1 = ImageTk.PhotoImage(im)
        imageLabel['image'] = im1
        imageLabel.image = im1



#檔案路徑處理
cd = os.getcwd()
image_path = os.path.join(cd, "image")

#建立圖形介面
win = tk.Tk() #建立視窗window
win.title('巴哈姆特動畫瘋') #視窗的名子
win.geometry('1480x764') # 設定視窗的大小(長x寬) 
win.config(bg='#4F4F4F') #背景
win.iconbitmap(os.path.join(image_path, "icon.ico"))  #ICON


anime_list = get_rank()#動漫排名列表
url_list = get_main_url()#動漫網址
        

frame = tk.Frame(win) #讓滾動條和listbox長度一致    
frame2 = tk.Frame(win)
scb = tk.Scrollbar(frame) #設定滾動條

listbox = tk.Listbox(frame,yscrollcommand=scb.set,width=65,height=30,font=('微軟正黑體',12,'bold'))#設定listbox
#逐筆資料加入listbox
for index,content in enumerate(anime_list):
    listbox.insert(index,content)   

title = tk.Label(win,text='巴哈姆特動畫瘋之動漫新番分析',bg='#02F78E',fg='#FFFFFF',width=250,font=('微軟正黑體',20,'bold'))#標題
ranking = tk.Label(win,text='動漫新番排行榜',font=('微軟正黑體',18,'bold'),bg='#FF5809',fg='#FFFFFF',justify='left',padx = 100,pady=10)#排行榜字串
operation_des = tk.Label(frame2,text='操作提示:先點選左方動漫，再按下顯示按鈕',font=('微軟正黑體',12,'bold'),bg='#4F4F4F' ,fg='#FFFFFF')

btn_search = tk.Button(frame2,text='顯示詳細資訊',command = display_info, width = 23,bg='#02F78E',fg='#FFFFFF',font=('微軟正黑體',16,'bold'),relief="flat")#設定搜尋詳細資訊
content_info = tk.StringVar() #設定一個字串變數
anime_name = tk.StringVar()
content_info.set('')  #尚未點擊時的顯示
anime_name.set('')
show_label = tk.Label(win,textvariable=content_info,justify='left',font=('微軟正黑體',14,'bold'),pady=20,bg='#4F4F4F',fg='#FFFFFF',relief="flat")#當btn點擊的時候，content_info會改變資訊，再將其刷新顯示
anime_name_label = tk.Label(win,textvariable=anime_name,font=('微軟正黑體',20,'bold'),bg='#4F4F4F' ,fg='#FFFFFF',relief="flat") #當btn點擊的時候，anime_name會改變資訊，再將其刷新顯示
scb.config(command=listbox.yview)#滾動卷軸和listbox連動

image_text = tk.StringVar()
image_text.set('詳細資訊(包含每集觀看人數圖表)')
imageLabel = tk.Label(win,textvariable= image_text,bg='#4F4F4F' ,fg='#FFFFFF',font=('微軟正黑體',20,'bold'))

title.pack(side='top')
ranking.pack(side='top', anchor = tk.NW, padx = 30, pady = 10)
listbox.pack(side='left', padx = 5, pady = 0)#顯示listbox
scb.pack(side = 'left', fill = tk.Y)
frame.pack(side = 'left') #frame框架顯示
frame2.pack()
operation_des.pack()
btn_search.pack(side = 'top')#顯示btn
anime_name_label.pack()#顯示Label
show_label.pack()
imageLabel.pack()


win.mainloop()

