from flask import Flask,request,jsonify,render_template
import requests
# import gunicorn

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')


@app.route('/api/',methods = ['POST'])
def api():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    # print(data)
    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)
    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    return jsonify(response)

def fetch_conversion_factor(source,target):

    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey=9aa0c54f5ad4c460c36d".format(source,target)

    response = requests.get(url)# get data 
    response = response.json()# json form

    return response['{}_{}'.format(source,target)]


if __name__ == '__main__':
    app.run(debug=True)
    #web: sh setup.sh && streamlit run demo.py

