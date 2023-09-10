from flask import Flask, render_template, Response, request
import requests

app = Flask(__name__, template_folder='.')

num_per_cat = 10

# Define the API URL
api_url = 'https://opentdb.com/api.php?amount=' + str(num_per_cat)

# api to retrieve session token
api_retrieve = 'https://opentdb.com/api_token.php?command=request'

# api for resetting a token
api_reset = 'https://opentdb.com/api_token.php?command=reset&token='

# api for looking up question count
api_count = 'https://opentdb.com/api_count.php?category='

# token for session
token = 0

# Function to reset the api_url
def reset_url():
    global token, api_retrieve
    resp = requests.get(api_reset)
    data = resp.json()
    if data['response_code'] == 0:
        print("Resetted the session")
    else:
        print("Error while resetting")

def fetch_token():
    resp = requests.get(api_retrieve)
    data = resp.json()
    if data['response_code'] == 0:
        token = data['token']
    else:
        print("Error while fetching token")


# Function to lookup categories from the API
def fetch_cats():
    resp = requests.get('https://opentdb.com/api_category.php')
    data = resp.json()['trivia_categories']
    fin_data = []
    for cat in data:
        id = cat['id']
        if requests.get(api_count+str(id)).json()['category_question_count']['total_question_count'] > num_per_cat:
            fin_data.append(cat)

    return fin_data

# Function to fetch data from the API - difficulty and others not added yet
def fetch_questions(category):
    response = requests.get(api_url + '&category=' + str(category))
    data = response.json()
    if data['response_code'] == 0:
        return data['results']
    elif data['response_code'] == 1:
        print("invalid number of qns - ", num_per_cat)
        exit()
    elif data['response_code'] == 3:
        reset_url()
        fetch_questions(category)
    elif data['response_code'] == 4:
        reset_url()
        fetch_questions(category)
    else:
        print('Error fetching qns')
        exit()

def compute_results(questions, answers):
    # Each correct answer gets 1 mark
    marks = 0
    for i in range(10):
        if answers[i].lower() == questions.correct_answer.lower():
            marks += 1
    return marks

@app.route('/', methods=['GET', 'POST', 'RES'])
def index():
    if request.method == 'POST':
        sel_cat = request.form.get('category')
        print("got category!")
        questions = fetch_questions(sel_cat)
        response = Response(render_template('lol1.html', questions=questions))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

    elif request.method == 'GET':
        categories = fetch_cats()
        questions = []
        response = Response(render_template('lol.html', categories=categories, questions=questions))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response
    
    else:
        answers = []
        for i in range(10):
            print("hi", request.form.get('answer-'+str(i)))
            answers.append(request.form.get('answer-'+str(i)))
    
        marks = compute_results(questions, answers)
        response = Response(render_template('lol.html', marks=marks))
        response.headers['Content-Type'] = 'text/html; charset=utf-8'
        return response

        ## compute results

if __name__ == '__main__':
    fetch_token()
    app.run(debug=True)
