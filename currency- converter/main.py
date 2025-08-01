from requests import get
from pprint import PrettyPrinter

API_KEY = "1bd7c8923e7d8762fea40468"  
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}"

printer = PrettyPrinter()


def get_currencies():
    url = f"{BASE_URL}/codes"
    response = get(url).json()

    if response['result'] != 'success':
        print("Error fetching currency list.")
        return []

    return response['supported_codes']


def print_currencies(currencies):
    for code, name in sorted(currencies):
        print(f"{code} - {name}")


def exchange_rate(currency1, currency2):
    url = f"{BASE_URL}/pair/{currency1}/{currency2}"
    response = get(url).json()

    if response['result'] != 'success':
        print("Invalid currency pair or API error.")
        return None

    rate = response['conversion_rate']
    print(f"{currency1} -> {currency2} = {rate}")
    return rate


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    converted_amount = rate * amount
    print(f"{amount} {currency1} = {round(converted_amount, 2)} {currency2}")
    return converted_amount


def main():
    currencies = get_currencies()
    valid_codes = set(code for code, _ in currencies)

    print("Welcome to the currency converter!")
    print("List - lists the different currencies")
    print("Convert - convert from one currency to another")
    print("Rate - get the exchange rate of two currencies")
    print()

    while True:
        command = input("Enter a command (q to quit): ").lower()

        if command == "q":
            break
        elif command == "list":
            print_currencies(currencies)
        elif command == "convert":
            currency1 = input("Enter a base currency: ").upper()
            if currency1 not in valid_codes:
                print("Invalid base currency. Use 'list' to see valid codes.")
                continue
            amount = input(f"Enter an amount in {currency1}: ")
            currency2 = input("Enter a currency to convert to: ").upper()
            if currency2 not in valid_codes:
                print("Invalid target currency. Use 'list' to see valid codes.")
                continue
            convert(currency1, currency2, amount)
        elif command == "rate":
            currency1 = input("Enter a base currency: ").upper()
            currency2 = input("Enter a currency to convert to: ").upper()
            if currency1 not in valid_codes or currency2 not in valid_codes:
                print("Invalid currency codes. Use 'list' to see valid codes.")
                continue
            exchange_rate(currency1, currency2)
        else:
            print("Unrecognized command!")

main()
