import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64

################################
#####   Helper Functions   #####
#####vvvvvvvvvvvvvvvvvvvvvv#####

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
def get_tag_df(soup, headers_to_include):
    tags_df = []
    for n in headers_to_include:
        tag = f'h{n}'
        tags_df.append(h_tag_text(soup, tag))
    return pd.concat(tags_df, ignore_index=True)

# DOWNLOAD LINK
def download_csv(df, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="h_tags.csv">** {text} **</a>'
    st.markdown(href, unsafe_allow_html=True)

#################################
#####   STREAMLIT CONTENT   #####
#####vvvvvvvvvvvvvvvvvvvvvvv#####
st.set_page_config(page_title='Get <h> Tags')

# SIDEBAR
st.sidebar.subheader("Which <h> tags would you like to include in the table?")
h1 = st.sidebar.checkbox('<h1>', value=True)
h2 = st.sidebar.checkbox('<h2>')
h3 = st.sidebar.checkbox('<h3>')
h4 = st.sidebar.checkbox('<h4>')
h5 = st.sidebar.checkbox('<h5>')
h6 = st.sidebar.checkbox('<h6>')

#   take values from the check boxes and return the selected tag numbers in a list
checked = [(i+1, bool(h)) for i, h in enumerate([h1, h2, h3, h4, h5, h6])]
headers_to_include = [i[0] for i in checked if i[1] == True]


# STREAMLIT MAIN PAGE
st.title("Get <h> Tags")
st.subheader("Enter a URL to get started.")

url = st.text_input('URL to check')
if url:
    if headers_to_include == []:
        st.header("You must include at least one header tag from the sidebar!")
    else:
        soup = get_soup(url)
        tags = get_tag_df(soup, headers_to_include)
        download_csv(tags, "Download as .csv")
        #          " .assign(hack='').set_index('hack') " is added to remove the df index from the table display on the streamlit page
        st.table(tags.assign(hack='').set_index('hack'))
        download_csv(tags, "Download as .csv")
    
# FOOTER
st.markdown(
    """
    ***
    **Created by [@arrantate](https://twitter.com/arrantate).**   
    You can support me by [buying me a coffee](https://www.buymeacoffee.com/arrantate). (I like coffee)
    """
)