import requests as req
from bs4 import BeautifulSoup

def main(): 
    for date in range(1990, 2023, 2):
        response = req.get('https://www.opensecrets.org/industries/summary.php?ind=E&recipdetail=S&sortorder=A&mem=Y&cycle='+str(date))
        if response.status_code == 200: 
            get_table_data(html = response.text)

def get_table_data(html): 
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Access and display HTML tags
    table = soup.find('table', {'class': 'datadisplay'})
    # Iterate through the rows of the table
    for row in table.find_all('tr'):
        # Iterate through the cells of each row
        for cell in row.find_all('td'):
            # Extract and process the data from each cell
            data = cell.get_text()
            print(data + 'dfdsfsdf\n\n\n\n\n')


main() 