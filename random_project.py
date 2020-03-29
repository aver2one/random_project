#This version is using Pandas
import argparse
import csv
import pandas as pd


# Optional command line argument to specify number of lines to show default 10
parser = argparse.ArgumentParser()
parser.add_argument('-n', type=int, default=10,
                    help='specify number of line items to show (default: 10)')
# Optional command line argument to show least profitable default most                    
parser.add_argument('-least', action='store_true', default=False,
                    help='the least profitable will be shown (default: most)')

args = parser.parse_args()

# Open and parse the file 
df = pd.read_csv('https://raw.githubusercontent.com/HexoCraft/MemWorth/'
	'master/tools/Minecraft%20Economy%20Manager.csv',
sep=None, engine='python', header=5)

# Ignore non-line item rows AND ignore sub items rows.
df = df[~df.ID.str.contains(";")]
df = df[ df['Quantity'].notna()]
df = df[ df['Production Cost'].notna()]
df = df[ df['Sell Price'].notna()]

# Remove non-digits from string
df['Sell Price'] = df['Sell Price'].str.replace(r'\D+', '')
df['Production Cost'] = df['Production Cost'].str.replace(r'\D+', '')

# Converting Strings (objects) to ints
df['Production Cost'] = df['Production Cost'].astype(int)
df['Sell Price'] = df['Sell Price'].astype(int)

# Dollar amount of profit for each line item
# This is based on the production cost vs the sell price
df['Profit ($)'] = df['Sell Price'] - df['Production Cost'] 

#Determine the percentage of profit
df['Profit (%)'] = df['Profit ($)'] / df['Production Cost'] * 100

#Ignoring non line items in profits
df = df[ df['Profit (%)'].notna()]

#Sort by the most profitable
df.sort_values(by=['Profit ($)'], inplace=True, ascending=args.least)

#Output ID, Production Cost, Sell Price, Profit ($), Profit (%), Name
df = df[['ID', 'Production Cost', 'Sell Price', 'Profit ($)', 'Profit (%)', 'Name'  ]]

#Format and print out top 10 getting rid of the index
print(df.head(n=args.n).to_string(index=False, justify='center'))
