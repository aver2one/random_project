import argparse
import csv
import operator
from decimal import Decimal, InvalidOperation
from re import sub

import requests

URL = "https://raw.githubusercontent.com/HexoCraft/MemWorth/master/tools/Minecraft%20Economy%20Manager.csv"


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

    def __str__(self):
        return f"{self.id:<4} {self.cost:>14,} {self.price:>14,} {self.profit:>10,} {self.profitp:>9}  {self.name}"

    @property
    def is_valid(self):
        if ";" in self.id or "ID" in self.id:
            return False
        if not self.price or not self.cost:
            return False
        return True


class LineList:
    def __init__(self, rows, num_lines, order):
        self.num_lines = num_lines
        self.lines = []
        for row in rows:
            line = Line(row)
            if line.is_valid:
                self.lines.append(line)

        self.lines.sort(key=operator.attrgetter("profit"), reverse=order)

    def __iter__(self):
        return iter(self.lines[: self.num_lines])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        type=int,
        default=10,
        help="specify number of line items to show (default: 10)",
    )
    parser.add_argument(
        "-least",
        action="store_false",
        default=True,
        help="the least profitable will be shown (default: most)",
    )
    args = parser.parse_args()

    print("ID  Production Cost     Sell Price  Profit($) Profit(%)  Name")
    lines = requests.get(URL).text.splitlines()
    rows = csv.reader(lines, delimiter=";")
    for line in LineList(rows, args.n, args.least):
        print(line)
