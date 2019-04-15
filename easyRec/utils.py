import pandas as pd
from movies import movies_utils
from books import books_utils
from tvshows  import shows_utils
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def similar_items(item_id):
    book = pd.read_csv(books_utils.data_path)
    movie = pd.read_csv(movies_utils.data_path)
    tvshow = pd.read_csv(shows_utils.data_path)

    # data cleaning
    book['item_data'] = book['book_title'] + ' ' + book['book_author'] + ' ' + book['book_plot']
    book['item_id'] = book['book_id']
    book = book.drop(['book_id', 'book_title', 'book_genre', 'book_author', 'book_plot', 'book_rating', 'book_link'],
                     axis=1)
    movie['item_data'] = movie['movie_title'] + ' ' + movie['movie_plot']
    movie['item_id'] = movie['movie_id']
    movie = movie.drop(
        ['movie_id', 'movie_title', 'movie_genre', 'actors', 'movie_plot', 'imdb_rating', 'movie_link', 'director'],
        axis=1)
    tvshow['item_data'] = tvshow['show_name'] + ' ' + tvshow['show_plot']
    tvshow['item_id'] = tvshow['show_id']
    tvshow = tvshow.drop(['show_id', 'show_name', 'show_genre', 'show_plot', 'show_rating', 'show_link'], axis=1)

    data = (book.append(movie)).append(tvshow)

    data['key_words'] = ""

    for index, row in data.iterrows():
        item_data = row['item_data']
        r = Rake()
        r.extract_keywords_from_text(item_data)
        key_words_dict_scores = r.get_word_degrees()
        row['key_words'] = list(key_words_dict_scores.keys())
    data.drop(columns=['item_data'], inplace=True)

    data.set_index('item_id', inplace=True)

    data['bag_of_words'] = ''
    columns = data.columns
    for index, row in data.iterrows():
        words = ''
        for col in columns:
            words = words + ' '.join(row[col]) + ' '
        data.at[index, 'bag_of_words'] = words

    data.drop(columns=[col for col in data.columns if col != 'bag_of_words'], inplace=True)

    count = TfidfVectorizer()
    count_matrix = count.fit_transform(data['bag_of_words'])
    indices = pd.Series(data.index)
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    idx = indices[indices == item_id].index[0]

    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)

    top_30_indexes = list(score_series.iloc[1:51].index)

    ans=[]
    for i in top_30_indexes:
        ans.append(data.iloc[i].name)
    return ans