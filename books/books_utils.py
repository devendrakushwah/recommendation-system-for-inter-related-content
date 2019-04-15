#!/usr/bin/env python
# coding: utf-8
import pandas as pd
from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os
from surprise import Reader, Dataset, SVD, evaluate
from books.models import *
from easyRec import utils
from movies.models import Movie
from tvshows.models import Show

data_path=os.path.abspath('datasets/book_data.csv')
rating_path=os.path.abspath('datasets/book_ratings.csv')


def get_book_details(title):
    try:
        qSet=Book.objects.filter(book_title=title)
        qSet=qSet[0]
        qSet=Book.objects.get(book_title=title)
        ans={}
        ans['book_title']=qSet.book_title
        ans['book_id']=qSet.book_id
        ans['book_plot']=qSet.book_plot[:150]
        ans['book_genre']=qSet.book_genre
        ans['book_link']=qSet.book_link
        ans['book_rating']=qSet.book_rating
        return ans
    except:
        pass

def popular_books():
    try:
        data = pd.read_csv(data_path)
        data = data.sort_values('book_rating', ascending=False)
        ans = []
        final=[]
        i = 0
        for index, row in data.iterrows():
            i += 1
            if (i >= 7):
                break
            ans.append(row['book_title'])
        for i in ans:
            final.append(get_book_details(i))
        return final
    except:
        pass


def top_charts(genre):
    try:
        data = pd.read_csv(data_path)
        data = data.sort_values('book_rating', ascending=False)
        ans = []
        final=[]
        for index, row in data.iterrows():
            if (genre in row['book_genre']):
                ans.append(row['book_title'])
        for i in ans[:6]:
            final.append(get_book_details(i))
        return final
    except:
        pass


def clean_genre(s):
    return s.replace(' ', '').split(',')
def clean_author(s):
    return s.replace(' ', '').lower().split(',')

def similar_books(title):
    try:
        data = pd.read_csv(data_path)
        data = data.drop('book_rating', 1)
        data = data.drop('book_link', 1)
        data = data.drop('book_id', 1)

        data['book_genre'] = data['book_genre'].map(lambda x: clean_genre(x))
        data['book_author'] = data['book_author'].map(lambda x: clean_author(x))
        data['key_words'] = ""

        for index, row in data.iterrows():
            plot = row['book_plot']
            r = Rake()
            r.extract_keywords_from_text(plot)
            key_words_dict_scores = r.get_word_degrees()
            data.at[index, 'key_words'] = list(key_words_dict_scores.keys())

        # dropping the Plot column
        data.drop(columns=['book_plot'], inplace=True)
        data.set_index('book_title', inplace=True)
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
        idx = indices[indices == title].index[0]
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_10_indexes = list(score_series.iloc[1:6].index)
        ans=[]
        for i in top_10_indexes:
            ans.append(data.iloc[i].name)
        final=[]
        for i in ans:
            final.append(get_book_details(i))
        return final
    except:
        pass

def personalized_books(username):
    try:
        ratings = pd.read_csv(rating_path)
        reader = Reader()
        data = Dataset.load_from_df(ratings[['username', 'book_id', 'rating']], reader)
        data.split(n_folds=10)
        svd = SVD()
        evaluate(svd, data, measures=['RMSE'])
        temp=[]
        obj=Book.objects.all()
        for i in obj:
            temp.append([i.book_id,i.book_title,svd.predict(username,i.book_id).est])
        temp.sort(key= lambda x:x[2],reverse=True)
        ans=[]
        rated=Book_Rating.objects.filter(username=username)
        already_rated=[]
        for i in rated:
            already_rated.append(i.book_id)
        j=0
        for i in temp:
            if(j>11):
                break
            if(i[0] not in already_rated):
                ans.append(i[1])
                j+=1
        final=[]
        for i in ans:
            final.append(get_book_details(i))
        return final
    except:
        pass

def rate_book(username,book_id,rating):
    try:
        qSet=Book_Rating.objects.filter(username=username,book_id=book_id)
        if(len(qSet)==0):
            old = open(rating_path,'a')
            old.write(str(username) + "," + str(book_id) + "," + str(rating) + "\n")
            old.close()
            obj = Book_Rating(username=str(username), book_id=str(book_id), rating=str(rating))
            obj.save()
        else:
            #to update rating csv file
            qSet[0].rating=rating
            qSet[0].save()
            with open(rating_path, 'r') as f:
                data = f.readlines()
                f.close()
            for i in range(len(data)):
                if ((username + ',' + book_id) in data[i]):
                    data[i] = username + ',' + book_id + ',' + rating+'\n'
            with open(rating_path, 'w') as file:
                file.writelines(data)
                file.close()
    except:
        pass

def get_similar_content(book_id):
    items=utils.similar_items(book_id)
    movie_ids=[]
    tvshow_ids=[]
    for i in items:
        if i[0]=='t':
            if(len(tvshow_ids)!=5):
                tvshow_ids.append(i)
        elif i[0]=='m':
            if(len(movie_ids)!=5):
                movie_ids.append(i)
        if(len(movie_ids)==5 and len(tvshow_ids)==5):
            break

    similar_movies=[]
    similar_tvshows=[]

    for i in movie_ids:
        qSet = Movie.objects.filter(movie_id=i)[0]
        ans = {}
        ans['movie_title'] = qSet.movie_title
        ans['movie_id'] = qSet.movie_id
        ans['movie_plot'] = qSet.movie_plot
        ans['movie_genre'] = qSet.movie_genre
        ans['movie_link'] = qSet.movie_link
        ans['imdb_rating'] = qSet.imdb_rating
        similar_movies.append(ans)

    for i in tvshow_ids:
        qSet = Show.objects.filter(show_id=i)[0]
        ans = {}
        ans['show_title'] = qSet.show_title
        ans['show_id'] = qSet.show_id
        ans['show_plot'] = qSet.show_plot
        ans['show_genre'] = qSet.show_genre
        ans['show_link'] = qSet.show_link
        ans['show_rating'] = qSet.show_rating
        similar_tvshows.append(ans)

    return similar_movies,similar_tvshows