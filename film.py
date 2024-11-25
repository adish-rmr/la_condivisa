import streamlit as st
import datetime as dt
from pymongo import MongoClient

st.title("Film - La Condivisa")

client = MongoClient("mongodb+srv://user:1234@cluster0.mxnrotu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["film_database"]
collection_polls = db["polls"]
collection_votes = db["movies"]

with st.form("create_poll"):
    st.write("Crea un nuovo poll")
    start_date = dt.datetime.today()
    end_date = dt.datetime.today() + dt.timedelta(days=7)
    date_str = start_date.strftime("%d_%m_%y")
    end_date_str = end_date.strftime("%d_%m_%y")
    poll = {
        "date": date_str + " - " + end_date_str,
        "start_date": start_date,
        "end_date": end_date,
        "movies": [],
        "votes": []
    }
    submitted = st.form_submit_button("Submit")
    if submitted:
        today = dt.datetime.today()
        for poll in collection_polls.find():
            if today >= poll["start_date"] and today <= poll["end_date"]:
                st.write(f"Poll già esistente per la settimana {poll['date']}")
            else:
                poll_id = collection_polls.insert_one(poll).inserted_id
                st.write(f"Poll created from {date_str} to {end_date_str} with id {poll_id}")

if st.checkbox("Vota per il film della settimana"):
    today = dt.datetime.today()
    for poll in collection_polls.find():
        if today >= poll["start_date"] and today <= poll["end_date"]:
            st.write(f"Poll {poll['date']} is active")
            with st.form("my_form"):
                your_name = st.text_input("Your name", "Type Here")
                title = st.text_input("Movie title", "Life of Brian")
                st.write("You proposed:", title)

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if poll["movies"] != []:
                        for i in poll["movies"]:
                            if title in i[1] or your_name in i[0]:
                                st.write("Film già proposto o l'utente ha già proposto")
                    else:
                        poll["votes"].append((your_name, title))
                        poll["movies"].append((your_name, title))
                        st.write(f"Voto registrato per {title}")
                        ver = collection_polls.update_one({"_id": poll["_id"]}, {"$set": poll}).inserted_id
                        if ver:
                            st.write("Voto registrato")

st.write("Verifica sondaggio dei film proposti")
for poll in collection_polls.find():
    today = dt.datetime.today()
    if today >= poll["start_date"] and today <= poll["end_date"]:
        st.write(f"Poll {poll['date']} is active")
        risultati = []
        for vote in poll["votes"]:
            risultati.append(vote[1])
        st.write("Risultati del sondaggio")
        set = list(set(risultati))
        for i in set:
            st.write(f"{i} - {risultati.count(i)} voti")


        


    



