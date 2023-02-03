# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 14:08:00 2023

@author: Ryed Badr
"""

from datetime import datetime
import pandas as pd
import sys
#Dependancies

# transaction takes in an integer as a parameter and simulates a transaction of that amount
def transaction(amount):
    transactions = pd.read_csv("transactions.csv")
    df_transactions = pd.DataFrame(transactions)
    # ^Read in the csv file and store it in a DataFrame
    
    balances = {}
    for index in range(len(df_transactions.index)):
        date = df_transactions.iloc[index]['timestamp']
        date_formatted = date[0:len(date) - 1]
        date_to_int = datetime.fromisoformat(date_formatted).timestamp()
        df_transactions.loc[index,'timestamp'] = date_to_int
    # ^Normalize the dates and put them in an easy to comapre integer format 
    
        people = df_transactions.iloc[index]['payer']
        if people in balances:
            balances[people] += df_transactions.iloc[index]['points']
        else:
            balances[people] = df_transactions.iloc[index]['points']
    # ^Put the total balances of each payer in a map
    
    while (amount > 0):
    # ^Run this until the remaining amount of points is fully paid
    
        oldest_date = [list(df_transactions.index.values)[0],0,df_transactions.iloc[0]['timestamp']]
        for index in range(len(df_transactions.index)):
            if df_transactions.iloc[index]['timestamp'] < oldest_date[2]:
                oldest_date = [list(df_transactions.index.values)[index], index, df_transactions.iloc[index]['timestamp']]
        oldest_payer_points = balances[df_transactions.iloc[oldest_date[1]]['payer']]
        oldest_transaction = df_transactions.iloc[oldest_date[1]]['points']
        # ^Find and initialize the oldest payment date, total points of the payer, and the points of the oldest transaction
        
        if oldest_transaction < amount and oldest_payer_points - oldest_transaction >= 0:
            amount -= oldest_transaction
            balances[df_transactions.iloc[oldest_date[1]]['payer']] -= oldest_transaction
            df_transactions = df_transactions.drop(labels=oldest_date[0], axis=0)
        elif oldest_transaction > amount:
            balances[df_transactions.iloc[oldest_date[1]]['payer']] -= amount
            amount = 0
            break
        # ^Updates the remaining balance due and the total points for the account with the oldest transaction
        # If the total amount is paid, the program stops running
        
    return balances
    # ^Returns a map of all the total balances post transaction        
            
if __name__ == "__main__":
    try:
        transaction_amount = int(sys.argv[1])
        print(transaction(transaction_amount))
    except:
        transaction_amount = int(input("Error Running... Enter Transaction Amount Here Now: "))
        print(transaction(transaction_amount))
# ^Driver