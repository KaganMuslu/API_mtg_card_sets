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
    return {"data":'Magic the Gathering TCG Sets-Cards App --written by Kagan Muslu'}


@app.get('/about')
def home():
    return {"data":'This API written by Kagan Muslu'}




@app.get('/random_card')
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




@app.get('/mtgsets')
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




@app.get('/search/{searching}')
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




#"selected_link" : "https://scryfall.com/sets/vow"
@app.post('/selected_set')
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




#selected_link = 'https://scryfall.com/card/tneo/16/tamiyos-notebook'
@app.post('/selected_card')
def selected_card(item: links):

    response = session.get(item.selected_link)


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return {'card_name':card_name,'card_type':card_type, 'card_text':card_text,'card_price':card_price, 'card_image':card_image}




#HTML PAGES
#selected_link = 'https://scryfall.com/card/tsr/76/mystical-teachings'
@app.post('/selected_card_html')
def selected_card_html(request: Request, item: links):

    response = session.get(item.selected_link)


    card_name = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/h1')[0].text
    card_type = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/p[1]')[0].text
    card_text = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[3]/div/div[1]')[0].text
    card_price = response.html.xpath(f'//*[@id="stores"]/ul/li[1]/a/span')[0].text
    card_image = response.html.xpath(f'//*[@id="main"]/div[1]/div/div[1]/div[1]/img/@src')[0]

    
    return templates.TemplateResponse('random.html', {"request": request, 'card_name':card_name,'card_type':card_type,
                                            'card_text':card_text,'card_price':card_price, 'card_image':card_image})




#selected_set_link = 'https://scryfall.com/sets/mid'
@app.get('/mtgsets_html')
def mtgsets_html(request: Request):
    
    """response = session.get('https://scryfall.com/sets')


    txt = open('templates\sets.html', 'w')
    txt.write('<table style="border-collapse: collapse; width: 65.8407%; height: 397px; margin-left: auto; margin-right: auto;" border="1"><tbody>')
    txt.write('<tr><th style="width: 32.3894%;">NAME</th><th class="em6" style="width: 37.6991%;">CARDS</th><th class="em9" style="width: 29.7345%;">DATE</th></tr>')


    for x in range(9999):
        set_name = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[1]/a')[0].text
        set_card_quantity = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[2]/a')[0].text
        set_date = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[3]/a')[0].text
        set_link = response.html.xpath(f'//*[@id="js-checklist"]/tbody/tr[{x+1}]/td[1]/a/@href')[0]
                

        # create
        new_link = f'<td style="width: 33.3333%; text-align: center;"><a href={set_link}>{set_name}</td>'
        new_link2 = f'<td style="width: 33.3333%; text-align: center;">{set_card_quantity}</td>'
        new_link3 = f'<td style="width: 33.3333%; text-align: center;">{set_date}</td>'
        
        # insert
        txt.write("<tr>")
        txt.write(new_link)
        txt.write(new_link2)
        txt.write(new_link3)
        txt.write("</tr>")


    txt.write('</tbody></table>')
    txt.close()"""
    return templates.TemplateResponse('sets.html', {"request": request})




@app.get('/random_card_html')
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




@app.get('/search_html/{searching}')
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





@app.post('/selected_set_html')
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
