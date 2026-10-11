import html
import streamlit as st
from rsvp import extract_players
from teams import make_teams

st.set_page_config(page_title="Touch Grass FC", page_icon="⚽")

st.markdown(
    """
    <style>
    .banner {
        background: linear-gradient(135deg, #0B6623, #2FA84F);
        color: white;
        padding: 1.4rem 1.6rem;
        border-radius: 14px;
        margin-bottom: 1.2rem;
    }
    .banner h1 { color: white; margin: 0; font-size: 2rem; }
    .banner p { margin: 0.3rem 0 0 0; opacity: 0.9; }
    .team-card {
        background: white;
        border-left: 8px solid var(--kit);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin-bottom: 0.8rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.12);
    }
    .team-card h3 { margin: 0 0 0.4rem 0; color: var(--kit); }
    .team-card ul { margin: 0; padding-left: 1.2rem; }
    </style>
    <div class="banner">
        <h1>⚽ Touch Grass FC</h1>
        <p>Paste the group chat. Get fair teams. Go play outside.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

KIT_COLORS = ["#C62828", "#1565C0", "#F57F17", "#6A1B9A", "#00838F", "#2E7D32"]


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


st.caption("The AI runs on this computer, so nothing is uploaded.")

chat = st.text_area("Group chat", height=250)
ratings_text = st.text_area(
    "Player ratings, optional (one per line, 1 to 5, like  Tobi: 4)", height=120
)
num_teams = st.slider("Number of teams", min_value=2, max_value=6, value=2)

if st.button("Make teams"):
    if not chat.strip():
        st.warning("Paste the chat first.")
    else:
        with st.spinner("Reading the chat..."):
            players = extract_players(chat)

        ratings = parse_ratings(ratings_text)
        playing = [p["name"] for p in players if p["status"] == "in"]
        maybes = [p["name"] for p in players if p["status"] == "maybe"]

        if not playing:
            st.warning("Nobody is marked as in.")
        else:
            teams_wanted = min(num_teams, len(playing))
            if teams_wanted < num_teams:
                st.info(
                    f"Only {len(playing)} players are in, so making {teams_wanted} teams."
                )

            teams, scores = make_teams(playing, ratings, teams_wanted)

            cols = st.columns(2)
            for i, team in enumerate(teams):
                items = "".join(f"<li>{html.escape(n)}</li>" for n in team)
                card = (
                    f'<div class="team-card" style="--kit:{KIT_COLORS[i]}">'
                    f"<h3>Team {chr(65 + i)} · strength {scores[i]}</h3>"
                    f"<ul>{items}</ul></div>"
                )
                with cols[i % 2]:
                    st.markdown(card, unsafe_allow_html=True)

            if maybes:
                st.info("Maybe (reserves): " + ", ".join(maybes))