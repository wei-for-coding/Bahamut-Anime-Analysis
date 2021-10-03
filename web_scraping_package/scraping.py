import io
import requests                    #使用requests模組建立各種HTTP 請求
from bs4 import BeautifulSoup      #使用Beautiful Soup模組可以快速解析網頁HTML碼
import matplotlib.pyplot as plt    #視覺化模組
from PIL import Image


def get_soup(url):     #對網頁提出要求  並依照得到的回應建立BeautifulSoup物件  方便剖析網頁
    url_headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    r = requests.get(url, headers = url_headers)  #對網頁提出要求
    soup = BeautifulSoup(r.text, "lxml")          #建立BeautifulSoup物件
    return soup


def to_number(string):   #將觀看數全部統一為數值(例如:30萬 => 300000)
    number = 0
    if string[-1] == "萬":     
        number = int(float(string[0 : -1]) * 10000)
    else:
        number = int(string)
    return number


def plot(x, y):      #畫出每集觀看數的圖表
    #字形設定
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False

    figure = plt.figure(figsize=(9, 5))    
    plt.style.use("seaborn-deep")
    plt.bar(x, y)
    plt.title("每集觀看數", fontsize = 20)
    plt.xticks(rotation = 45)  #將標籤旋轉 避免重疊
    plt.xlabel("集數", fontsize = 15)
    plt.ylabel("觀看數", fontsize = 15)
    return figure


def fig_to_img(fig):
    """
    Convert a Matplotlib figure to a PIL Image in RGB format
    parameter fig : a matplotlib figure
    return : a Python Imaging Library ( PIL ) image
    """
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    image = Image.open(buf)
    return image


def get_rank():
    result_list = []
    
    soup = get_soup("https://ani.gamer.com.tw")
    tag_views = soup.find("div", attrs = {"class", "newanime-wrap normal-ver newanime-content-hide"})
    #找到全部動漫名稱的標籤
    tag_anime_name = tag_views.find_all("p", attrs = {"class", "anime-name_for-marquee"}) 
    #找到全部總觀看次數的標籤
    tag_watch_number = tag_views.find_all("div", attrs = {"class", "anime-watch-number"})  
    rank = 0            #人氣排名(因為已經依照觀看人數排序，所以不用特別處理)
    anime_name_list = []
    for i in range(len(tag_anime_name)):
        result = ""
        rank += 1
        result += "---第" + str(rank) + "名---"
        anime_name = tag_anime_name[i]
        name = anime_name.text
        if (name not in anime_name_list):   #要過濾重複名稱的動漫  沒跟之前重複的就進行處理
            anime_name_list.append(name)
            result += "   名稱 : " + name
            watch_number = tag_watch_number[i].find("p")
            if watch_number.text == "統計中":             #若觀看數還在統計中，先預設觀看數為0
                number = 0
                result += "   總觀看次數 : 0(正在統計中)"
            else:
                number = to_number(watch_number.text)     #將總觀看數全部統一為數值
                result += "   總觀看次數 : " + str(number) + "次 "  
            result_list.append(result)
    return result_list


def get_main_url():
    result_list = []
    
    soup = get_soup("https://ani.gamer.com.tw")
    tag_views = soup.find("div", attrs = {"class", "newanime-wrap normal-ver newanime-content-hide"})
    #找到全部動漫名稱的標籤
    tag_anime_name = tag_views.find_all("p", attrs = {"class", "anime-name_for-marquee"}) 
    #找到全部動漫的影片網址
    tag_anime_url = tag_views.find_all("div", attrs = {"class", "anime-block"})            
    anime_name_list = []
    for i in range(len(tag_anime_name)):
        anime_name = tag_anime_name[i]
        name = anime_name.text
        if (name not in anime_name_list):   #要過濾重複名稱的動漫  沒跟之前重複的就進行處理
            anime_name_list.append(name)
            tag_a = tag_anime_url[i].find("a")    #最新一集影片的網址
            url = "https://ani.gamer.com.tw/" + tag_a.attrs["href"]
            result_list.append(url)
    return result_list
        
        
def get_detail(index, main_url_list):
    result = ""
    
    soup = get_soup(main_url_list[index])
    tag_type = soup.find("ul",attrs={"class", "data_type"})   #電影簡介
    per_data_type = tag_type.find_all("li")   
    for i in range(len(per_data_type)):   
        string = per_data_type[i].text
        strlist = list(string)
        strlist.insert(4," : ")
        strlist_string = "".join(strlist)
        result += strlist_string + "\n"
    tag_score = soup.find("div", attrs={"class", "ACG-score"})   #觀眾評分
    tag_score_div = tag_score.find("span")
    for i in range(len(tag_score.text)):
        str1 = tag_score.text
        str2 = tag_score_div.text
        if str1[i : i + len(str2)] == str2:
            score = str1[0 : i]
            break
    if score == "--":
        result += "觀眾評分 : 尚未有人評分\n"
    else:
        result +=  "觀眾評分 : " + score + "分\n"
   
    tag_feature = soup.find("div", attrs={"class", "ACG-data"}).find("li")   #最大賣點 
    feature = tag_feature.text
    result += "觀眾喜歡這部動漫的原因 : " + feature + "\n"
    return result


def get_episode_view(index, main_url_list):
    episode_dict = {}        #動漫集數對應每集觀看人數的字典
    soup = get_soup(main_url_list[index])
    tag_episode = soup.find("section", attrs = {"class", "season"})   
    if tag_episode == None:  #如果沒有歷史集數  代表是電影  或是此動漫目前只有一集 將不採計
         #print(" 只有一集  故不統計")
         return None
    else:
        episodes = tag_episode.find_all("a")   #先找出每集的網址  再依據拿到的網址找尋每集觀看人數
        for episode in episodes:
            episode_number = episode.text
            each_url = "https://ani.gamer.com.tw/animeVideo.php" + episode.attrs["href"]
            #依照每集的網址  找尋各集的觀看人數
            episode_soup = get_soup(each_url)
            tag_episode_watch = episode_soup.find("span", attrs = {"class", "newanime-count"})
            episode_watch = tag_episode_watch.find("span") 
            if episode_watch.text != "統計中":    #若某集觀看數還在統計中  則不採計那集
                episode_watch_number = to_number(episode_watch.text)
                episode_dict.update({episode_number : episode_watch_number}) #將集數.每集觀看數加入字典
        if len(episode_dict.keys()) == 0:
            #print("  統計中...")
            return None
        else:
            #畫圖的前置準備
            episode_number_list = []
            episode_watch_number_list = []
            #從動漫集數對應每集觀看人數的字典中 分別拿出集數.每集觀看人數
            for key in episode_dict.keys():        #先截取集數 放進串列裡面
                episode_number_list.append(key)
            for value in episode_dict.values():    #再擷取每集的觀看人數 放進串列
                episode_watch_number_list.append(value)
            figure = plot(episode_number_list, episode_watch_number_list)  #填入對應的x.y座標並畫圖
            image = fig_to_img(figure)
            return image

