import yfinance as yf
import time
import datetime

def is_valid_stock(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info is not None
    except:
        return False

def fetch_stock_details(symbol, window_size=5):
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        stock_name = info.get('longName', 'Unknown')
        stock_data = yf.download(symbol, period='1d', interval='1m', progress=False)  # Set progress to False
        latest_price = stock_data['Close'].iloc[-1]
        opening_price = stock_data['Open'].iloc[0]
        highest_price = stock_data['High'].max()
        lowest_price = stock_data['Low'].min()
        volume = stock_data['Volume'].sum()
        moving_average = sum(stock_data['Close'].tolist()[-window_size:]) / window_size
        return stock_name, symbol, latest_price, moving_average, opening_price, highest_price, lowest_price, volume
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def save_trading_book(trading_book):
    with open("trading_book.txt", "w") as f:
        for symbol, details in trading_book.items():
            f.write(f"{symbol},{details['amount_owned']}\n")

def load_trading_book():
    trading_book = {}
    try:
        with open("trading_book.txt", "r") as f:
            lines = f.read().strip().split("\n")
            for line in lines:
                parts = line.split(",")
                if len(parts) == 2:
                    symbol, amount_owned = parts
                    trading_book[symbol] = {'amount_owned': float(amount_owned), 'details': None}
                else:
                    print(f"Skipping malformed line: {line}")
    except FileNotFoundError:
        pass
    return trading_book


    
def clear_trading_book(trading_book):
    trading_book.clear()
    with open("trading_book.txt", "w") as f:
        f.write("")

def calculate_profit(current_price, prev_close_price, amount_owned):
    if prev_close_price is not None:
        return (current_price - prev_close_price) * amount_owned
    return None

def fetch_prev_close_price(symbol):
    today = datetime.date.today()
    last_trading_day = today - datetime.timedelta(days=1)

    while last_trading_day.weekday() >= 5:
        last_trading_day -= datetime.timedelta(days=1)
        
    stock_data = yf.download(symbol, start=last_trading_day, end=last_trading_day + datetime.timedelta(days=1), progress=False)  # Set progress to False
    return stock_data['Close'].iloc[-1] if not stock_data.empty else None


if __name__ == "__main__":
    trading_book = load_trading_book()
    try:
        while True:
            action = input("Would you like to add, remove, clear all stocks, or start monitoring? (add/remove/clear/start): ").lower()
            if action == "add":
                while True:
                    symbol = input("Enter the stock symbol to add (e.g., AAPL for Apple Inc.): ").upper()
                    if is_valid_stock(symbol):
                        amount = float(input("Enter the amount of stock owned: "))
                        trading_book[symbol] = {'amount_owned': amount, 'details': None}
                        save_trading_book(trading_book)
                        break
                    else:
                        print("Invalid or not found stock symbol. Please try again.")
            elif action == "remove":
                symbol = input("Enter the stock symbol to remove: ").upper()
                if symbol in trading_book:
                    trading_book.pop(symbol, None)
                    save_trading_book(trading_book)
                else:
                    print(f"Symbol {symbol} is not in the trading book.")
            elif action == "clear":
                trading_book.clear()
                save_trading_book(trading_book)
                print("Cleared")
            elif action == "start":
                try:
                    while True:
                        total_profit_today = 0.0
                        total_value_last_closing = 0.0
                        total_value_now = 0.0
                        print("╔════════════════════════════════════════════════════════════╗")
                        print("║                         TRADEBOOK                          ║")
                        print("╟────────────────────────────────────────────────────────────╢")
                        
                        for symbol, details_dict in trading_book.items():
                            stock_details = fetch_stock_details(symbol)
                            if stock_details is not None:
                                details_dict['details'] = stock_details
                                stock_name, _, latest_price, moving_average, _, _, _, _ = stock_details
                                
                                prev_close_price = fetch_prev_close_price(symbol)
                                profit = calculate_profit(latest_price, prev_close_price, details_dict['amount_owned'])
                                
                                if profit is not None:
                                    total_profit_today += profit
                                
                                if prev_close_price is not None:
                                    total_value_last_closing += prev_close_price * details_dict['amount_owned']
                                
                                total_value_now += latest_price * details_dict['amount_owned']
                                print("--------------------------")
                                print(f"Stock: {stock_name}")
                                print(f"Ticker Symbol: {symbol}")
                                print(f"Latest Price: {latest_price}")
                                print(f"Price at Last Closing: {prev_close_price}")
                                print(f"Moving Average: {moving_average}")
                                print(f"Stock Owned: {details_dict['amount_owned']}")
                                print(f"Return: {profit}")
                                print("-------------------------")

                        print("--------------------------")
                        print(f"Total Return Today: {total_profit_today}")
                        print(f"Total Asset Value at Last Closing: {total_value_last_closing}")
                        print(f"Total Asset Value Now: {total_value_now}")
                        print("-------------------------")
                        print("╚════════════════════════════════════════════════════════════╝")
                        time.sleep(30)
                except KeyboardInterrupt:
                    print("Monitoring stopped. Returning to main menu.")
            elif action == "clear":
                clear_trading_book(trading_book)
                print("All entries have been cleared.")
            else:
                print("Invalid action. Please try again.")
    except KeyboardInterrupt:
        print("Stopped by user.")
