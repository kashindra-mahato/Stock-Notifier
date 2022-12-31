from flask import Flask, render_template, request, redirect
import yfinance as yf
import smtplib
import sched
import time
from twilio.rest import Client
import json



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-alert', methods=['POST'])
def send_alert():
  # Get the form data
  ticker = request.form['ticker']
  threshold = request.form['threshold']
  frequency = request.form['frequency']
  notification_type = request.form['notification_type']
  

  # Set up the scheduler
  scheduler = sched.scheduler(time.time, time.sleep)

  # Get the stock data for the ticker
  try:
    stock_data = yf.Ticker(str(ticker)).info
    # Get the closing price from the stock data
    current_price = stock_data['regularMarketPreviousClose']
  
  except Exception as e:
    # Handle the error
    print(f'An error occurred: {e}')
    # Render the error template
    return render_template('error.html', ticker=ticker)

  # Check if the current price has crossed the threshold
  if current_price > float(threshold):
    # Send the notification
    send_notification(notification_type, ticker, current_price, threshold)
    # Render the stock data template and pass in the stock data
    return render_template('stock_data.html', stock_data=stock_data)
  else:
    # Schedule the send_alert function to run again at the specified frequency
    if frequency == 'hourly':
      scheduler.enter(3600, 1, send_alert)
    elif frequency == 'daily':
      scheduler.enter(86400, 1, send_alert)
    elif frequency == 'weekly':
      scheduler.enter(604800, 1, send_alert)
    # Render a template indicating that the current price has not crossed the threshold
    return render_template('alert_not_triggered.html', stock_data=stock_data, ticker=ticker, current_price=current_price, threshold=threshold)
  # Run the scheduler
  scheduler.run()

def send_notification(notification_type, ticker, current_price, threshold):
  if notification_type == 'email':
    send_email_notification(ticker, current_price, threshold)
  elif notification_type == 'text':
    send_text_notification(ticker, current_price, threshold)

def send_email_notification(ticker, current_price, threshold):
  # Load the configuration file
  with open('config.json', 'r') as f:
    config = json.load(f)
  # Get the email server and port from the configuration file
  server = config['email']['server']
  port = config['email']['port']

  # Set up the email server
  server = smtplib.SMTP(server, port)
  server.starttls()

  # Get the username and password from the configuration file
  username = config['email']['username']
  password = config['email']['password']

  # Login to the email server
  server.login(username, password)

  # Send the email
  subject = 'Stock Alert: {}'.format(ticker)
  body = 'The price of {} has crossed the threshold of {}. The current price is {}.'.format(ticker, threshold, current_price)
  message = 'Subject: {}\n\n{}'.format(subject, body)
  email = request.form['email_address']
  server.sendmail(str(username), str(email), message)
  server.quit()


def send_text_notification(ticker, current_price, threshold):
  # Load the configuration file
  with open('config.json', 'r') as f:
    config = json.load(f)
  # Get the Twilio account SID and auth token from the configuration file
  account_sid = config['twilio']['account_sid']
  auth_token = config['twilio']['auth_token']

  # Set up the Twilio client
  client = Client(account_sid, auth_token)

  # Get the Twilio phone number from the configuration file
  from_ = config['twilio']['phone_number']

  # Set up the message parameters
  to = request.form['phone_number']
  body = 'The price of {} has crossed the threshold of {}. The current price is {}.'.format(ticker, threshold, current_price)

  # Send the message
  message = client.messages.create(to=to, from_=from_, body=body)
  print('Message sent: {}'.format(message.sid))

if __name__ == '__main__':
  app.run()
