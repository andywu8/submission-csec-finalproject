"""main file to run flask app"""

from flask import Flask, render_template, request, make_response, redirect, url_for, session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import requests
import retrieve_token

from amadeus import Client, ResponseError

import os 

import urllib.request, json
import jsonify 
import spacy
# https://towardsdatascience.com/keyword-extraction-process-in-python-with-natural-language-processing-nlp-d769a9069d5c
# from pricing_algorithm import find_best_time_to_buy
import pricing_algorithm
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def home():
    """home page"""
    error_messages = []
    users = None
    confirmation_message = None
    if request.method == 'POST':
        budget = request.form['budget']
        domestic = request.form['domestic']
        source = request.form['source']
        destination = request.form['destination']
        preferred_airline = request.form['preferred_airline']
        about_trip = request.form['about_trip']
        departure_date = request.form["departure-date"]
        return_date = request.form["return-date"]

        print("budget", budget)
        print("domestic", domestic)
        
        print("source:", source)
        print("destination", destination)
        print("preferred_airline", preferred_airline)
        print("about trip", about_trip)
        print("departure_date", departure_date)
        print("return_date", return_date)
        # return render_template('index.html')
        # key_words = process_key_words(about_trip)
        # print("key words is", key_words)
        # pricing_algorithm.find_best_time_to_buy(source, domestic, destination, departure_date,return_date)
        flight_data = find_flight_data(source, destination, preferred_airline, departure_date, return_date)
        print(flight_data)
        open_ai_data = find_open_ai_data(source, destination, about_trip)
        planned_trip = plan_trip(open_ai_data, flight_data)
        return render_template('index.html',
                                  planned_trip = planned_trip, )
    else:
        return render_template('index.html')






    # insert_dummy_users()
def plan_trip(open_ai_data, flight_data):
    trip_plan = "Here is the Trip Planning Data: \n"
    trip_plan += "Here are possible options of things you can do: {} \n".format(open_ai_data)
    trip_plan += "Here are the prices for these options and you can book now"

    trip_plan += "Here is what the expected prices look like in the next week"
    # for word in key_words:
    #     trip_plan += word

    return (trip_plan)

def process_key_words(about_trip):
    nlp = spacy.load("en_core_web_md")
    doc = nlp(about_trip)
    print("Keywords", doc.ents)
    return (doc.ents)


def find_flight_data(origin, destination, preferred_airline, departure_date, return_date):
    token = retrieve_token.retrieve_token()

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    adults = 1
    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "originLocationCode": 'LAX',
        "destinationLocationCode": 'SFO',
        "departureDate": departure_date,
        "returnDate": return_date,
        "adults": adults
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        flight_offers = response.json()["data"]
        print(flight_offers)
    else:
        print("Error:", response.status_code, response.text)


def find_open_ai_data(source, destination, about_trip):
    prompt = "What are fun things to do in {} given: {}?".format(destination, about_trip)
    endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = os.environ.get('chat_gpt_api_key')
    params = {
        "model": "gpt-3.5-turbo",
        "max_tokens": 400,
        "temperature": 0.7,
        "n": 1,
        "messages": [{"role": "user", "content": prompt}]
    }
    # make the API request
    headers = {"Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",}
    response = requests.post(endpoint, json=params, headers=headers)
    
    # parse the response
    json_data = response.json()
    
    with open("output.json", "w") as outfile:
        # use the 'json.dump()' function to write the data to the file
        json.dump(json_data, outfile)

    generated_text = json_data["choices"][0]
    generated_text = generated_text['message']['content']

    
    print("open ai data", generated_text)
    return generated_text




if __name__ == '__main__':
    """runs the application on a server"""
    app.run(debug=True, host='0.0.0.0', port=8000)