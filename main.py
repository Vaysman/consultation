from flask import Flask, render_template, request, redirect, url_for
import csv
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def langsearch():
    langs = []
    fields = ['id', 'language', 'derivation', 'class', 'extra_info', 'example']
    with open("database.csv", 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fields, delimiter=';')
        for row in reader:
            if not row['language'] in langs:
                langs.append(row['language'])
    return render_template('langsearch.html', langs=langs)

@app.route('/langresult', methods=('GET', 'POST'))
def langresult():
    urls = \
      {'return to Search page': url_for('langsearch')}
    dict_csv = {}
    if request.args:
        language = request.args['language']
        fields = ['id', 'language', 'derivation', 'class', 'extra_info', 'example']
        with open("database.csv", 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, fieldnames=fields, delimiter=';')
            for row in reader:
                if language in row['language']:
                    dict_csv[row['id']] = json.loads(json.dumps(row))
            print(dict_csv)
            return render_template('langresult.html', 
                            dict_csv=dict_csv,
                            str_csv=dict_csv.values(),
                            urls=urls)
    return redirect(url_for('/'))

if __name__ == '__main__':
  app.run(host='0.0.0')