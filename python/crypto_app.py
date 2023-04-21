from flask import Flask, render_template, request
import requests
app = Flask(__name__,  template_folder='../html_files/templates')

# Route to display the form
@app.route('/')
def index():
    # Get the list of top 250 cryptocurrencies from CoinGecko API
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=false')
    data = response.json()

    # Extract the names of the top 250 cryptocurrencies
    cryptos = [crypto['name'] for crypto in data]

    # Render the form template with the list of cryptocurrencies
    return render_template('index.html', cryptos=cryptos)

# Route to process the form data and display the results
@app.route('/result', methods=['POST'])
def result():
    # Get the selected cryptocurrencies from the form
    crypto_a = request.form['crypto_a']
    crypto_b = request.form['crypto_b']

    # Get the current price and market cap of the selected cryptocurrencies from CoinGecko API
    response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_a},{crypto_b}&vs_currencies=usd&include_market_cap=true')
    data = response.json()

    # Extract the price and market cap of the selected cryptocurrencies
    price_a = data[crypto_a]['usd']
    price_b = data[crypto_b]['usd']
    market_cap_b = data[crypto_b]['usd_market_cap']

    # Render the result template with the price and market cap data
    return render_template('result.html', crypto_a=crypto_a, crypto_b=crypto_b, price_a=price_a, price_b=price_b, market_cap_b=market_cap_b)