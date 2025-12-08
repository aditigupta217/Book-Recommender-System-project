from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular-3.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
Books = pickle.load(open('Books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_name=list(popular_df['Book-Title'].values),
        book_author=list(popular_df['Book-Author'].values),
        image=list(popular_df['Image-URL-M'].values),
        votes=list(popular_df['num_ratings'].values),
        rating=list(popular_df['avg_rating'].values)
    )

@app.route('/Recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/Recommend_Books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')


    if user_input not in pt.index:
        return render_template('recommend.html', data=[], message="Book not found!")

    index = np.where(pt.index == user_input)[0][0]

    data = []
    similar_items = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    for i in similar_items:
        item = []
        temp_df = Books[Books['Book-Title'] == pt.index[i[0]]]

        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
        item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

        data.append(item)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
