import streamlit as st
from bs4 import BeautifulSoup
import requests
import re

st.title('Imdb Parental Guide')

titolo = st.text_input("Search for movie name", placeholder="f.e. Titanic")

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
url = 'https://www.imdb.com/find/?q=' + titolo + '%20' + '&ref_=nv_sr_sm'

if st.button("Search"):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    if soup:
        st.write("Search results:")
        link = soup.find('a', class_='ipc-metadata-list-summary-item__t', href=lambda href: href and '/title/' in href)
        image = soup.find("img", class_="ipc-image")
        image_src = image['src']
        st.image(image_src)
        href = link.get('href')
        title = link.get_text()
        title_id = href.split('/title/')[1].split('/')[0]
        st.write(title_id)

        info = {
            "title": title,
            "image": image_src
        }

        response = requests.get(f"https://www.imdb.com/title/{title_id}", headers=headers)
        if response.status_code != 200:
            st.write("Information not available")
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            if soup:
                items = soup.find_all("li", class_="ipc-inline-list__item")

        for i in range(4, 11):
            info["year"] = items[4].get_text()
            info["rating"] = items[5].get_text()
            info["duration"] = items[6].get_text()
            info["director"] = items[7].get_text()
            info["writer"] = items[8].get_text()
            info["with"] = items[9].get_text()
            info["and"] = items[10].get_text()

        """response = requests.get(f"https://www.imdb.com/title/{title_id}/parentalguide", headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        categories = ["nudity", "violence", "profanity", "frightening"]

        for category in categories:
            content = soup.find("section", id=f"advisory-{category}")
            content_row = content.find_all("li", class_='ipl-zebra-list__item')
            lista = []
            for each in content_row:
                each = each.get_text()
                cleaned_text = re.sub(r'\bEdit\b|\s*\n+\s*', '', each)
                frase = cleaned_text.split('\n')
                lista += frase
            info[f"{category.upper()}"] = lista

"""
        col1, col2 = st.columns([1,7])
        with col1:
            st.text(" ")
            st.text(" ")
            st.image(info["image"], use_column_width=True)
        with col2:
            st.title(info["title"])
            st.text(f"{info['year']} | {info['rating']} | {info['duration']}")
            st.text(f"Director: {info['director']}\n"
                    f"Writer: {info['writer']}\n"
                    f"with: {info['with']}\n"
                    f"and: {info['and']}")
            
            """st.subheader("Nudity")
            st.write(info['NUDITY'])
            st.subheader("Violence")
            st.write(info['VIOLENCE'])
            st.subheader("Profanity")
            st.write(info['PROFANITY'])
            st.subheader("Frightening")
            st.write(info['FRIGHTENING'])"""






