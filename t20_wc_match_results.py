# -*- coding: utf-8 -*-
"""
Created on Sat Apr  1 14:19:25 2023

@author: Abhi
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

source = requests.get('https://stats.espncricinfo.com/ci/engine/records/team/match_results.html?id=14450;type=tournament')
#check if url is correct or not
source.raise_for_status()

soup = BeautifulSoup(source.text, 'html.parser')

matches = soup.find('tbody').find_all('tr', {'class':'data1'})

matchSummary_list = []

for match in matches:
  summary_dict ={}
  match_record = match.find_all('td')
  summary_dict['Team 1'] = match_record[0].find('a').text
  summary_dict['team2'] = match_record[1].find('a').text
  summary_dict['winner'] = match_record[2].find('a').text if match_record[2].find('a') else match_record[2].text
  summary_dict['margin'] = match_record[3].text
  summary_dict['ground'] = match_record[4].find('a').text
  summary_dict['matchDate'] = match_record[5].text
  summary_dict['scorecard'] = match_record[6].find('a').text
  

  matchSummary_list.append(summary_dict)
  
t20_wc_match_results_df = pd.DataFrame(matchSummary_list)

t20_wc_match_results_df.to_csv('t20_wc_match_results.csv', index =False)