
# Magic: The Gathering (MTG) Cards and Sets - API

Bu projenin amacı, [Magic: The Gathering (MTG)](https://magic.wizards.com/en) adlı popüler bir kart oyununda kullanılan kart setlerinin ve bu setlerde yer alan kartların özelliklerinin  [FastAPI](https://fastapi.tiangolo.com) aracılığıyla erişilebilir hale getirilmesidir.

Veri Kaynağı olarak hazır bir dataset kullanmayarak Python'un [requests_html](https://requests.readthedocs.io/projects/requests-html/en/latest/) modülü ile ["Scryfall.com"](https://scryfall.com/) adlı websitesinden webscraping yapmaktayım.

Bu API, kullanıcılara MTG kart setlerinin isimleri, yayın tarihleri, kart sayısı gibi bilgileri ve her kartın adı, tipi, maliyeti, atak ve defans puanları gibi özelliklerini sunar. Kullanıcılar bu API'yi kullanarak, MTG kart setlerini araştırabilir, bir setin hangi kartları içerdiğini öğrenebilir veya belirli bir özellikteki kartları filtreleyebilirler.

Bu proje, MTG hayranları için bir veri kaynağı sağlamayı amaçlar ve bu verileri kullanarak uygulamalar, web siteleri veya MTG kart koleksiyonu yöneticileri oluşturmak isteyen geliştiricilere kolaylık sağlar.


## API Kullanımı

#### Son 20 Kart Seti

```
  GET /mtgsets
```

#### Seçilmiş Setin Bilgileri

```
  GET /selected_set
  {"selected_link" : "https://scryfall.com/sets/vow"}
```

#### Rasgele Kart Bilgileri 

```
  GET /random_card
```

#### Seçilmiş Kartın Bilgileri

```
  GET /selected_card
  {"selected_link" : "https://scryfall.com/card/tneo/16/tamiyos-notebook"}
```

#### Kart Arama

```
  GET /search/{searching}
```
#### HTML Kısmı


#### Seçilmiş Kartın Bilgilerini HTML'de Gösterme

```
  GET /selected_card_html
  {"selected_link": "https://scryfall.com/card/tsr/76/mystical-teachings"}
```

#### Rastgele Seçilen Kartın Bilgilerini HTML'de Gösterme

```
  GET /random_card_html
```

#### Aranan Kartın Bilgilerini HTML'de Gösterme

```
  GET /search_html/{searching}
```

#### Seçilmiş Setin Bilgilerini HTML'de Gösterme

```
  GET /selected_set_html
  {"selected_link":"https://scryfall.com/sets/nec"}
```



