## All the categories on <https://www.nirfindia.org/2023/Ranking.html>

import pathlib
import csv

import requests
from bs4 import BeautifulSoup

urls = [
    'https://www.nirfindia.org/2023/OverallRanking.html',
    'https://www.nirfindia.org/2023/UniversityRanking.html',
    'https://www.nirfindia.org/2023/CollegeRanking.html',
    'https://www.nirfindia.org/2023/ResearchRanking.html',
    'https://www.nirfindia.org/2023/EngineeringRanking.html',
    'https://www.nirfindia.org/2023/ManagementRanking.html',
    'https://www.nirfindia.org/2023/PharmacyRanking.html',
    'https://www.nirfindia.org/2023/MedicalRanking.html',
    'https://www.nirfindia.org/2023/DentalRanking.html',
    'https://www.nirfindia.org/2023/LawRanking.html',
    'https://www.nirfindia.org/2023/ArchitectureRanking.html',
    'https://www.nirfindia.org/2023/AgricultureRanking.html',
    'https://www.nirfindia.org/2023/InnovationRanking.html'
    ]

for url in urls:
    category = pathlib.Path(url).stem.removesuffix('Ranking')
    table = table_from_URL( url )
    
    for rank, suffix in ( ( '101-150', '150.html' ), ( '151-200', '200.html' ) ):
        table2 = table_from_URL( pathlib.Path(url).with_suffix( suffix ) )
        table.extend([ row + [rank] for row in table2 ])
    
    with open( category + '.csv', 'w' ) as f:
        csv = csv.writer( f )
        csv.writerow( 'Name,City,State,Rank,Category' )
        for row in table:
            csv.writerow( row + [category] )

## Thanks, ChatGPT
def table_from_URL( url ):
    # Fetch HTML content from the URL
    response = requests.get(url)
    if response.status_code != 200:
        raise KeyError( "URL not found. Status code:", response.status_code )
        return None
    
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table in the HTML
    table = soup.find('table')
    
    if not table:
        raise KeyError( "Table not found." )
        return None
    
    # Extract text contents of the rows
    table_data = []
    for row in table.find_all('tr'):
        row_data = [ cell.get_text(strip=True) for cell in row.find_all('td') ]
        table_data.append( row_data )
    
    return table_data
