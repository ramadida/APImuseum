from flask import Flask
from flask import jsonify
import requests
import json
from bs4 import BeautifulSoup
app = Flask(__name__)

# Collect and parse first page
page = requests.get('https://www.museummacan.org/collections')
soup = BeautifulSoup(page.text, 'html.parser')
result = []


# Pull all text from the BodyText div
artist_name_list = soup.find_all(class_='collection__each hover__opacity')

# make a json file from scraping data
for artist_name in artist_name_list:
    artist = artist_name.find(class_='collection__artistname body').text
    works = artist_name.find(class_='collection__artname body').text
    single = {'artist': artist, 'works': works}
    result.append(single)
    with open('works.json', 'w') as f:
        json.dump(result, f, indent=4)

with open('works.json') as g:
    data = json.load(g)


@app.route('/')
def home():
    return '''<h1>Katalog Seni</h1>
<p>Prototype API for showing works of art from a museum re: Museum Macan</p>'''

# METHODS GET TO TAKE ALL THE works


@app.route('/karyaseni', methods=['GET'])
def show_karyaseni():
    return jsonify(data)

# METHODS GET TO TAKE ALL THE artist


@app.route('/seniman', methods=['GET'])
def show_seniman():
    return jsonify((data['artist']))


app.run()
