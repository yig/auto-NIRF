## All the categories on <https://www.nirfindia.org/2023/Ranking.html>
## pip install requests beautifulsoup4

## Author: Yotam Gingold <yotam@yotamgingold.com>
## License: CC0
## URL: https://gist.github.com/yig/bc29935d22845dc02bf5000bcf18ba25

# from pathlib import Path
import csv
import os

import requests
from bs4 import BeautifulSoup

def main():
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
        ## Pathlib isn't great with 
        # category = Path(url).stem.removesuffix('Ranking')
        category = url.removesuffix('Ranking.html').split('/')[-1]
        outpath = category + '.csv'
        if os.path.exists( outpath ):
            print( "Path exists, skipping:", outpath )
            continue
        table = table_from_URL( url )

        ## Keep only the columns we want (Name, City, State, Rank)
        if category == 'Innovation':
            table = [ [ row[1], '', row[2], row[3] ] for row in table ]
        else:
            table = [ row[1:4] + [row[5]] for row in table ]
        
        for rank, suffix in ( ( '101-150', '150.html' ), ( '151-200', '200.html' ) ):
            try:
                table2 = table_from_URL( url.removesuffix('.html') + suffix )
                ## Add a rank column for this data.
                table2 = [ row + [rank] for row in table2 ]
                ## Combine tables
                table.extend( table2 )
            except KeyError as k:
                print( k )
        
        with open( outpath, 'w' ) as f:
            out = csv.writer( f )
            out.writerow( ['Name', 'City', 'State', 'Rank', 'Category'] )
            for row in table:
                out.writerow( row + [category] )
        
        print( "Wrote:", outpath )

## Thanks, ChatGPT
def table_from_URL( url ):
    # Fetch HTML content from the URL
    print( "Fetching:", url )
    response = requests.get(url)
    if response.status_code != 200:
        raise KeyError( f"URL not found: <{url}>. Status code: {response.status_code}." )
        return None
    
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text contents of the rows
    table_data = []
    for row in soup.select('.table-condensed > tbody > tr'):
        row_data = [ list(cell.stripped_strings)[0] for cell in row.find_all('td', recursive = False) ]
        table_data.append( row_data )
    
    return table_data

if __name__ == '__main__': main()
