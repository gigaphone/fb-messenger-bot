# -*- coding: cp1250 -*-

#import bot
#print "done bot import"
#from bot import get_bot
#from chatterbot import ChatBot

import json
import os
import sys
import traceback
from nltk.tokenize import word_tokenize

import requests
from flask import Flask, request

print "done all imports"

app = Flask(__name__)

print "assigned flask to app"

answers = {
    'pare': u'Sve pare �e da budu kod �ike',
    'cika': u'Ljubi �ika!',
    'ave': 'Ave Beli !',
    '5': 'Ave Beli ! 5 !',
    '#samojako': '#samojako',
    'jako': 'Samo Jako !',
    'sikiracija': 'Samo bez sikiracije',
    '#avebeli': '#avebeli',
    'belo': 'Tvoje belo nije dovoljno belo',
    'bez': 'Bez sikiranja',
    'ima': u'Ima za �iku, al ima i za druge.',
    'rad': u'Radim od rane zore, ve� od 8.',
    'kobre': u'voleo bih da me �uvaju �kobre� kad postanem predsednik.',
    'stan': u'Predsednik �e �iveti u vikendici u Mladenovcu',
    'vila': u'Vilu na Dedinju pokloni�emo najboljim studentima.',
    'cilj': u'Glavni cilj je da se domognemo predsedni�ke pozicije, a posle �emo da vidimo.',
    'tajkun': u'Ljubi�in tajkun je kum Petar Popovi� Ajkula',
    'sarma': u'Sarmu probo nisi.',
    'mrak': u'�ta se beli u mraku Srbije?',
    'glava': u'Samo jako uzdignute glave !',
    'doktorat': u'Idem po doktorat u korporativnom industrijskom menad�mentu, jer to je budu�nost.',
    'placenik': u'Idem na obuku za strane pla�enike, a dogovaramo i sastanak sa Trampom',
    'sumadija': u'Tokom programa bi�e obavljeni i va�ni razgovori o potencijalnim ulaganjima na�e dijaspore u AP �umadija',
    'zena': u'Kad postanem preCednik, ni jedna �ena ne sme biti izvre�ana.',
    'predskazan': u'Beli je predskazan ...',
    'prevaren': u'Da li je bilo ko od vas 12,640 kad je potpisao bio prevaren i nije znao da podr�ava Ljubi�u Preleta�evi�a Belog?',
    'rik': u'�ao mi je �to ste zabrinuti i ne verujete RIK-u.',
    'zemun': u'Zna�i uspeo sam da ispo�tujem Zemun. Ispo�tujte i vi brata. ',
    'sirotinja': u'Sirotinja uzvra�a udarac',
    'mart': u'�ene moje sre�an osmi mart. Ljubi �ika �i�arkice',
    'bot': u'Evo ponude: moji botovi po�etnici imaju jagnjetinu. Mogu�e napredovanje.',
    'paypal': u'PayPal account je  belisamojako@gmail.com  ',
    'saj': u'Do�li i SAJevci da pomognu skupljanje potpisa po Mladenovcu',
    'formula': u'Moja formula je jednostavna. Zna�i samo jako i bez sikiranja, bi�e sve ok. ;)',
    'godina': u'Da zavr�imo ovu godinu pa da krenemo Samo Jako u narednu !',
    'interes': u'Ja gledam da imam svoj li�ni interes, ali da dam i narodu. Su�tina je da �u krasti, da �u se vajditi, ali i da �u dati narodu. Tako treba raditi i tako smo namireni i mi i oni',
    'soros': u'Ko da vi�e love, taj je dobrodo�ao. Nebitno je ko finansira. Ko je spreman da ulo�i novac u ne�to �to je dobro, taj je dobrodo�ao.',
    'glasanje': u'Treba da iza�ete na izbore, jako je bitno. Dosta ste sedeli ku�i, ni�ta niste radili. Su�tina je da sada uradite ne�to novo i bitno, iza�ite 2. aprila na izbore i zaokru�ite broj pet � ; Ljubi�a Preleta�evi� Beli. Ljubi �ika, bez sikiranje',
    'kosovo': u'Izvolite, mo�ete da se vratite, ne samo vi, ve� i Bugarska, Gr�ka� Od Ma�arske do Gr�ke da se svi ujedinimo',
    'mmf': u'Ne znam ko to dr�i. Lepo �out�, izlazi� iz zemlje, a sva lova kod ��ike�. Narod zna da je lova kod mene, treba ti ne�to, do�e� kod mene, pita� treba mi za to i to, ja iske�iram sve iz d�epa, odem provjerim da li si to uradio i lijepo',
    'ljubi': u'Ljubi �ika, bez sikiranja',
    'loto': u'Loto je �ika Beli namestio. Dosta su drugi name�tali loto, sad malo �ika. Da usre�im kojeg Mladenov�anina, bi�e toga jo�. Ljubi predsednik.',
    'istokzapad': u'Radim za zapad i za istok. U zavisnosti kuda vi�e love, ja za njih radim, tako da je kod mene sve to promenljivo.',
    'kontrola': u'Nema tu kontrole, zna�i, mojih botova ima mnogo vi�e od ostalih stranaka i tu nema neke preterane kontrole, podelimo im te kapri�oze i oni se malo smire, ali opet krenu, mnogo su jaki, ko god krene na mene, oni me brane.',
    'krug': u'Sad idemo u krug, sad malo ja deset godina, pa �e neko drugi. Nema tu neke filozofije, razume�.',
    'iskreno': u'Pa zna� �ta je fora, �to bih ja ujedinio sve ljude. Svi da se volimo, da se grlimo, da nam bude svima lepo, da ne postoje granice, da nema NATO-a, i to je ono iskreno.',
    'drugi': u'Nema ni�ta od toga, prvi krug ja dobijam i to je to.',
    'dama': u' Postoji prva dama. Mislim ona nije jo� prva dama, ja kada postanem prvi predsednik, onda �u je uzeti za �enu.',
    'zelenas': u'Nema tu kancelarije, ti do�e� kod mene li�no, tra�i� od mene pare. Zna�i nema ti da tra�i� ni od koga drugog, pare �e da budu kod mene ku�i, ti do�e� kod mene pa tra�i� pare. Sad, ti si seljak �ovek ho�e� da poseje� njivu neku tamo, kupi� kombajn, do�e� kod mene i tra�i�, ja odem posle i proverim jesi li kupio i to je to. To je prosto.',
    'jezik': u'Dakle engleski, nema�ki, francuski.',
    'veselje': u'Napravi�u op�te narodno veselje. Napravi�emo 20 mangala za 20 bravova i op�te narodno veselje da proslavimo predsednikovu pobedu, onako narodski �to se ka�e.',
    'nikolic': u'Pa verovatno bolje igram od Nikolica, imam smisla za igranku, �ene ka�u da sam zgodan, tako da, za po�etak, i tri strana jezika, a spreman sam da nau�im jo� dva, mislim da je to za po�etak dovoljno.',
    'kruna': u'Verovatno �u imati prilike da upoznam predsednika kad bude predaja kruna.',
    'tempo': u'Evo ja ti prijatelju radim od 7 jutros, pa ti vidi sad koliko je to, zna�i mogu da izguram 22 sata da radim.',
    'arapi': u'Kad postanem predsednik ne�u da radim ni�ta, �ta ima da radim, da potpisujem tamo, da igram sa Arapima, da pe�em rakiju, da se �etam ambasadama. Sad da izguram ovo po 22 sata da radim i posle milina Bo�ija.',
    'istina': u'Kako ne�e, ljudima treba istina, niko nije bio iskren 20-30 godina, ja iza�em i ka�em, kao �to sam tebi rekao malopre, moj li�ni interes je na prvom mestu, pa onda drugi, ali ja �u davati i njima.',
    'srdja': u'Ja sam i�ao na privatne �asove kod Sr�e, 1000 dinara po �asu je bilo i uz to mi je matematiku predavao, jedan od koeficijenata je 2, to ti je dovoljno da bude� predsednik dr�ave. Tako da to je sve po tom principtu.',
    'kabinet': u'Vidi� da ja �irim ljubav, nema haosa. Ja ne �elim ljude na ulici, �elim sebe u predsedni�kom kabinetu.',
    'lgbt': u'To je ono �to ti ka�em, zna�i ako je potrebno i to da se uradi samo da ja postanem predsednik, nije nikakav problem. �to se mene ti�e mogu goli ljudi da �etaju ulicama, ako �u ja da budem presednik dr�ave. Samo za taj li�ni interes, �ta god, treba da se uradi. Samo da se do�e do cilja.',
    'ujedini': u'Pa ja bih potpisao da se ujedinimo svi komplet od Ma�arske dole do Gr�ke. Sve ako mo�e da se to ujedini u jednu zemlju, bez razmi�ljanja. Niko da se ne otcepljuje.',
    'golf': u'Golf �dvica�, 1.6 td, 86. godi�te, zna�i jednom mi je nestalo goriva dole na primorju sipao sam karton zejtina, je li veruje� da je dogurao do Beograda?',
    'referendum': u'Ko vi�e nudi love, prijatelju, tamo treba da idemo. Sad da li to bila Evropska unija ili unija Azije i Severne Koreje, to je nebitno. Ja to ka�em, da ne bude da je moje mi�ljenje, referendum pa nek narod odlu�i. Po�teno.',
    'jeremic': u'Divan momak, stvarno legendica, divan de�ak, radi svoj posao kako treba.',
    'jankovic': u'Fin momak i Sa�a je stvarno fin de�ak. On je bio be�e za�titnik gra�ana, to nije lo�a funkcija.',
    'radulovic': u'Odu�evio me �ovek �to je pozivao da ljudi potpi�u za nas, hvala mu za to.',
    'bosko': u'Bo�ko je momak i po. Ne pratim ne�to njegove politi�ke aktivnosti, ali ovako je stvarno fin �ovek.',
    'gandalf': u'Gandalf Beli. Rekao je Tarabi� da �e da do�e �ovek na belom konju, ne znam da li je rekao u belom odelu. Ali belo kao �isto ne�to je prepoznatljivo.',
    'preletacevic': u'Nijedan se ne preziva Preleta�evi� osim mene. Ja opet u svom prezimenu imam iskrenost, razume�, ja ka�em da sam Preleta�evi�. To je su�tina.',
}

qa_dict = {
    'pare': answers['pare'],
    'kes': answers['pare'],
    u'ke�': answers['pare'],
    'lova': answers['pare'],
    'brinem': answers['sikiracija'],
    'sikiram': answers['sikiracija'],
    'sekiram': answers['sikiracija'],
    'mislim': answers['sikiracija'],
    'srce': answers['ljubi'],
    'cao': answers['ljubi'],
    u'�ao': answers['cika'],
    'ajd': answers['cika'],
    'vidimo se': answers['cika'],
    'pozdrav': answers['ljubi'],
    'ziveo': answers['ave'],
    'izbori': answers['5'],
    'udri': answers['jako'],
    'rokaj': answers['jako'],
    'kako': answers['jako'],
    'pobeda': answers['jako'],
    'jako': answers['jako'],
    '#samojako': answers['#avebeli'],
    '#avebeli': answers['#samojako'],
    'belo': answers['belo'],
    'odelo': answers['belo'],
    'bez': answers['bez'],
    'pet': answers['5'],
    '5eli': answers['5'],
    'ave': answers['#avebeli'],
    'ima': answers['ima'],
    'ljubim': answers['cika'],
    'rad': answers['rad'],
    'kobra': answers['kobre'],
    'zmija': answers['kobre'],
    'poskok': answers['kobre'],
    'stan': answers['stan'],
    'kuca': answers['stan'],
    'vila': answers['vila'],
    'dedinje': answers['vila'],
    'student': answers['vila'],
    'cilj': answers['cilj'],
    'posle': answers['cilj'],
    'tajkun': answers['tajkun'],
    'placenik': answers['placenik'],
    'ajkula': answers['tajkun'],
    'sarma': answers['sarma'],
    'spn': answers['sarma'],
    'glava': answers['glava'],
    'doktorat': answers['doktorat'],
    'diploma': answers['doktorat'],
    'izdajnik': answers['placenik'],
    'sumadija': answers['sumadija'],
    'zena': answers['zena'],
    'predskazan': answers['predskazan'],
    'proreknut': answers['predskazan'],
    'tarot': answers['predskazan'],
    'sudbina': answers['predskazan'],
    'potpisi': answers['prevaren'],
    'prevara': answers['prevaren'],
    'podrska': answers['prevaren'],
    'rik': answers['rik'],
    'zabrinut': answers['sikiracija'],
    'zemun': answers['zemun'],
    'munze': answers['zemun'],
    'sirotinja': answers['sirotinja'],
    'siromah': answers['sirotinja'],
    'leba': answers['sirotinja'],
    'mart': answers['mart'],
    'bot': answers['bot'],
    'botovi': answers['bot'],
    'paypal': answers['paypal'],
    'uplata': answers['paypal'],
    'saj': answers['saj'],
    'formula': answers['formula'],
    'recept': answers['formula'],
    'godina': answers['godina'],
    'interes': answers['interes'],
    'kradja': answers['interes'],
    'vajda': answers['interes'],
    'ovajdi': answers['interes'],
    'soros': answers['soros'],
    'finansira': answers['soros'],
    'glasa': answers['glasanje'],
    'izbor': answers['glasanje'],
    'zaokruzi': answers['glasanje'],
    'kosovo': answers['kosovo'],
    'mmf': answers['mmf'],
    'monetarni': answers['mmf'],
    'kredit': answers['mmf'],
    'pozajmica': answers['mmf'],
    'pozajmi': answers['mmf'],
    'dug': answers['mmf'],
    'dugovanja': answers['mmf'],
    'loto': answers['loto'],
    'lutrija': answers['loto'],
    'istok': answers['istokzapad'],
    'zapad': answers['istokzapad'],
    u'radi�': answers['rad'],
    'jutro': answers['rad'],
    'komunist': answers['istokzapad'],
    'stranci': answers['istokzapad'],
    'kontrola': answers['kontrola'],
    'pica': answers['bot'],
    'sendvic': answers['bot'],
    'krug': answers['krug'],
    'organizacija': answers['kontrola'],
    'filozofija': answers['krug'],
    'ujedinio': answers['iskreno'],
    'iskreno': answers['iskreno'],
    'nato': answers['iskreno'],
    'alijansa': answers['iskreno'],
    'drugi': answers['drugi'],
    'dama': answers['dama'],
    u'�enidba': answers['dama'],
    'zenidba': answers['dama'],
    'zene': answers['dama'],
    'devojku': answers['dama'],
    'ozeni': answers['dama'],
    u'�eni�': answers['dama'],
    'zenis': answers['dama'],
    'zelenas': answers['zelenas'],
    'njivu': answers['zelenas'],
    'kombajn': answers['zelenas'],
    'jezik': answers['jezik'],
    'engleski': answers['jezik'],
    'nemacki': answers['jezik'],
    'francuski': answers['jezik'],
    'veselje': answers['veselje'],
    'pobede': answers['veselje'],
    'slavlje': answers['veselje'],
    'proslava': answers['veselje'],
    'nikolic': answers['nikolic'],
    u'nikoli�': answers['nikolic'],
    'kruna': answers['kruna'],
    'predsednik': answers['kruna'],
    'tempo': answers['tempo'],
    'jutros': answers['tempo'],
    'ustao': answers['tempo'],
    'rano': answers['tempo'],
    'arapi': answers['arapi'],
    'rakiju': answers['arapi'],
    'ambasada': answers['arapi'],
    'istina': answers['istina'],
    'srdja': answers['srdja'],
    u'sr�a': answers['srdja'],
    'casovi': answers['srdja'],
    u'�asovi': answers['srdja'],
    u'u�i': answers['srdja'],
    'haos': answers['kabinet'],
    'ulici': answers['kabinet'],
    'ljubav': answers['kabinet'],
    'lgbt': answers['lgbt'],
    'parada': answers['lgbt'],
    'prajd': answers['lgbt'],
    'ujedini': answers['ujedini'],
    'ujedinimo': answers['ujedini'],
    'golf': answers['golf'],
    'auto': answers['golf'],
    'kola': answers['golf'],
    'aktivisti': answers['bot'],
    'referendum': answers['referendum'],
    'glasanje': answers['referendum'],
    u'odlu�i': answers['referendum'],
    'odluci': answers['referendum'],
    'unija': answers['referendum'],
    'jeremic': answers['jeremic'],
    'vuk': answers['jeremic'],
    'jankovic': answers['jankovic'],
    'radulovic': answers['radulovic'],
    'bosko': answers['bosko'],
    'obradovic': answers['bosko'],
    'gandalf': answers['gandalf'],
    u'tarabi�': answers['gandalf'],
    'preletacevic': answers['preletacevic'],
    u'preleta�evi�': answers['preletacevic']
}


import distance
def answer(message):
    message = message.lower()
    try:
        count = 0
        smallest_distance = 999
        closest_key = ""
        closest_word = ""

        for word in word_tokenize(message):
            count += 1
            if len(word) < 3 or word == 'beli':
                continue

            for key in qa_dict.keys():
                #print "key: " + key
                #print "word: " + word
                current_distance = distance.levenshtein(key, word)
                #print "distance: " + str(current_distance)
                if current_distance < smallest_distance:
                    closest_key = key
                    closest_word = word
                    smallest_distance = current_distance
            if count > 10:
                #print 1
                #log_wrapper("no words in first 11 match - going for the best one")
                break
            if smallest_distance < 2:
                #print 2
                #log_wrapper("found the best one after " + str(count) + " tries." )
                break

        log_wrapper("Nearest words are key '" + closest_key + \
              "' and word '" + closest_word + \
              "' with score " + str(smallest_distance) + ".")

        return qa_dict[closest_key]
    except:
        log_wrapper(traceback.print_exc())
        return "#samojakobot"


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log_wrapper(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                if messaging_event.get("message"):  # someone sent us a message
                    try:
                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = "jako" if "text" not in messaging_event["message"] else messaging_event["message"]["text"] # the message's text

                        bot_reply =  answer(message_text)

                        #log_wrapper(bot_reply)

                        send_message(sender_id, bot_reply.decode('utf8'))
                    except:
                        log_wrapper("Could not answer due to error")
                        log_wrapper(traceback.print_exc())

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                    pass

    return "ok", 200


def send_message(recipient_id, message_text):

    log_wrapper("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log_wrapper(r.status_code)
        log_wrapper(r.text)


def log_wrapper(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()


if __name__ == '__main__':
    print "Going into main"
    app.run(debug=False)

