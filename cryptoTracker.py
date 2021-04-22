import requests
from bs4 import BeautifulSoup
import os
import time
from colorama import Fore, Style


def notification(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


# clear terminal
print(chr(27) + "[2J")

# Getting prices
# Ensuring valid
while True:
    try:
        invariable = input(f"{Fore.YELLOW}Crypto to watch: {Style.RESET_ALL}")
        result = requests.get("https://www.coindesk.com/price/" + invariable)
        # Storing the value
        source = result.content
        soup = BeautifulSoup(source, 'lxml')
        # Price for printing
        priceDiv = soup.find("div", {"class": "price-large"})
        priceString = priceDiv.text
        break
    except AttributeError:
        print(f"{Fore.RED}\n\n!! please enter a valid crypto !! \n\n")
        print(f"{Fore.GREEN}currencies include:\n")
        print(
            f"{Fore.YELLOW}bitcoin\nethereum\nxrp\ncardano\n{Fore.CYAN}&more\n\n {Style.RESET_ALL}")


priceFloat = priceString[1:len(priceString)]

# Price for maths
priceFloat = priceFloat.replace(',', '')
priceFloat = float(priceFloat)


# clear terminal
print(chr(27) + "[2J")

while True:
    try:
        percentChange = float(
            input(f"{Fore.CYAN}percentage change before notification?: {Style.RESET_ALL}"))
        break
    except ValueError:
        print(
            f'\n\n{Fore.RED}!! please enter a valid percent, without the "%" sign{Style.RESET_ALL}\n\n')


# Keeps calling, updating the values when needed
print(chr(27) + "[2J")
print(
    f"\n\n{Fore.WHITE}You're all good to go! You will be notified when")
print(f"{Fore.YELLOW}"+invariable+f"{Fore.WHITE} goes {Fore.GREEN}up{Fore.WHITE}/{Fore.RED}down {Fore.WHITE}" +
      str(percentChange)+f"%.{Style.RESET_ALL}\n\n")


def priceTest(coinName, coinPrice, percentNeeded):

    # Same as before, finding the price.
    result = requests.get("https://www.coindesk.com/price/" + invariable)
    # Storing the value
    source = result.content
    soup = BeautifulSoup(source, 'lxml')
    # Price for printing
    priceDiv = soup.find("div", {"class": "price-large"})
    priceString = priceDiv.text
    priceFloat = priceString[1:len(priceString)]
    # Price for maths
    priceFloat = priceFloat.replace(',', '')
    priceFloat = float(priceFloat)
    return priceFloat


def timeLoop(coinName, originalPrice, changeNeeded):
    while True:
        returnPrice = priceTest(coinName, originalPrice, changeNeeded)

        # checking if we need to notify:
        if(returnPrice >= (originalPrice + originalPrice*(changeNeeded/10)) or returnPrice <= originalPrice - originalPrice*(changeNeeded/10)):
            return returnPrice

        time.sleep(2)


updatedPrice = timeLoop(invariable, priceFloat, percentChange)

changeAsPercent = ((updatedPrice - priceFloat)/priceFloat) * 100

if changeAsPercent > 0:
    notificationText = invariable + " is up " + \
        str(abs(round(changeAsPercent, 3))) + "%, at $" + str(updatedPrice)
else:
    notificationText = invariable + " is down " + \
        str(abs(round(changeAsPercent, 3))) + "%, at $" + str(updatedPrice)


notification(invariable, notificationText)
