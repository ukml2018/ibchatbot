from flask import Flask, request, render_template, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
#@app.route('/chat', methods=['GET'])
@app.route("/get")
def chat():
    userText = request.args.get('msg')  
    #return str(bot.get_response(userText)) 
    #return response
    #message = request.form['message']
    print("Before calling the ")
    # Construct the URL with the user's query
    url = f"https://datalookupflow.azurewebsites.net/{userText}"
    
    # Make an HTTPS call to the constructed URL
    #response = requests.get(url)
    # Make an HTTPS call to the desired URL
    #response = requests.post('https://datalookupflow.azurewebsites.net', data={'message': userText})
    try:
        # Make an HTTPS call to the constructed URL
        print("Inside try block")
        response = requests.get(url)
        print(response)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        #return json.dump(response)
        return response.text
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print("Inside except block")
        error_message = f"An error occurred: {str(e)}"
        return json.dump(error_message)
    #return response

if __name__ == '__main__':
    app.run(debug=True,port=8000)