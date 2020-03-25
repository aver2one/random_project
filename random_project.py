import csv
import pandas as pd

# Open and parse the file 
df = pd.read_csv('https://raw.githubusercontent.com/HexoCraft/MemWorth/'
	'master/tools/Minecraft%20Economy%20Manager.csv',
sep=None, engine='python', header=5)

#ignore non-line item rows AND ignore sub items rows.
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

# Determine the dollar amount of profit for each line item based on the production cost vs the sell price
df['Profit ($)'] = df['Sell Price'] - df['Production Cost'] 

#Determine the percentage of profit
df['Profit (%)'] = df['Profit ($)'] / df['Production Cost'] * 100

#Sort by the most profitable
df.sort_values(by=['Profit ($)'], inplace=True, ascending=False)

#Output ID, Production Cost, Sell Price, Profit ($), Profit (%), Name
df = df[['ID', 'Production Cost', 'Sell Price', 'Profit ($)', 'Profit (%)', 'Name'  ]]

#Format and print out top 10 getting rid of the index
print(df.head(n=10).to_string(index=False, justify='center'))




#Display for testing
#df.to_excel("output.xlsx") 
# print(df)