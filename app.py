import random
from bs4 import BeautifulSoup
from flask import Flask, request, redirect, render_template, url_for
from functions import get_extra_journal_info_scraper,get_all_journal_info_from_csv, get_journal_previews, get_words

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore():
    all_title_words = get_words()
    return render_template('explore.html', all_title_words=all_title_words)

@app.route('/explore/<letter>')
def explore_letter(letter):
    all_title_words = get_words()
    words_starting_with_letter = list(set(word for word in all_title_words if word.startswith(letter)))
    journals_that_have_words_starting_with_letter = []
    for word in words_starting_with_letter:
        journals_that_have_words_starting_with_letter += [title for title in get_words() if word in title]
    return render_template('explore_letter.html', letter=letter, words_starting_with_letter=words_starting_with_letter, journals_that_have_words_starting_with_letter=journals_that_have_words_starting_with_letter)

@app.route('/explore/titles/<word>')
def explore_titles(word):
    data = get_journal_previews()
    data_with_word = [entry for entry in data if word in entry[0]]
    return render_template('explore_titles.html', word=word, data_with_word=data_with_word)


#TEST DESIGN CURRENTLY ACTIVE
@app.route('/explore/titles_version_2/<word>')
def explore_titles_version_2(word):
    colors = ["bg-red-500", "bg-yellow-500", "bg-green-500", "bg-blue-500"]
    data = get_journal_previews()
    data_with_word = [(entry[0], entry[1], entry[2], random.choice(colors)) for entry in data if word in entry[0]]
    return render_template('explore_titles_version_2.html', word=word, data_with_word=data_with_word)



@app.route('/explore/journals/<title>')
def explore_journal(title):
    all_info = get_all_journal_info_from_csv(title)
    print(all_info)
    return render_template('explore_journal.html', all_info=all_info)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    return redirect(url_for('search_results', query=query))

@app.route('/search/<query>', methods=['GET'])
def search_results(query):
    data = get_journal_previews()
    query_words = query.lower().split()
    results = [entry for entry in data if all(word in entry[0].lower() for word in query_words)]
    return render_template('search_results.html', query=query, results=results)

@app.route('/creditos')
def credits():
    return render_template('credits.html')

if __name__ == '__main__':
    app.run(debug=True)