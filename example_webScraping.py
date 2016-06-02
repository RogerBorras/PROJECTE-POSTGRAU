import urllib2
import re
#import time

# DONADA UNA URL (url_page) I UN DICCIONARI (data)
# LA FUNCIO extract_page AFEGEIX AL DICCIONARI LA INFORMACIO DELS INMOBLES DE LA URL 
# LES CLAUS SERAN EL ID DE CADASCUN DELS INMOBLES (EL ID ES UNIC)
# PER A CADA INMOBLE ES GUARDA: PREU, METRES QUADRATS I COORDENADES
def extract_page(url_page, data):
    
    # ES LLEGEIX EL CODI FONT DE LA URL
    code_page = urllib2.urlopen(url_page).read()
    
    # ES DIVIDEIX EL CODI DE LA URL DONADA PELS ID DE TOTS ELS INMOBLES
    # ES CREEN N+1 PARTICIONS (ON N ES EL TOTAL D'INMOBLES D'AQUELLA PAGINA)
    list_id_inmuebles = re.findall("<a href=\"/inmueble/\d+/\"", code_page)
    split_id_inmuebles = re.split("<a href=\"/inmueble/\d+/\"", code_page)
    
    # id_inmuebles CONTE ELS ID DELS N INMOBLES (UNICAMENT NUMEROS)
    # LA URL CORRESPONENT A UN ID ES: "http://www.idealista.com/inmueble/ID/"
    id_inmuebles = []
    for inmueble in list_id_inmuebles:
        id_inmuebles.append(re.search("\d+", inmueble).group())
      
    # A CADA DIVISIO DEL CODI FONT ON ESTAN ELS N ANUNCIS
    # ES CONSULTA EL PREU I ELS METRES QUADRATS DE CADASCUN DELS INMOBLES
    for i in range(1,len(split_id_inmuebles)):
        # DESPRES DE LA PARAULA item-price ES GUARDEN DES DE 3 A 11 CARACTERS (FINS QUE S'ESCRIU <span>)
        # NO ES POSA \d+.\d+ PERQUE SI EL PREU ES SUPERIOR A 999.999e ALESHORES FALTARIEN DIGITS (I UN PUNT)
        text_price = re.search("<span class=\"item-price\">.{3,11}<span>", split_id_inmuebles[i]).group()
        price = re.search("\d+.*\d+", text_price).group()
        # DESPRES DE LA PARAULA item-detail ES GUARDEN ELS DIGITS QUE APAREIXEN (MINIM 1) FINS <small>m
        # S'AFEGEIX QUE ACABI EN m PERQUE ES EL INDICADOR QUE SON METRES (EL QUADRAT NO HO IDENTIFICA) 
        text_size = re.search("<span class=\"item-detail\">\d?\.?\d+ <small>m", split_id_inmuebles[i]).group()
        size = re.search("\d?\.?\d+", text_size).group()
        # ES GUARDEN ELS DOS VALORS ANTERIORS (price I size) EN EL DICCIONARI (LA CLAU ES EL ID DEL INMOBLE)
        # NOTA: EL TEXT "i" CORRESPON AL ID "i-1", JA QUE EL PRIMER TEXT NO CORRESPON A CAP ID (INICIA EN 1)
        # data[id_inmuebles[i-1]] = [price, size] # S'INTRODUEIXEN ELS VALORS COM STRING
        price_int = int(price.replace(".",""))
        size_int = int(size.replace(".",""))
        # data[id_inmuebles[i-1]] = [price_int, size_int] # S'INTRODUEIXEN ELS VALORS COM INT
        data[id_inmuebles[i-1]] = [price_int, size_int, round(price_int/float(size_int),2)] # S'AFEGEIX EL PREU DEL METRE
    
    # PER A CADASCUN DELS INMOBLES ES CONSULTA EL CODI FONT DEL SEU ANUNCI I S'EXTREUEN LES COORDENADES
    # A DIFERENCIA DE PREU/METRES AQUESTA INFORMACIO NO ES POT EXTREURE DE LA PAGINA ON ESTAN TOTS ELS ANUNCIS
    for inmueble in id_inmuebles:
        # ES CONSTRUEIX LA URL A PARTIR DEL ID I S'OBTE EL CODI FONT DE LA PAGINA
        url = "http://www.idealista.com/inmueble/" + inmueble + "/"
        code_inmueble = urllib2.urlopen(url).read()
        # ES LLEGEIXEN LES COMPONENTS X Y DE LES COORDENADES I S'AFEGEIXEN AL DICCIONARI (COM UNA LLISTA DE 2 ELEMENTS) 
        coord = re.search("latitude:\"\d+.\d+\",longitude:\"\d+.\d+\"", code_inmueble).group()
        coordxy = re.split(",", coord)
        coordx = re.search("\d+.\d+", coordxy[0]).group()
        coordy = re.search("\d+.\d+", coordxy[1]).group()
        data[inmueble].append([coordx, coordy])
        
        # AFEGIR UNA PAUSA 
        #time.sleep(3)
    
    # EN TOTAL, CADA ELEMENT DE DATA TE 4 ELEMENTS: PREU - METRES - PREU METRE QUADRAT - COORDENADES
    # A LA VEGADA, COORDENADES ES UNA LLISTA AMB 2 ELEMENTS (COORDENADA X I COORDENADA Y) 
    return data