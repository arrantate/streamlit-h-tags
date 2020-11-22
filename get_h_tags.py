import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64

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

# DOWNLOAD LINK
def download_csv(df, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="h_tags.csv">** {text} **</a>'
    st.markdown(href, unsafe_allow_html=True)


# STREAMLIT MAIN PAGE
st.set_page_config(page_title='Get <h> Tags')
st.title("Get <h> Tags")
st.subheader("Enter a URL to get started.")
url = st.text_input('URL to check')

if url:
    soup = get_soup(url)
    tags = get_tag_df(soup)
    download_csv(tags, "Download as .csv")
    # .assign(hack='').set_index('hack') is added to remove the df index from the table display on the streamlit page
    st.table(tags.assign(hack='').set_index('hack'))
    download_csv(tags, "Download as .csv")
    
st.markdown(
    """
    ***
    **Created by [@arrantate](https://twitter.com/arrantate).**   
    You can support me by [buying me a coffee](https://www.buymeacoffee.com/arrantate). (I like coffee)
    """
)



