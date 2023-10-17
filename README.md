
# Magic: The Gathering (MTG) Cards and Sets - API

Bu projenin amacı, [Magic: The Gathering (MTG)](https://magic.wizards.com/en) adlı popüler bir kart oyununda kullanılan kart setlerinin ve bu setlerde yer alan kartların özelliklerinin  [FastAPI](https://fastapi.tiangolo.com) aracılığıyla erişilebilir hale getirilmesidir.

Veri Kaynağı olarak hazır bir dataset kullanmayarak Python'un [requests_html](https://requests.readthedocs.io/projects/requests-html/en/latest/) modülü ile ["Scryfall.com"](https://scryfall.com/) adlı websitesinden webscraping yapılmıştır.

Bu API, kullanıcılara MTG kart setlerinin isimleri, yayın tarihleri, kart sayısı gibi bilgileri ve her kartın adı, tipi, maliyeti, atak ve defans puanları gibi özelliklerini sunar. Kullanıcılar bu API'yi kullanarak, MTG kart setlerini araştırabilir, bir setin hangi kartları içerdiğini öğrenebilir veya belirli bir özellikteki kartları filtreleyebilirler.

Bu proje, MTG hayranları için bir veri kaynağı sağlamayı amaçlar ve bu verileri kullanarak uygulamalar, web siteleri veya MTG kart koleksiyonu yöneticileri oluşturmak isteyen geliştiricilere kolaylık sağlar.


## API Kullanımı

#### Son 20 Kart Seti

```
  GET /set/all
```

#### Seçilmiş Setin Bilgileri

```
  GET /set/selected
  {"selected_link" : "https://scryfall.com/sets/vow"}
```

#### Rasgele Kart Bilgileri 

```
  GET /card/random
```

#### Seçilmiş Kartın Bilgileri

```
  GET /card/selected
  {"selected_link" : "https://scryfall.com/card/tneo/16/tamiyos-notebook"}
```

#### Kart Arama

```
  GET /card/{searching}
```
#### HTML Kısmı


#### Seçilmiş Kartın Bilgilerini HTML'de Gösterme

```
  GET /card/selected/html
  {"selected_link": "https://scryfall.com/card/tsr/76/mystical-teachings"}
```

#### Rastgele Seçilen Kartın Bilgilerini HTML'de Gösterme

```
  GET /card/random/html
```

#### Aranan Kartın Bilgilerini HTML'de Gösterme

```
  GET /card/{searching}/html
```

#### Seçilmiş Setin Bilgilerini HTML'de Gösterme

```
  GET /set/selected/html
  {"selected_link":"https://scryfall.com/sets/nec"}
```

![Ekran görüntüsü 2023-10-17 152200](https://github.com/KaganMuslu/API_mtg_card_sets/assets/71410113/5ebe8351-b5ba-429f-a700-43a68adcd1b4)

![random](https://github.com/KaganMuslu/API_mtg_card_sets/assets/71410113/0ab41cc2-a14c-439f-a8ad-888787409da5)




