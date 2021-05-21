# Import Dependencies
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
import pandas as pd
from flask_cors import CORS


rds_connection_string = (f'dfprimldpzkawt:daee61afbe9e4cd6d00f43d9dbbbeb3aee8b373b1d8b7c67ff29e014246fb644@ec2-3-217-219-146.compute-1.amazonaws.com:5432/d8r4gedbk2rdiv')
engine = create_engine(f'postgresql://{rds_connection_string}')
conn = engine.connect()

data = pd.read_sql_query('SELECT * FROM imdb_movies_global', conn)
data_yr = pd.read_sql_query('SELECT DISTINCT year_mv FROM imdb_movies_global ORDER BY year_mv', conn)
movies_data = data.set_index('imdb_title_id').T.to_dict('dict')

#STARTING FLAST SERVER
app = Flask(__name__)
CORS(app)

#DEFINING HOME PAGE
@app.route('/')
def home():
    return "Home Page"

#RETURNING ALL MOVIE_DATA IN JASON FORMAT
@app.route('/all_movies')
def all_movies():
    return jsonify(movies_data)

#RETURNING SPECIFIC MOVIE RECORD BASED ON TITLE
@app.route('/movie/<title>')
def id(title):
    titleDF = data.loc[data['title'] == title.capitalize()]
    titleDic = titleDF.set_index('imdb_title_id').T.to_dict('dict')
    try:
        return jsonify(titleDic)
    except:
        return "Movie not available"

#RETURNING ALL MOVIE RECORDS
@app.route('/all_titles')
def all_titles():
    titleDic = data['title'].to_dict()
    try:
        return jsonify(titleDic)
    except:
        return "Movie not available"

#RETURNING ONLY A SPECIFIC YEAR
@app.route('/year/<year>')
def year(year):
    yearDF = data.loc[data['year_mv'] == str(year)]
    yearDic = yearDF.set_index('imdb_title_id').T.to_dict('dict')
    try:
        return jsonify(yearDic)
    except:
        return "Year not found"

@app.route('/all_years')
def all_titles():
    title_yr = data_yr['year_mv'].to_dict()
    try:
        return jsonify(title_yr)
    except:
        return "Year not found"

#RETURNING RECORDS PER GENRE AND LANGUAGE
@app.route('/filter/<genre>/<language>')
def filter(genre=None, language=None):
    filterDF = data.loc[(data['genre_1'] == genre.capitalize()) & (data['lang_1'] == language.capitalize())]
    filterDic = filterDF.set_index('imdb_title_id').T.to_dict('dict')
    try:
        return jsonify(filterDic)
    except:
        return "Record not found"

if __name__ == '__main__':
    app.run(debug=True)
