import qrcode
from bitcoin import *
import subprocess
import numpy as np
import stripe
from coinbase.wallet.client import Client

def buy_btc(amount, addr):
  client = Client(api_key,api_secret)
  account = client.get_primary_account()
  payment_method = client.get_payment_methods()[0]
  buy_price  = client.get_buy_price(currency='USD')
  buy = account.buy(amount=amount/(buy_price*1.1),
                    currency="BTC",
                    payment_method=payment_method.id)
  tx = account.send_money(to=addr,
                                amount=amount/(buy_price*1.1),
                                currency='BTC')
def charge(number, month, year, cvc, amount):
  stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
  token = stripe.Token.create(
    card={
      "number": number,
      "exp_month": month,
      "exp_year": year,
      "cvc": cvc,
    },
  )
  stripe.Charge.create(
   amount=amount,
   currency="usd",
   source=token,
   description="My First Test Charge (created for API docs)",
  )

def create_wallet():
  my_private_key = random_key()

  my_public_key = privtopub(my_private_key)

  addr = pubtoaddr(my_public_key)
  print(addr)
  print_wallet(addr, my_private_key)
  return addr

def print_wallet(addr, my_private_key):
  data = "Your BTC address is " + addr + "and your private key is " + my_private_key
  img = qrcode.make(data)
  path = addr+'.png'
  img.save(path)
  # lpr =  subprocess.call(["/usr/bin/lp", path])

try:
  # Use Stripe's library to make requests...
  charge(4242424242424242, 03, 2021, 123, 2500)
  addr = create_wallet()
  buy_btc(25, addr)
  pass
except stripe.error.CardError as e:
  # Since it's a decline, stripe.error.CardError will be caught

  print('Status is: %s' % e.http_status)
  print('Code is: %s' % e.code)
  # param is '' in this case
  print('Param is: %s' % e.param)
  print('Message is: %s' % e.user_message)
except stripe.error.RateLimitError as e:
  # Too many requests made to the API too quickly
  pass
except stripe.error.InvalidRequestError as e:
  # Invalid parameters were supplied to Stripe's API
  pass
except stripe.error.AuthenticationError as e:
  # Authentication with Stripe's API failed
  # (maybe you changed API keys recently)
  pass
except stripe.error.APIConnectionError as e:
  # Network communication with Stripe failed
  pass
except stripe.error.StripeError as e:
  # Display a very generic error to the user, and maybe send
  # yourself an email
  pass
except Exception as e:
  # Something else happened, completely unrelated to Stripe
  print(e)
  pass

