# import requests
# import json
# url = 'https://script.google.com/macros/s/AKfycbwuIo6i2wfcTW_yavo25LTEegNH3trsu2BxNEgMipHfcI4mu5QuHJUoGlfNHK-tihguHA/exec'
# data = {'name': 'suryash', 'age': 21, 'city': 'subodh'}
# # post request to the server
# post_data= json.dumps(data)
# res= requests.post(url, data=post_data)
# print(res.text)



# import pandas as pd
# from sklearn.tree import DecisionTreeRegressor
from flask import Flask, jsonify, request
import requests
# from flask_cors import CORS, cross_origin
import time
# import pandas
import json
import csv

# from multiprocessing import Value

# counter = Value('i', 0)
app = Flask(__name__)
# cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/ret', methods=['GET'])
def ReturnJSON():
  # count=0
  start = time.time()
  f = open("count.txt", "r")
  count = int(f.read())
  f.close()

  count += 1

  f = open("count.txt", "w")
  f.write(str(count))
  f.close()
  # with counter.get_lock():
  #   counter.value += 1
  #   out = counter.value
  id = request.args.get('id')
  cookies = {
    'csrftoken':
    '008zLFeqD6hn1uVwMWU5R7D08wpQpL1kS6pjdR8CI9FIkyafLRCDMkibTYT0DVeN',
    'gr_user_id': '6340500b-656f-48ab-849f-f91ebe8e4ffc',
    '87b5a3c3f1a55520_gr_session_id': '8212ca8a-d573-4829-8fe0-268a3fd8ccf9',
    '87b5a3c3f1a55520_gr_session_id_8212ca8a-d573-4829-8fe0-268a3fd8ccf9':
    'true',
    '_gid': 'GA1.2.1034509744.1670739497',
    '_gat': '1',
    '_ga_CDRWKZTDEX': 'GS1.1.1670739498.1.0.1670739498.0.0.0',
    '_ga': 'GA1.1.938791714.1670739497',
  }

  headers = {
    'authority':
    'leetcode.com',
    'accept':
    '*/*',
    'accept-language':
    'en-US,en;q=0.9',
    'authorization':
    '',
    'content-type':
    'application/json',
    # 'cookie': 'csrftoken=008zLFeqD6hn1uVwMWU5R7D08wpQpL1kS6pjdR8CI9FIkyafLRCDMkibTYT0DVeN; gr_user_id=6340500b-656f-48ab-849f-f91ebe8e4ffc; 87b5a3c3f1a55520_gr_session_id=8212ca8a-d573-4829-8fe0-268a3fd8ccf9; 87b5a3c3f1a55520_gr_session_id_8212ca8a-d573-4829-8fe0-268a3fd8ccf9=true; _gid=GA1.2.1034509744.1670739497; _gat=1; _ga_CDRWKZTDEX=GS1.1.1670739498.1.0.1670739498.0.0.0; _ga=GA1.1.938791714.1670739497',
    'origin':
    'https://leetcode.com',
    'referer':
    'https://leetcode.com/godofcode99/',
    'sec-ch-ua':
    '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile':
    '?1',
    'sec-ch-ua-platform':
    '"Android"',
    'sec-fetch-dest':
    'empty',
    'sec-fetch-mode':
    'cors',
    'sec-fetch-site':
    'same-origin',
    'user-agent':
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36',
    'x-csrftoken':
    '008zLFeqD6hn1uVwMWU5R7D08wpQpL1kS6pjdR8CI9FIkyafLRCDMkibTYT0DVeN',
  }

  json_data = {
    'query':
    '\n    query recentAcSubmissions($username: String!, $limit: Int!) {\n  recentAcSubmissionList(username: $username, limit: $limit) {\n    id\n    title\n    titleSlug\n    timestamp\n  }\n}\n    ',
    'variables': {
      'username': id,
      'limit': 15,
    },
  }

  response = requests.post('https://leetcode.com/graphql/',
                           cookies=cookies,
                           headers=headers,
                           json=json_data).json()

  data = {
    "name": id,
    "subject": response,
    "count": count,
    "callTime": round(time.time()),
    "respTime": time.time() - start,
  }
  finalResp = jsonify(data)
  # finalResp.headers.add("Access-Control-Allow-Origin", "*")
  # finalResp.headers['Access-Control-Allow-Origin'] = '*'

  # print(request.args.get('id'))
  return finalResp


@app.route('/tasks', methods=['GET'])
def GetTasks():
  df = pandas.read_csv(r'tasks.csv')

  # for data as list of objects
  # data = df.to_dict(orient='records')

  #  for data as object of objects
  data = df.to_dict(orient='index')
  # dict={}
  # dict["status"]= "success"
  # use jsonify instead of json.dumps()
  json_data = jsonify(data)
  return json_data


@app.route('/tasks', methods=['POST'])
def PostTasks():
  #  to convert data to parseable dictionary
  data = request.get_json()
  # print(data['task'])
  # request_json = json.loads(data)

  # Open the CSV file for appending
  with open('tasks.csv', 'a', newline='') as csvfile:
    #   # Create a CSV writer
    csvwriter = csv.writer(csvfile)
    #   # Write the JSON object to the CSV file as a new row
    csvwriter.writerow(data.values())
  # print(data)
  response = jsonify(success=True)
  return response


@app.route('/pushToHisaabDb', methods=['POST'])
def pushToDb():
  import requests
  import json
  url = 'https://script.google.com/macros/s/AKfycbwuIo6i2wfcTW_yavo25LTEegNH3trsu2BxNEgMipHfcI4mu5QuHJUoGlfNHK-tihguHA/exec'
  dataVal = request.get_data()
  res = requests.post(url, data=dataVal)
  return dataVal 


def modelCheck(n):

  # Define model. Specify a number for random_state to ensure same results each run

  melbourne_file_path = 'melb_data.csv'
  melbourne_data = pd.read_csv(melbourne_file_path)
  # print(melbourne_data.columns)

  melbourne_data = melbourne_data.dropna(axis=0)
  y = melbourne_data.Price
  melbourne_features = [
    'Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude'
  ]
  ActualPrice = ['Price']
  # t= melbourne_data[ActualPrice]

  X = melbourne_data[melbourne_features]
  # X.describe()
  melbourne_model = DecisionTreeRegressor(random_state=1)

  # Fit model
  melbourne_model.fit(X, y)
  temp = melbourne_model.predict(X.head(n=n)).tolist()
  return temp
  # print(temp[2])
  # print(melbourne_model.predict(X.head()))


@app.route('/result', methods=['GET'])
def ModelReturnJSON():
  # count=0
  start = time.time()
  countVal = request.args.get('n')

  valData = modelCheck(int(countVal))
  xy = list(valData)
  print(type(xy))
  data = {'s': 'success', 'predictionList': xy}
  finalResp = jsonify(data)
  return finalResp


if __name__ == '__main__':
  app.run(debug=True)
