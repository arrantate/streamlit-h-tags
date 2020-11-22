import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# GET SOUP
def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content)

# GET DF from <H> TAG
def h_tag_text(soup, h_tag):
    header_list = [tag.text for tag in soup.find_all(h_tag)]
    df = pd.DataFrame(header_list, columns=['Text'])
    df['Tag'] = h_tag
    return df
    
# COMBINE TAG DFs INTO ONE DF
def get_tag_df(soup):
    tags_df = []
    for n in range(1, 7):
        tag = f'h{n}'
        tags_df.append(h_tag_text(soup, tag))
    return pd.concat(tags_df, ignore_index=True)

# MAIN
st.title("Get HTML Tag Text")
st.write("Enter a URL to get started.")
url = st.text_input('URL to check')

if url:
    soup = get_soup(url)
    tags = get_tag_df(soup)
    st.table(tags)
    


