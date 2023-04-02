# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 16:27:09 2023

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
 
t20_wc_bowling_summary = [] 
 
for scorecard,url in url_list:
    soup = make_soup(url)
    
    #get detail of team which bats first
    team = soup.select('div > span > span > span')[-4:-2]
    team1 = team[0].text.replace(' Innings','')
    team2 = team[1].text.replace(' Innings','')
    
    #get the bowling summary table for both teams
    #get the second child of div (second table contains bowling stats)
    bowling_table = list(soup.select('div  table:nth-of-type(2)'))
    
    try:
        first_inning = bowling_table[0].find_all('tr')
        
    except:
        continue
    
    #selecting only those rows which have 11 columns
    first_inning = [row for row in first_inning if len(row.find_all('td')) == 11]
    

    for element in first_inning:
        tds = element.find_all('td')
        t20_wc_bowling_summary.append({'bowlingTeam': team2,
                                       'scorecard': scorecard,
                                       'bowlerName': tds[0].find('a').find('span').text.replace(' ', ''),
                                       "overs": tds[1].text,
                                       "maiden": tds[2].text,
                                       "runs": tds[3].text,
                                       "wickets": tds[4].text,
                                       "economy": tds[5].text,
                                       '0s':tds[6].text,
                                       "4s":tds[7].text,
                                       "6s": tds[8].text,
                                       "wides":tds[9].text,
                                       "noBalls": tds[10].text })
    
    #second inning
    second_inning = bowling_table[1].find_all('tr')
    
    second_inning = [row for row in second_inning if len(row.find_all('td')) == 11]
    for element in second_inning:
        tds = element.find_all('td')
        t20_wc_bowling_summary.append({'bowlingTeam': team1,
                                       'scorecard': scorecard,
                                       'bowlerName': tds[0].find('a').find('span').text.replace(' ', ''),
                                       "overs": tds[1].text,
                                       "maiden": tds[2].text,
                                       "runs": tds[3].text,
                                       "wickets": tds[4].text,
                                       "economy": tds[5].text,
                                       '0s':tds[6].text,
                                       "4s":tds[7].text,
                                       "6s": tds[8].text,
                                       "wides":tds[9].text,
                                       "noBalls": tds[10].text })
        
t20_wc_bowling_summary_df = pd.DataFrame(t20_wc_bowling_summary)
print(t20_wc_bowling_summary_df)

#t20_wc_bowling_summary_df.to_csv('t20_wc_bowling_summary.csv', index=False)