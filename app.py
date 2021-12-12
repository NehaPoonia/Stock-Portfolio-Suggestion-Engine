import time
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, request
import json
import matplotlib.pyplot as plt
import seaborn
import yfinance as yf
app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


def one_investment_strategy(data, amount, strategy):
    all_stock_portfolio = []
    current_value_of_investment = 0
    amount_to_invest = int(amount)
    necessary_info = []
    for stock_item in data[strategy]:
        info = []
        stock_portfolio = []
        money_invested = (int(stock_item['percentage'])/100)*amount_to_invest
        print("Money invested in", stock_item['name'], "is", money_invested)
        stock = yf.Ticker(stock_item['symbol'])
        current_price = stock.info['currentPrice']
        print("Current value of", stock_item['name'], "is", current_price)
        info.append(stock_item['name'])
        info.append(money_invested)
        info.append(current_price)
        necessary_info.append(info)
        stock = yf.Ticker(stock_item['symbol'])
        hist = stock.history(period="5d")
        number_of_shares = money_invested/current_price
        for price in hist['Close']:
            stock_portfolio.append(price*number_of_shares)
        all_stock_portfolio.append(stock_portfolio)
        current_value_of_investment += (current_price*number_of_shares)

    print(all_stock_portfolio)
    total_portfolio = []
    for index in range(len(all_stock_portfolio[0])):
        s = 0
        s = s + all_stock_portfolio[0][index] + all_stock_portfolio[1][index] + \
            all_stock_portfolio[2][index] + all_stock_portfolio[3][index]
        total_portfolio.append(s)
    print(total_portfolio)
    current_time = datetime.now()
    current_day = current_time.strftime('%m-%d-%Y')
    d = str(current_day)
    d1 = datetime.strptime(d, '%m-%d-%Y')
    dates = [(d1-timedelta(days=i)).strftime('%m-%d-%Y')
             for i in range(5, 0, -1)]
    print(dates)
    print(total_portfolio)
    print(current_value_of_investment)
    return necessary_info
    # plt.savefig('templates/investment-strategy.png')
    # plt.plot(dates, total_portfolio)
    # plt.xlabel("Last 5 days")
    # plt.ylabel("Amount in USD")
    # plt.title("Overall Portfolio Trend")
    # time.sleep(60)
    # plt.savefig('templates\investment-strategy.jpeg')
    # return render_template('one_strategy.html', name=amount, strategy=strategy)


@app.route('/result', methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    strategy = output["strategy"]
    with open('investing_strategies.json') as f:
        data = json.load(f)
    print(data)
    if len(strategy.split()) == 2:
        info = one_investment_strategy(data, name, strategy)
        stock1 = info[0][0]
        stock2 = info[1][0]
        stock3 = info[2][0]
        stock4 = info[3][0]
        stock1_price = info[0][2]
        stock2_price = info[1][2]
        stock3_price = info[2][2]
        stock4_price = info[3][2]
        stock1_money = info[0][1]
        stock2_money= info[1][1]
        stock3_money = info[2][1]
        stock4_money = info[3][1]
    else:
        print("No")
    return render_template('one_strategy.html', name=name, strategy=strategy, stock1 = stock1, stock2 = stock2, stock3 = stock3, stock4 = stock4, stock1_price = stock1_price, stock2_price = stock2_price, stock3_price = stock3_price, stock4_price = stock4_price, stock1_money = stock1_money, stock2_money = stock2_money, stock3_money = stock3_money, stock4_money = stock4_money)


if __name__ == "__main__":
    app.run(debug=True)
