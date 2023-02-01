"""
This script defines functions to be used in a personal finance app web page. 
The application allows you to see returns from various potential investments.
"""
#import libraries, initialize app
from flask import Flask, render_template, request
from return_functions import calculate_return, create_df, calculate_tax_rate, historical_returns
import pandas as pd

#initialize app
app = Flask(__name__,  template_folder='../html_files/templates')

#load in returns dataframe
returns_df = pd.read_excel(r'../data/Output/Returns dataset.xlsx', sheet_name = "r.data")

#function to format dollar sign
@app.template_filter()
def currencyFormat(value):
    value = float(value)
    return "${:,.2f}".format(value)

#Displays the index page accessible at '/'
@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

#Simple interest calculation
@app.route('/simple_interest/', methods = ['GET'])
def simple_interest_home():
    principal = 100
    interest = 10
    years = 10
    result = calculate_return(principal, interest, years)[0]
    df = create_df(principal, interest, years)
    labels = list(df["Year"])
    values = list(df["Value"])
    return(
    render_template('simple_interest.html',
                      Principal1 = principal,
                      Interest1 = interest,
                      Years1 = years,
                      result1 = result,
                      labels = labels,
                      values = values,
                      calculation_success1 = True
                      ))

@app.route('/simple_interest/', methods = ['POST'])
def simple_interest():
    result = None
    #extract inputs from user submission
    principal = float(request.form['Principal1']) 
    interest = float(request.form['Interest1'])
    years = float(request.form['Years1']) 
    try:
        result = calculate_return(principal, interest, years)[0]
        df = create_df(principal, interest, years)
        labels = list(df["Year"])
        values = list(df["Value"])
        return(
        render_template('simple_interest.html',
                          Principal1 = principal,
                          Interest1 = interest,
                          Years1 = years,
                          result1 = result,
                          labels = labels,
                          values = values,
                          calculation_success1 = True
                          ))
    
    #return error messages if exceptions
    except ValueError:
         return (render_template('simple_interest.html',
                         Principal1 = principal,
                         Interest1 = interest,
                         Years1 = years,
                         result1 = result,
                         calculation_success1 = False,
                         error = "Cannot perform operations with provided input"
                         ))
    
#Simple interest calculation, including tax
@app.route('/simple_interest_taxed/', methods = ['GET'])
def simple_interest_taxed_home():
    principal = 100
    interest = 10
    tax = 10
    years = 10
    result = calculate_return(principal, interest, years, inflation = 0, cap_tax_rate = tax)[0]
    return(
    render_template('simple_interest_taxed.html',
                     Principal2 = principal,
                     Interest2 = interest,
                     Years2 = years,
                     Tax2 = tax,
                     result2 = result,
                     calculation_success2 = True))

@app.route('/simple_interest_taxed/', methods = ['POST'])
def simple_interest_taxed():
    result = None
    #extract inputs from user submission
    principal_text = request.form['Principal2']
    interest_text = request.form['Interest2']
    tax_text = request.form['Tax2']
    years_text = request.form['Years2']
    principal = float(principal_text)
    interest = float(interest_text)
    tax = float(tax_text)
    years = float(years_text)
    try:
        result = calculate_return(principal, interest, years, inflation = 0, cap_tax_rate = tax)[0]
    #return value
        return(
        render_template('simple_interest_taxed.html',
                         Principal2 = principal,
                         Interest2 = interest,
                         Years2 = years,
                         Tax2 = tax,
                         result2 = result,
                         calculation_success2 = True
                         ))
    #return error messages if exceptions
    except ValueError:
         return (render_template('simple_interest_taxed.html',
                         Principal2 = principal,
                         Interest2 = interest_text,
                         Years2 = years,
                         result2 = result,
                         calculation_success2 = False,
                         error = "Cannot perform operations with provided input"
                         ))
#Real interest calculation
@app.route('/real_interest/', methods = ['GET'])
def real_interest_home():
    result = None
    #extract inputs from user submission
    principal = 100
    interest = 10
    years = 10
    inflation = 2
    result = calculate_return(principal, interest, years, inflation = inflation)[0]
    return(
    render_template('real_interest.html',
                     Principal3 = principal,
                     Interest3 = interest,
                     Years3 = years,
                     result3 = result,
                     Inflation3 = inflation,
                     calculation_success3 = True
                     ))
@app.route('/real_interest/', methods = ['POST'])
def real_interest():
    result = None
    #extract inputs from user submission
    principal_text = request.form['Principal3']
    interest_text = request.form['Interest3']
    years_text = request.form['Years3']
    inflation = request.form['Inflation3']
    principal = float(principal_text)
    interest = float(interest_text)
    years = float(years_text)
    inflation = float(inflation)
    try:
        result = calculate_return(principal, interest, years, inflation = inflation)[0]
    #return value
        return(
        render_template('real_interest.html',
                         Principal3 = principal,
                         Interest3 = interest,
                         Years3 = years,
                         result3 = result,
                         Inflation3 = inflation,
                         calculation_success3 = True
                         ))
    #return error messages if exceptions
    except ValueError:
         return (render_template('real_interest.html',
                         Principal3 = principal,
                         Interest3 = interest_text,
                         Years3 = years,
                         result3 = result,
                         calculation_success3 = False,
                         error = "Cannot perform operations with provided input"
                         ))
#Real interest taxed
@app.route('/real_interest_taxed/', methods = ['GET'])
def real_interest_taxed_home():
    principal = 100
    interest = 10
    years = 10
    inflation = 2
    tax = 20
    result = calculate_return(principal,interest, years, inflation = inflation, cap_tax_rate = tax)[0]
    #return value
    return(
        render_template('real_interest_taxed.html',
                         Principal4 = principal,
                         Interest4= interest,
                         Years4 = years,
                         result4 = result,
                         Inflation4 = inflation,
                         Tax4 = tax,
                         calculation_success4 = True
                         ))
@app.route('/real_interest_taxed/', methods = ['POST'])
def real_interest_taxed():
    result = None
    #extract inputs from user submission
    principal_text = request.form['Principal4']
    interest_text = request.form['Interest4']
    years_text = request.form['Years4']
    inflation_text = request.form['Inflation4']
    tax_text = request.form['Tax4']
    principal = float(principal_text)
    interest = float(interest_text)
    years = float(years_text)
    inflation = float(inflation_text)
    tax = float(tax_text)
    try:
        result = calculate_return(principal,interest, years, inflation = inflation, cap_tax_rate = tax)[0]
    #return value
        return(
        render_template('real_interest_taxed.html',
                         Principal4 = principal,
                         Interest4= interest,
                         Years4 = years,
                         result4 = result,
                         Inflation4 = inflation,
                         Tax4 = tax,
                         calculation_success4 = True
                         ))
    #return error messages if exceptions
    except ValueError:
         return (render_template('real_interest_taxed.html',
                         Principal4 = principal,
                         Interest4 = interest_text,
                         Years4 = years,
                         result4 = result,
                         Inflation4 = inflation,
                         Tax4 = tax,
                         calculation_success4 = False,
                         error = "Cannot perform operations with provided input"
                         ))
        
@app.route("/capital_gains/", methods = ["GET"])
def capital_gains_home():
    income = 10000
    status = "Married, filing jointly"
    tax_rate = calculate_tax_rate(income, status)
    return(render_template('capital_gains_calculator.html',
                           income = income,
                           status = status,
                           tax_rate = tax_rate,
                           calculation_success5= True))
@app.route("/capital_gains/", methods = ['POST'])
def capital_gains_calculator():
    income = float(request.form["Income"])
    status = request.form["Status"].lower()
    try:
        tax_rate = calculate_tax_rate(income, status)
        return(render_template('capital_gains_calculator.html',
                               income = income,
                               status = status,
                               tax_rate = tax_rate,
                               calculation_success5= True))
    #return error messages if exceptions
    except ValueError:
        return(render_template('capital_gains_calculator.html',
                               income = income, 
                               status = status,
                               calculation_success5= False,
                               error = "Cannot perform operations with provided input"))
        
#Historical returns
@app.route("/historical_returns/", methods = ["GET"])
def historical_returns_home():
    amount= 100
    investment_choice = "S&P 500"
    purchase_year= 2010
    sale_year = 2020
    tax_rate = 20
    df = historical_returns(returns_df, investment_choice, amount, purchase_year, sale_year, tax_rate)
    investment_amount = float(df["Initial investment amount"])
    nominal_sale_price = float(df["Nominal sale price"])
    real_sale_price = float(df["Real sale price"])
    tax = float(df["Tax"])
    nominal_sale_price_tax = float(df["Nominal sale price minus tax"])
    real_end_value_tax = float(df["Real value of nominal sale price minus tax"])
    real_return_tax = float(df["Real return including inflation and tax"])
    for col in df.columns:
       df[col] = df[col].apply(lambda x: "${:.2f}".format((x)))
    return (render_template('historical_returns_calculator.html',
                            tables = [df.to_html(classes = 'data')], 
                            purchase_year = purchase_year,
                            sale_year = sale_year, 
                            titles = df.columns.values,
                            investment_amount = investment_amount,
                            investment_choice = investment_choice,
                            nominal_sale_price = nominal_sale_price,
                            real_sale_price = real_sale_price,
                            tax = tax,
                            nominal_gain = nominal_sale_price - investment_amount,
                            tax_rate = tax_rate,
                            nominal_sale_price_tax = nominal_sale_price_tax,
                            real_end_value_tax = real_end_value_tax,
                            real_return_tax = real_return_tax,
                            calculation_success6 = True))

@app.route('/historical_returns/', methods = ['POST'])
def historical_returns_calculator():
    amount= float(request.form["Investment amount"])
    investment_choice = request.form["Investment choice"]
    purchase_year= int(request.form["Purchase year"])
    sale_year = int(request.form["Sale year"])
    tax_rate = float(request.form["Capital gains tax rate"])
    try:
        df = historical_returns(returns_df, investment_choice, amount, purchase_year, sale_year, tax_rate)
        investment_amount = float(df["Initial investment amount"])
        nominal_sale_price = float(df["Nominal sale price"])
        real_sale_price = float(df["Real sale price"])
        tax = float(df["Tax"])
        nominal_sale_price_tax = float(df["Nominal sale price minus tax"])
        real_end_value_tax = float(df["Real value of nominal sale price minus tax"])
        real_return_tax = float(df["Real return including inflation and tax"])
        for col in df.columns:
           df[col] = df[col].apply(lambda x: "${:.2f}".format((x)))
        return (render_template('historical_returns_calculator.html',
                                tables = [df.to_html(classes = 'data')], 
                                purchase_year = purchase_year,
                                sale_year = sale_year, 
                                titles = df.columns.values,
                                investment_amount = investment_amount,
                                investment_choice = investment_choice,
                                nominal_sale_price = nominal_sale_price,
                                real_sale_price = real_sale_price,
                                tax = tax,
                                nominal_gain = nominal_sale_price - investment_amount,
                                tax_rate = tax_rate,
                                nominal_sale_price_tax = nominal_sale_price_tax,
                                real_end_value_tax = real_end_value_tax,
                                real_return_tax = real_return_tax,
                                calculation_success6 = True))
    
    except ValueError:
        return (render_template('historical_returns_calculator.html',
                                tables = [df.to_html(classes = 'data')], 
                                purchase_year = purchase_year,
                                sale_year = sale_year, 
                                titles = df.columns.values,
                                investment_amount = investment_amount,
                                investment_choice = investment_choice,
                                nomminal_sale_price = nominal_sale_price,
                                real_sale_price = real_sale_price,
                                tax = tax,
                                tax_rate = tax_rate,
                                nominal_sale_price_tax = nominal_sale_price_tax,
                                nominal_gain = nominal_sale_price - investment_amount,
                                real_end_value_tax = real_end_value_tax,
                                real_return_tax = real_return_tax,
                                error = "Cannot perform operations with provided input",
                                calculation_success6 = False))

#Real interest calculation, including tax
if __name__ == '__main__':
    app.debug = True
    app.run()
