from flask import Flask, request, render_template, jsonify
from flask_jsonpify import jsonpify
import requests
import json
import os
import pandas as pd
import numpy as np

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
        #converted_data = response.text.replace('\n', '<br/>')
        #print(converted_data)
        #return converted_data
        #return response.text
        string = response.text
        print("The string value",string)
        if string.startswith('"[{'):
           print("Inside Json")
           #json_data = jsonify(string)
           json_data = json.loads(string)
           print("Json data:", json_data)
           # Parse JSON data
           data = json.loads(json_data)
           print("Printing data:",data)
           # Assuming output_array is your NumPy array
           output_array = np.array(data)
           # Convert NumPy array to DataFrame
           #df = pd.DataFrame(output_array)
           
           # Convert to DataFrame
           df = pd.DataFrame(data)
           #df_list = df.values.tolist()
           #df_list = list(df.columns) + list(df.values.flatten())
           #df_list = list(df.columns) + list(df.values.tolist())
           df_list = list(df.values.tolist())
           print("df list:",df_list)
           # Create a string with each element on a separate line
           df_list1 = list(df.columns.tolist())
           df_list1.append(df_list)
           print("df_list1:",df_list1)
           #l=[df_list1,df_list]
           output_string = '\n'.join(str(element) for element in df_list1)
           #output_string1 = df_list1 +'\n'+ output_string
           JSONP_data = jsonpify(df_list)
           df1= df.to_json()
           print ("Printing array dataframe:",df)
           print ("Printing json dump:",df1)
           print("Print JSONP_data:",JSONP_data)
           print("Print output_string:", output_string)
           # Convert DataFrame to dictionary
           output_dict = df.to_dict(orient='records')
           print("output_dict value:",output_dict)
           #array = df.values
           #data_list = df.values.tolist()
           #data_list = df.values.to_dict()
           #print (data_list)
           #return data_list
           #data frame to string
           #df1 = df.to_dict(orient='records')
           #print("Print df1:",df1)
           return output_string
        else: 
           print("Inside string")
           return response.text
        '''
        try:
          print("Inside try response")
          return response
        except:
          print("Inside except response")
          return response.text
        '''
    except requests.exceptions.RequestException as e:
        # Handle the exception here
        print("Inside except block")
        error_message = f"An error occurred: {str(e)}"
        return json.dump(error_message)
    #return response

if __name__ == '__main__':
    app.run(debug=True,port=8000)
