import argparse
import csv
import operator
from decimal import Decimal, InvalidOperation
from re import sub

import requests

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
        money = Decimal(sub(r"[^\d.]", "", s))
    except InvalidOperation:
        money = Decimal("0.0")
    return money


class Line:
    """Line represents an individual line in the file."""

    def __init__(self, row):
        self.id = row[0]
        self.name = row[1]
        self.price = force_money(row[4])
        self.cost = force_money(row[3])

        # If not valid, don't bother finishing
        if not self.is_valid:
            return

        self.profit = self.price - self.cost
        self.profitp = round(self.profit / self.cost * Decimal("100"))

    @property
    def is_valid(self):
        if ";" in self.id or "ID" in self.id:
            return False
        if not self.price or not self.cost:
            return False
        return True


def process():
    for row in reader:
        line = Line(row)
        if line.is_valid:
            output.append(line)

    output.sort(key=operator.attrgetter("profit"), reverse=args.least)
    print("ID  Production Cost     Sell Price  Profit($) Profit(%)  Name")
    for l in output[: args.n]:
        print(
            f"""{l.id:<4} {l.cost:>14,} {l.price:>14,} {l.profit:>10,} {l.profitp:>9}  {l.name}"""
        )


if __name__ == "__main__":
    process()
