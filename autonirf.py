## All the categories on <https://www.nirfindia.org/Rankings/2024/Ranking.html>
## pip install requests beautifulsoup4

## Author: Yotam Gingold <yotam@yotamgingold.com>
## License: CC0
## URL: <https://github.com/yig/auto-NIRF>

# from pathlib import Path
import csv
import os

import requests
from bs4 import BeautifulSoup

def main():
    urls = [
        'https://www.nirfindia.org/Rankings/2024/OverallRanking.html',
        'https://www.nirfindia.org/Rankings/2024/UniversityRanking.html',
        'https://www.nirfindia.org/Rankings/2024/CollegeRanking.html',
        'https://www.nirfindia.org/Rankings/2024/ResearchRanking.html',
        'https://www.nirfindia.org/Rankings/2024/EngineeringRanking.html',
        'https://www.nirfindia.org/Rankings/2024/ManagementRanking.html',
        'https://www.nirfindia.org/Rankings/2024/PharmacyRanking.html',
        'https://www.nirfindia.org/Rankings/2024/MedicalRanking.html',
        'https://www.nirfindia.org/Rankings/2024/DentalRanking.html',
        'https://www.nirfindia.org/Rankings/2024/LawRanking.html',
        'https://www.nirfindia.org/Rankings/2024/ArchitectureRanking.html',
        'https://www.nirfindia.org/Rankings/2024/AgricultureRanking.html',
        'https://www.nirfindia.org/Rankings/2024/InnovationRanking.html'
        ]
    
    outpaths = []
    
    for url in urls:
        ## Pathlib isn't great with 
        # category = Path(url).stem.removesuffix('Ranking')
        category = url.removesuffix('Ranking.html').split('/')[-1]
        outpath = category + '.csv'
        outpaths.append( outpath )
        if os.path.exists( outpath ):
            print( "Path exists, skipping:", outpath )
            continue
        table = table_from_URL( url, '#tbl_overall' )
        
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
    
    ## Merge them into "All.csv"
    ## Via: <https://stackoverflow.com/questions/2512386/how-can-i-merge-200-csv-files-in-python>
    if len( outpaths ) == 0: return
    assert "All.csv" not in outpaths
    with open( "All.csv", "wb" ) as allfile:
        ## First file:
        with open( outpaths[0], "rb" ) as f:
            allfile.writelines( f )
        ## Rest:
        for outpath in outpaths[1:]:
            with open( outpath, "rb" ) as f:
                next(f) # skip the header
                allfile.writelines( f )
    
    print( "Wrote:", "All.csv" )

## Thanks, ChatGPT
def table_from_URL( url, prefix = '' ):
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
    for row in soup.select( prefix + '.table-condensed > tbody > tr' ):
        row_data = [ list(cell.stripped_strings)[0] for cell in row.find_all('td', recursive = False) ]
        table_data.append( row_data )
    
    print( f"Fetched {len(table_data)} row{'s' if len(table_data) != 1 else ''}." )
    return table_data

if __name__ == '__main__': main()
