# Bahamut-Anime-Analysis
A system to introduce upcoming anime on this website : 動畫瘋, provided with interactive graphical user interface(GUI).  
(巴哈姆特動畫瘋動漫新番之分析 )

# Overview 

introduction PPT: [Bahamut-Anime-Analysis.pptx](https://github.com/wei-0321/Bahamut-Anime-Analysis/files/7360276/Bahamut-Anime-Analysis.pptx)


I collected data from the website named "動畫瘋", which is an anime streaming platform in Taiwan. 

Here is a brief introduction to this website.

(website homepage)
![巴哈1](https://user-images.githubusercontent.com/71260071/135490391-94df339e-a4ea-4d51-b41e-38c09f353bb2.PNG)

(choose any anime you want to see, then enjoy watching anime)

![image](https://user-images.githubusercontent.com/71260071/137641367-37315629-0a09-42d7-80f5-fe9808f16187.png)

For anime enthusiasts, is's important to decide which anime to watch.

So I built a system with GUI to sort out the information(e.g., total vies, user ratings) of upcoming anime, as a criteria.

Below are some demo pictures about this system:

This UI was built with tkinter package.
At first, this system will rank upcoming anime based on total views and show result on the left side list.
![巴哈2](https://user-images.githubusercontent.com/71260071/135490449-60357790-fe34-4739-8094-60da5d7a904f.PNG)

Choose one of the anime on the left side list, then click the green button named "顯示詳細資訊".
After that, you will get to see the information of the chosen anime in detail.

You can also see the histogram showing views per eposide to analysis the trend of views.
![巴哈4](https://user-images.githubusercontent.com/71260071/135491268-8d78c5c9-9a2d-4da7-bbee-56db93e2b858.PNG)


# Requirements 
packages:
- tkinter
- io
- pillow
- matplotlib
- request
- beautifulsoup4

# Usage 

1.Open git bash. 

2.Change the diretory where you want to do download this repository.
```
> cd (your directory)
```
3.Clone this repository. 
```
> git clone https://github.com/wei-0321/Bahamut-Anime-Analysis.git
```
4.Change the diretory to this repository.
```
> cd Bahamut-Anime-Analysis
```
5.Execute the program.
```
> python main.py
```


# Project Structure
```
(Path)                                	(Description)
Bahamut-Anime-Analysis    	          Main folder     
│  │
│  ├ image                              Images for UI
│  │ │
│  │ ├ XXX.png
│  │ │
│  │ ├ ...
│  │ 
│  ├ web_scraping_package               a package for web scraping
│  │ │
│  │ ├ __init__.py
│  │ │
│  │ ├ scraping.py                      a module containing functions which extract data from the website.
│  │ 
│  ├ main.py                            Main program

