from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import smtplib
import pandas

custom_url = "https://www.flipkart.com/search?q=phones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off";

client = Request(custom_url, headers={'User-Agent': 'Mozilla/5.0'})
page = urlopen(client).read();
page_soup = soup(page, "html.parser")
# bhgxx2 col-12-12
itemList = page_soup.findAll("div", {"class": "bhgxx2 col-12-12"})
# <div class="_3wU53n">Realme 5i (Forest Green, 64 GB)</div>
#<div class="_1vC4OE _2rQ-NK">₹10,999</div>
print(len(itemList))
df = pandas.DataFrame(columns=["Model Name", "Model Price", "Model Specs"])
for item in itemList:
    if (item.find("div", {"class": "_3wU53n"}) is not None):

        specs=item.findAll("li", {"class": "tVe95H"});

        df = df.append({"Model Name": item.find("div", {"class": "_3wU53n"}).text,
                        "Model Price": item.find("div", {"class": "_1vC4OE _2rQ-NK"}).text[1:],
                        "Model Specs":specs[0].text+("\n")+(specs[1].text)+("\n")+(specs[2].text)
                        +("\n") + (specs[2].text) + ("\n") + (specs[3].text)},
                       ignore_index=True)

        #print(item.find("div", {"class": "_3wU53n"}).text , 'price ' , item.find("div", {"class": "_1vC4OE _2rQ-NK"}).text , ' spces ' , item.findAll("li", {"class": "tVe95H"})[0].text)

print(df)
df.to_csv("phonelist.csv", sep=',', index=None, header=True)