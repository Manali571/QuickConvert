from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/',methods=['POST'])
def index():
    data = request.get_json()
    source_currency = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']

    print(source_currency)
    print(amount)
    print(target_currency)

    cf = fetch_conversion_factor(source_currency,target_currency)
    final_amount = amount * cf
    final_amount = round(final_amount,2)

    response = {
        'fulfillmentText':"{} {} is {} {}".format(amount,source_currency,final_amount,target_currency)
    }
    print(final_amount)
    return jsonify(response)

def fetch_conversion_factor(source,target):
    url = url = f"https://v6.exchangerate-api.com/v6/06aa0b84b3a83b2df39a15ff/pair/{source}/{target}"
    response = requests.get(url).json()

    # Check if the API call was successful
    if response.get('result') == 'success':
        return response['conversion_rate']
    else:
        raise ValueError(f"Error fetching conversion rate: {response.get('error-type')}")

    response = requests.get(url)
    response = response.json()
    print(response)

    return response['{}_{}'.format(source,target)]


print("fConverted Amount: {converted_amount}")

if __name__=="__main__":
    app.run(debug=True)
