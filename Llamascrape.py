from importlib.resources import path
from re import A
from tokenize import Double
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import ChromeOptions 
import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

#getting rid of the browser window 

def setting_up_chrome():
    options = ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    return driver

def get_path_objects(driver, round):
    url = 'https://llama.airforce/#/bribes/rounds/votium/cvx-crv/{}'.format(round)
    driver.get(url)
    WebDriverWait(driver,30).until(EC.presence_of_element_located((By.ID, 'SvgjsPath9665')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    body = soup.find('body')
    div1 = body.find('div')
    graph = div1.find('div',id='apexchartsvotium-bribe-round')
    path_in_graph = graph.find_all('path') # these are in a list and can be indexed 
    return path_in_graph


# mydict = {"name" : [cvx, fxs, luna], "val" : [20394, 2485792]}
# mydict["joey"] --> 1
def extract_values(path_in_graph, round): 
    allnames = []
    allvals = []
    allrounds = []
    for path_tag in path_in_graph:
        val = float(path_tag.get('val'))
        if val > 0: 
            name = path_tag.parent.get('seriesname')
            allnames.append(name)
            allvals.append(val)
            allrounds.append(round)
    return allnames, allvals, allrounds
            

def build_df(df, allnames, allvals, allrounds):
    tempdf = pd.DataFrame({'names' : allnames, 'values' : allvals, 'rounds' : allrounds})
    df = pd.concat([tempdf, df])
    return df      

df = pd.DataFrame()
driver = setting_up_chrome()
for x in range(1,21):
    path_in_graph = get_path_objects(driver, x)
    allnames, allvals, allrounds = extract_values(path_in_graph, x)
    df = build_df(df, allnames, allvals, allrounds)

driver.quit()

print(df)
