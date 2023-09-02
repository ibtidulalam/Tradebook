# Tradebook
A real-time stock monitoring and management tool that allows users to add, remove, and analyze stocks in their portfolio. The application fetches real-time data from Yahoo Finance and provides a variety of metrics, including current price, moving average, trading volume, and more.

**Real-Time Stock Monitor**
**Description**
A real-time stock monitoring and management tool written in Python. This application uses Yahoo Finance's API to provide real-time stock data, including current price, moving average, trading volume, and more. You can add and remove stocks to your 'Trading Book' and keep track of your investments.

**Features**
Add stocks to your portfolio by stock symbol.
Real-time monitoring of stock prices.
View moving averages, highest and lowest price of the day, and more.
Calculates profit based on previous day closing price.
Simple and easy-to-use console interface.
Requirements
Python 3.x
yfinance
pandas


**Installation**
bash
pip install yfinance pandas
Usage
Run stock.py to start the application. Follow the on-screen prompts to manage your trading book.

bash
python stock.py
License
MIT License

requirements.txt
makefile
yfinance==0.1.63
pandas==1.3.3
You can generate this file manually or by running pip freeze > requirements.txt in your virtual environment.

**.gitignore**
markdown
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/

# Text files
trading_book.txt
