# Stock-Notifier

# Introduction
This web application allows users to receive notifications when the price of a given stock reaches a certain threshold. Users can specify the stock ticker symbol, the price threshold, the frequency at which the stock's price should be checked, and the type of notification they would like to receive.

Prerequisites
Before you can use this application, you will need to install the following software on your machine:

- Python 3
- Flask
- yfinance
- requests

# Setting up the application
To set up the application, follow these steps:

## Clone the repository:

- git clone https://github.com/kashindra-mahato/Stock-Notifier/

## Edit the config.json
- provide your credentials for gmail and twilio
- follow the following instruction to get the gmail app password https://support.google.com/mail/answer/185833?hl=en-GB
- create account for twilio at https://www.twilio.com/ to get its credentials. It provides free trial.

## Install the required dependencies:

pip install -r requirements.txt

## Run the application:

flask run

# Using the application
To use the application, follow these steps:

- Navigate to the application's home page through localhost.

- Enter the stock ticker symbol, price threshold, frequency, and notification preferences in the form provided.

- Enter submit.

# Troubleshooting
If you encounter any issues while using the application, try the following troubleshooting steps:

1. Make sure that you have installed all of the required dependencies and set the appropriate environment variables.

2. Check the application's logs for any error messages that might help to identify the problem.

3. If the problem persists, please open an issue on the GitHub repository for the application.
