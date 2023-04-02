# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 14:30:18 2023

@author: Abhi
"""

#import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

#define function to parse url and make soup
def make_soup(url):
    try:
        source = requests.get(url)
        #check if url is correct or not
        source.raise_for_status()
        return BeautifulSoup(source.text, 'html.parser')
        
    except Exception as e:
        print(e)

url = 'https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament'
#make soup
soup = make_soup(url)
#find the result table and fetch all rows of the result table
matches = soup.find('tbody').find_all('tr', {'class':'data1'})

#get scorecard ID and match summary page's url
url_list = []

for match in matches:
  match_record = match.find_all('td')
  scorecard = match_record[6].find('a').text
  url = "https://www.espncricinfo.com" + match_record[6].find('a')['href']
  #store both as a tuple and make list of tuples
  url_list.append((scorecard,url))
  
#get batting details of both teams  
t20_wc_batting_summary = []

for scorecard,url in url_list:
    soup = make_soup(url)
    
    #get detail of team which bats first
    team = soup.select('div > span > span > span')[-4:-2]
    team1 = team[0].text.replace(' Innings','')
    team2 = team[1].text.replace(' Innings','')

    #get the batting summary table for both teams
    # find all the table elements that have a class ci-scorecard-table and are children of a div element
    # '>' symbol is used to select only the direct children of the div element
    batting_tables = soup.select('div > table.ci-scorecard-table')
 
    # use try except block to avoid null tables, continue to next loop if Exception
    try:
        # Find all the rows in the first inning scorecard table
        first_inning_rows = batting_tables[0].find_all('tr')
    except:
        continue
    
    

    # Filter out any rows that do not have at least 8 columns
    first_inning_rows = [row for row in first_inning_rows if len(row.find_all('td')) >= 8]
    
    #collect and store data 
    for index, element in enumerate(first_inning_rows):
        tds = element.find_all('td')
        t20_wc_batting_summary.append({
                    "teamInnings": team1,
                    "scorecard": scorecard,
                    "battingPos": index+1,
                    "batsmanName": tds[0].find('a').find('span').text.replace(' ', ''),
                    "dismissal": tds[1].text,
                    "runs": tds[2].find('strong').text,
                    "balls": tds[3].text,
                    "4s": tds[5].text,
                    "6s": tds[6].text,
                    "SR": tds[7].text })
        
    #second inning scorecard
    second_inning_rows = batting_tables[1].find_all('tr')
    
    second_inning_rows = [row for row in second_inning_rows if len(row.find_all('td')) >= 8]
    
    for index, element in enumerate(second_inning_rows):
        tds = element.find_all('td')
        t20_wc_batting_summary.append({
            "teamInnings": team2,
            "scorecard": scorecard,
            "battingPos": index+1,
            "batsmanName": tds[0].find('a').find('span').text.replace(' ', ''),
            "dismissal": tds[1].text,
            "runs": tds[2].find('strong').text,
            "balls": tds[3].text,
            "4s": tds[5].text,
            "6s": tds[6].text,
            "SR": tds[7].text
        })


t20_wc_batting_summary_df = pd.DataFrame(t20_wc_batting_summary)
print(t20_wc_batting_summary_df)

t20_wc_batting_summary_df.to_csv('t20_wc_batting_summary.csv', index = False)