import requests as req
from bs4 import BeautifulSoup
import re
import pandas as pd
import os


years = {}

def main(): 
    for date in range(1990, 2023, 2):
        response = req.get('https://www.opensecrets.org/industries/summary.php?ind=E&recipdetail=S&sortorder=A&mem=Y&cycle='+str(date))
        if response.status_code == 200: 
            years[date] = get_table_data(html = response.text, date=date)

    pd.DataFrame(years).to_csv(os.path.join('data', 'Senate_lobby_totals_by_year.csv'))

def get_table_data(html,date): 
    
    values = {}
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Access and display HTML tags
    table = soup.find('table', {'class': 'datadisplay'})
    # Iterate through the rows of the table
    for row in table.find_all('tr'):

        negative = False
        # Iterate through the cells of each row

        cells = row.find_all('td')

        if len(cells) > 0: 

            name = str(cells[0].get_text())

            #store number in varibale and check if it is negative
            num = str(cells[1].get_text())
            if '-' in num: 
                negative = True
            
            #eliminate non numeric characters
            num = re.sub("[^0-9]", "", num)
            
            #account for numbers being negative since negative sign is stripped earlier
            if negative: 
                num = int(num) * -1

            values[name] = num

    return values
        
     
    

main() 