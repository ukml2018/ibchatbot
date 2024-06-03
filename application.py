from flask import Flask, request, render_template, jsonify
import requests
import json
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
#@app.route('/chat', methods=['GET'])
@app.route("/get")
def chat():
    userText = request.args.get('msg')  
    #message = request.form['message']
    print("Before calling the ")
    
    #client = requests.Session()
    #get the current process id
    session_id = os.getpid()

    #print the sesion id of current process
    #session_id = os.getsid(pid)
    print (session_id)
    #print(client)
    flag="C"
    # Construct the URL with the user's query
    url = f"https://datalookupflow.azurewebsites.net/{session_id}/{flag}/{userText}"
    
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
        #If response Json data
        #If  image .jpg
        return response.text
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print("Inside except block")
        error_message = f"An error occurred: {str(e)}"
        return json.dump(error_message)
    #return response

if __name__ == '__main__':
    app.run(debug=True,port=8000)
