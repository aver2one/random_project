import argparse
import csv
import requests
from re import sub

# Optional command line argument to specify number of lines to show default 10
parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    type=int,
    default=10,
    help="specify number of line items to show (default: 10)",
)
# Optional command line argument to show least profitable default most
parser.add_argument(
    "-least",
    action="store_false",
    default=True,
    help="the least profitable will be shown (default: most)",
)

args = parser.parse_args()

url = (
    "https://raw.githubusercontent.com/HexoCraft/MemWorth/"
    "master/tools/Minecraft%20Economy%20Manager.csv"
)

data = requests.get(url).text
lines = data.splitlines()
reader = csv.reader(lines, delimiter=";")
output = []


def force_money(s):
    """force_money returns a float from a string while handling some weirdness of this file.

    This implementation is naive since. We know this document uses commas instead of
    period for the decimal separator. So we change the comma into a period to preserve.
    This would not work with UTF-8 or en-US currencies, since commas are just for
    readability. There are better ways with the locale package.

    """
    s = s.replace(",", ".")
    try:
        money = float(sub(r"[^\d.]", "", s))
    except ValueError:
        money = float(0.0)
    return money


print("ID  Production Cost  Sell Price  Profit($) Profit(%)  Name")
for row in reader:
    id = row[0]
    name = row[1]
    price = force_money(row[4])
    cost = force_money(row[3])
    if price and cost:
        profit = price - cost
        if profit != 0:
            # Percentage of profit
            profitp = round(profit / cost * 100)
            # Ignore sub items rows.
            if ";" not in id:
                if "ID" not in id:
                    result = [id, cost, price, profit, profitp, name]
                    output.append(result)

output.sort(key=lambda output: output[3], reverse=args.least)
for row in output[: args.n]:
    print(
        f"""{row[0]:<4} {row[1]:<14}  {row[2]:<11} {row[3]:<10} {row[4]:<9} {row[5]:<11}"""
    )
