import cbpro
from collections import deque
import time as datetime
import math

# Get new API keys
api_key = '{{Insert your API KEY here}}'
api_secret = '{{API SECRET}}'
passphrase = '{{Passphrase}}'

auth_client = cbpro.AuthenticatedClient(api_key, api_secret, passphrase)

# Get the current price every second and store it in an array
def invest(currency, ten_scale = 0.001, thirty_scale = 0.002, fifty_five_scale = 0.002, hold_time=60*4):
    arr = deque()
    amount = 0
    start_time = int(datetime.time())
    print("DEBUGGING timer: ", start_time)
    trade_timer = -1

    # First populate array
    print("Populating array")
    while len(arr) < 12:
        current_price = float(auth_client.get_product_ticker(product_id=currency + '-USD')['price'])
        print("Appending ", current_price)
        arr.append(current_price)
        print("Current List: ", [x for x in arr])
        datetime.sleep(5)

    while len(arr) == 12:
        print("Entering investment loop")
        # Append time
        current_price = float(auth_client.get_product_ticker(product_id=currency + '-USD')['price'])
        print("Appending ", current_price)
        arr.append(current_price)
        arr.popleft()
        print("Current list ", [x for x in arr])
        # 10s check
        if (arr[11] - arr[9])/arr[9] > 0.0025:
            print("Executing investment based off of 10s movement")
            scale = ten_scale
            temp_ammount = scale*f(trade_timer, int(datetime.time()))
            amount += temp_ammount
            execute_trade(temp_ammount, currency, post_only=True)
            execute_trade(temp_ammount, currency, post_only=False)
            if trade_timer == -1:
                trade_timer = int(datetime.time())
                print("Timer Started")
        # 30s check
        if (arr[11] - arr[5])/arr[5] > 0.004:
            print("Executing investment based off of 30s movement")
            scale = thirty_scale
            temp_ammount = scale*f(trade_timer, int(datetime.time()))
            amount += temp_ammount
            execute_trade(temp_ammount, currency, post_only=True)
            execute_trade(temp_ammount, currency, post_only=False)
            if trade_timer == -1:
                trade_timer = int(datetime.time())
                print("Timer Started")
        # 55s check
        if (arr[11] - arr[0])/arr[0] > 0.007:
            print("Executing investment based off of 55s movement")
            scale = fifty_five_scale
            temp_ammount = scale*f(trade_timer, int(datetime.time()))
            amount += temp_ammount
            execute_trade(temp_ammount, currency, post_only=True)
            execute_trade(temp_ammount, currency, post_only=False)
            if trade_timer == -1:
                trade_timer = int(datetime.time())
                print("Timer Started")
        # Some user info
        if (trade_timer != -1):
            print("Seconds left holding: ", hold_time - (int(datetime.time()) - trade_timer))
        # Sell if four minutes have elapsed
        if (trade_timer != -1) and ((int(datetime.time()) - trade_timer) > hold_time):
            # Drop entire position
            trade_timer = None
            execute_sell(amount/2, currency, post_only=True)
            execute_sell(amount/2, currency, post_only=False)
            amount = 0

        datetime.sleep(4.8)

# Scale down calculator
def f(trade_timer, curr_time):
    if trade_timer == -1:
        return 1
    else:
        trade_timer = curr_time - trade_timer
        ret = trade_timer/60
        ret += 1
        return 1/ret

# Execute buy orders
def execute_trade(volume, currency, post_only=True, epsilon = 0.0):
    # Get the price to open the maker order at
    # Ensure it does not cost anything
    price = float(auth_client.get_product_ticker(product_id=currency + '-USD')['price']) - epsilon
    # Execute buy order as a either a  maker or taker
    if post_only:
        resp = auth_client.buy(price = str(price), #USD
                   order_type='limit',
                   size = str(volume), #BTC
                   product_id = currency + '-USD',
                   tif = 'GTT',
                   time_in_force = 'GTT',
                   cancel_after = 'min',
                   post_only = 'true')
    else:
        resp = auth_client.buy(price = str(price), #USD
                   order_type='limit',
                   size = str(volume), #BTC
                   product_id = currency + '-USD',
                   tif = 'GTT',
                   time_in_force = 'GTT',
                   cancel_after = 'min',
                   post_only = 'false')
    if resp['status'] == 'rejected':
        print("*********************** ---- PURCHASE FAILED RESETTING ---- ***********************")
        print(resp['status'])
        print(resp['reject_reason'])
        execute_trade(volume, currency, post_only=True, epsilon = 0.01)
        return False
    else:
        print("*********************** ---- PURCHASE EXECUTED ---- ***********************")
        print("VOLUME: ", volume)
        print("USD: ", float(volume)*float(price))
        print("CURRENCY: ", currency)
        print("PRICE: ", price)
        print("\n")
        return True

# Execute sell orders
def execute_sell(volume, currency, post_only=True, epsilon = 0.00):
    # Sell
    price = float(auth_client.get_product_ticker(product_id=currency + '-USD')['price']) + epsilon
    # Execute buy order as a maker
    if post_only:
        resp = auth_client.sell(price = str(price), #USD
                   order_type='limit',
                   size = str(volume), #BTC
                   product_id = currency + '-USD',
                   post_only = 'true')
    else:
        resp = auth_client.sell(price = str(price), #USD
                   order_type='limit',
                   size = str(volume), #BTC
                   product_id = currency + '-USD',
                   post_only = 'false')
    if resp['status'] == 'rejected':
        print("*********************** ---- SALE FAILED ---- ***********************")
        print(resp['status'])
        print(resp['reject_reason'])
        execute_sell(volume, currency, post_only=True, epsilon = 0.01)
        return False
    else:
        print("*********************** ---- SALE EXECUTED ---- ***********************")
        print("VOLUME: ", volume)
        print("USD: ", float(volume)*float(price))
        print("CURRENCY: ", currency)
        print("PRICE: ", price)
        print("\n")
        return True

# Handles what we're doing yo
if __name__ == "__main__":
    import sys
    arg = sys.argv[1]

    if (arg == "t" or arg == "trade" or arg == "fuckyeah" or arg == "peterpan"):
        print("Running Investor")
        invest('BTC')
    elif (arg == "d" or arg == "debbugger"):
        # train.gen_train_test_data()
        print("Testing INvestor ")
        # invest('BTC', ten_scale = 0.001, hold_time = 30)
        execute_trade(0.001, 'BTC', post_only=True)
