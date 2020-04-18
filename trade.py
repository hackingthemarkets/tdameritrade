from tda import auth, client
from tda.orders import EquityOrderBuilder, Duration, Session
import json
import config
import datetime

# authenticate
try:
    c = auth.client_from_token_file(config.token_path, config.api_key)
except FileNotFoundError:
    from selenium import webdriver
    with webdriver.Chrome(executable_path=config.chromedriver_path) as driver:
        c = auth.client_from_login_flow(
            driver, config.api_key, config.redirect_uri, config.token_path)

# get price history for a symbol
r = c.get_price_history('AAPL',
        period_type=client.Client.PriceHistory.PeriodType.YEAR,
        period=client.Client.PriceHistory.Period.TWENTY_YEARS,
        frequency_type=client.Client.PriceHistory.FrequencyType.DAILY,
        frequency=client.Client.PriceHistory.Frequency.DAILY)

print(json.dumps(r.json(), indent=4))

# get a stock quote
response = c.get_quote('AAPL')

print(response.json())

# get stock fundamental data
response = c.search_instruments(['AAPL', 'BA'], c.Instrument.Projection.FUNDAMENTAL)

print(json.dumps(response.json(), indent=4))

# get option chain
response = c.get_option_chain('AAPL')

print(json.dumps(response.json(), indent=4))

# get all call options
response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL)

print(json.dumps(response.json(), indent=4))

# get call options for a specific strike
response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=300)

print(json.dumps(response.json(), indent=4))

# get call options for a specific strike and date range
start_date = datetime.datetime.strptime('2020-04-24', '%Y-%m-%d').date()
end_date = datetime.datetime.strptime('2020-05-01', '%Y-%m-%d').date()

response = c.get_option_chain('AAPL', contract_type=c.Options.ContractType.CALL, strike=300, strike_from_date=start_date, strike_to_date=end_date)

print(json.dumps(response.json(), indent=4))

# limit order of 5 shares of redfin stock at 18 dollars a share
builder = EquityOrderBuilder('RDFN', 5)
builder.set_instruction(EquityOrderBuilder.Instruction.BUY)
builder.set_order_type(EquityOrderBuilder.OrderType.LIMIT)
builder.set_price(18)
builder.set_duration(Duration.GOOD_TILL_CANCEL)
builder.set_session(Session.NORMAL)

response = c.place_order(config.account_id, builder.build())

print(response)