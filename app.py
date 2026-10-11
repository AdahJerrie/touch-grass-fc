import streamlit as st
from rsvp import extract_players
from teams import make_teams


def parse_ratings(text):
    ratings = {}
    for line in text.splitlines():
        if ":" in line:
            name, value = line.split(":", 1)
            try:
                ratings[name.strip()] = int(value.strip())
            except ValueError:
                pass  # ignore lines that aren't "Name: number"
    return ratings


st.title("Touch Grass FC")
st.write("Paste your group chat. The AI runs on this computer, so nothing is uploaded.")

chat = st.text_area("Group chat", height=250)
ratings_text = st.text_area(
    "Player ratings, optional (one per line, 1 to 5, like  Tobi: 4)", height=120
)

if st.button("Make teams"):
    if not chat.strip():
        st.warning("Paste the chat first.")
    else:
        with st.spinner("Reading the chat..."):
            players = extract_players(chat)

        ratings = parse_ratings(ratings_text)
        playing = [p["name"] for p in players if p["status"] == "in"]
        maybes = [p["name"] for p in players if p["status"] == "maybe"]

        team_a, team_b, score_a, score_b = make_teams(playing, ratings)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"Team A (strength {score_a})")
            for name in team_a:
                st.write("•", name)
        with col2:
            st.subheader(f"Team B (strength {score_b})")
            for name in team_b:
                st.write("•", name)

        if maybes:
            st.info("Maybe (reserves): " + ", ".join(maybes))