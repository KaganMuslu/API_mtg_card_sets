from pydantic import BaseModel
import requests_html
from fastapi import FastAPI, Request, HTTPException
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory='templates')
app = FastAPI()
session = requests_html.HTMLSession()



class links(BaseModel):
    selected_link: str

    class Config:
        orm_mode = True



# FAST-API SECTION
@app.get('/')
def home():
    return {"data":'Magic the Gathering TCG Sets - Cards API'}


@app.get('/about')
def home():
    return {"data":'This API written by Kagan Muslu'}



# Son 20 Kart Seti
@app.get('/set/all')
def mtgsets():
    response = session.get('https://scryfall.com/sets')


    database = {}
    for x in range(20):
        set_name = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[1]/a')[0].text
        set_card_quantity = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[2]/a')[0].text
        set_date = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[3]/a')[0].text
        set_link = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[1]/a/@href')[0]
        
        database[x] = {'set_name':set_name, 'set_card_quantity':set_card_quantity, 'set_date':set_date, 'set_link':set_link}

    return database


# Seçilmiş Setin Bilgileri
# "selected_link" : "https://scryfall.com/sets/vow"
@app.get('/set/selected')
def selected_set(item: links):
    
        response = session.get(item.selected_link)
        database = {}


        while True:
            try:
                for x in range(9999):
                        
                    card_name = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a')[0].text
                    card_link = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a/@href')[0]
                    card_image_link = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a/div/div/img/@src')[0]

                    database[x] = {'card_name':card_name,'card_link':card_link, 'card_image_link':card_image_link}
            except:
                break
        return database



# Rasgele Kart Bilgileri 
@app.get('/card/random')
def random_card():
    response = session.get('https://scryfall.com/random')


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    try:
        card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    except:
        card_price = 'No Info'
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return {'card_name':card_name,'card_type':card_type, 'card_text':card_text,'card_price':card_price, 'card_image':card_image}




# Seçilmiş Kartın Bilgileri
# "selected_link": "https://scryfall.com/card/tneo/16/tamiyos-notebook"
@app.get('/card/selected')
def selected_card(item: links):

    response = session.get(item.selected_link)


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return {'card_name':card_name,'card_type':card_type, 'card_text':card_text,'card_price':card_price, 'card_image':card_image}




# Kart Arama
@app.get('/card/{searching}')
def search(searching: str):

    response = session.get('https://scryfall.com/search?q='+searching)
    database = {}

    while True:
        try:
            for x in range(9999):
                if x == 0:
                    x += 1
                    
                card_name = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{x}]/a')[0].text
                card_image_link = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{x}]/a/div/div/img/@src')[0]

                database[x] = {'card_name':card_name, 'card_image_link':card_image_link}

        except:

            if len(database) > 0:
                return database
            else:
                try:                    

                    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
                    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
                    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
                    try:
                        card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
                    except:
                        card_price = 'No Info'
                    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

                
                    return {'card_name':card_name,'card_type':card_type, 'card_text':card_text,
                                    'card_price':card_price, 'card_image':card_image}
                except:
                    raise HTTPException(status_code=404, detail=f"'{searching}' not found!")



##HTML PAGES

# Seçilmiş Kartın Bilgilerini HTML'de Gösterme
# "selected_link": "https://scryfall.com/card/tsr/76/mystical-teachings"
@app.get('/card/selected/html')
def selected_card_html(request: Request, item: links):

    response = session.get(item.selected_link)


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return templates.TemplateResponse('random.html', {"request": request, 'card_name':card_name,'card_type':card_type,
                                            'card_text':card_text,'card_price':card_price, 'card_image':card_image})



# Rastgele Seçilen Kartın Bilgilerini HTML'de Gösterme
@app.get('card/random/html')
def random_card_html(request: Request):
        
    response = session.get('https://scryfall.com/random')


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    try:
        card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    except:
        card_price = 'No Info'
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return templates.TemplateResponse('random.html', {"request": request, 'card_name':card_name,'card_type':card_type,
                                                'card_text':card_text,'card_price':card_price, 'card_image':card_image})



# Aranan Kartın Bilgilerini HTML'de Gösterme
@app.get('card/{searching}/html')
def search_html(request: Request, searching: str):

    response = session.get('https://scryfall.com/search?q='+searching)
    database = {}


    while True:
        try:
            for x in range(9999):
                    
                card_name = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{x+1}]/a')[0].text
                card_image_link = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{x+1}]/a/div/div/img/@src')[0]

                database[x] = {'card_name':card_name, 'card_image_link':card_image_link}
        except:
            
            if len(database) > 0:
                txt = open('templates\search_html.html', 'w')
                txt.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible"')
                txt.write('content="IE=edge"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head>')
                txt.write('<body><table style="border-collapse: collapse; width: 100%;" border="0"><tbody><tr>')
                

                while True:
                    try:
                        for y in range(9999):
                            card_name = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{y+1}]/a')[0].text
                            card_link = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{y+1}]/a/@href')[0]

                            card_image_link = response.html.xpath(f'//*[@id="main"]/div[3]/div/div[{y+1}]/a/div/div/img/@src')[0]


                            if y % 4 == 0:
                                txt.write("</tr><tr>")
                            txt.write(f'<td style="width: 33%;"><a href={card_link} target="_blank"><img src="{card_image_link}" title="{card_name}" width="270"/></td>')


                    except:
                        txt.write('</tr> </table></body> </html>')
                        txt.close()
                        return templates.TemplateResponse('search_html.html', {"request": request})

            else:
                try:                    

                    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
                    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
                    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
                    try:
                        card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
                    except:
                        card_price = 'No Info'
                    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

                
                    return templates.TemplateResponse('random.html', {"request": request, 'card_name':card_name,'card_type':card_type,
                                        'card_text':card_text,'card_price':card_price, 'card_image':card_image})
                except:
                    raise HTTPException(status_code=404, detail=f"'{searching}' not found!")



# Seçilmiş Setin Bilgilerini HTML'de Gösterme
# "selected_link":"https://scryfall.com/sets/nec"
@app.get('/set/selected/html')
def selected_set_html(request: Request, item: links):

    txt = open('templates\set.html', 'w')
    txt.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge">')
    txt.write('<meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Document</title></head><body><table')
    txt.write('style="border-collapse: collapse; width: 100%;" border="0"><tbody><tr>')
    
    
    
    response = session.get(item.selected_link)

    while True:
        try:
            for x in range(9999):
                    
                card_name = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a')[0].text
                card_link = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a/@href')[0]
                card_image_link = response.html.xpath(f'//*[@id="main"]/div[2]/div/div[{x+1}]/a/div/div/img/@src')[0]


                if x % 4 == 0:
                    txt.write("</tr><tr>")
                txt.write(f'<td style="width: 33%;"><a href={card_link} target="_blank"><img src="{card_image_link}" title="{card_name}" width="270"/></td>')


        except:
            txt.write('</tr> </table></body> </html>')
            txt.close()
            return templates.TemplateResponse('set.html', {"request": request})
