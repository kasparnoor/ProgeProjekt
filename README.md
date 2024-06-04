# Üldine

Meie projekti eesmärk on teha videote genereerimine AI toel ligipääsetavamaks. Selleks seome AI mudeli meie endi kirjutatud API ja frontendi, kust inimesed saavad videoid genereerida

## Kuidas installida?
**Koodi jooksutamiseks on vaja ngraafika kaarti soovitatavalt selline millel on 16gb vrammi.** 
Minge soovitud kausta ja tehke terminalis käsk `git clone https://github.com/kasparnoor/ProgeProjekt.git`
Edasi võite soovikorral teha sinna ka virtualenvi käsuga `virtualenv venv`
Järgnevalt pange terminali `pip3 install -r requirements.txt`
Enne jooksutamist peab tegema uue kataloogi `checkpoints` ja lisama sinna faili mille saab alla tõmmata siit: 
Selleks et koodi jooksutada pange terminali `python3 gradio_app.py`
# Backend
Backend on koostatud pythoni programmeerimise keeles ning jookseb välise serveri peal. 
# Frontend

Kirjutatud Svelte raamistikuga Javascriptis (HTML ja CSS3 ka ikka)
Inimene kirjutab textareasse sisendi ja vajutab ENTER, peale seda saadab APIle päringu kirjeldusega, mis vastuseks saab video, mis laetakse alla.
