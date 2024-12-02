import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'matches.csv'
matches_df = pd.read_csv(file_path)

# Set the page title and layout
st.set_page_config(page_title="Cricket Match Analysis", layout="wide")

# Standardize the team name to "Rising Pune Supergiants"
matches_df['team1'] = matches_df['team1'].replace('Rising Pune Supergiant', 'Rising Pune Supergiants')
matches_df['team2'] = matches_df['team2'].replace('Rising Pune Supergiant', 'Rising Pune Supergiants')

# Also, standardize in the 'winner' column if applicable
matches_df['winner'] = matches_df['winner'].replace('Rising Pune Supergiant', 'Rising Pune Supergiants')


# Title of the app
st.title("Cricket Match Performance and Analysis")


# 1. Team Performances (Number of Wins)
def team_performace():

        st.header("Team Performances (Number of Wins)")
        team_performance = matches_df['winner'].value_counts()  # Count the wins per team
        # Create a color palette for the bars
        palette = sns.color_palette("coolwarm", len(team_performance))
        # Create a more compact and aesthetically pleasing plot
        fig, ax = plt.subplots(figsize=(8,5))  # Smaller size for the plot
        sns.barplot(x=team_performance.index, y=team_performance.values, palette=palette, ax=ax)

    # Add title and labels with more style
        ax.set_title('Team Performances (Number of Wins)', fontsize=16, fontweight='bold', color='black')
        ax.set_xlabel('Teams', fontsize=12, fontweight='bold', color='black')
        ax.set_ylabel('Number of Wins', fontsize=12, fontweight='bold', color='black')

    # Add value annotations on top of the bars
        for p in ax.patches:
            ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', fontweight='bold', xytext=(0, 5),
                        textcoords='offset points')

    # Rotate x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

    # Add gridlines to the background
        ax.grid(True, axis='y', linestyle='--', linewidth=0.7, alpha=0.7)
        st.pyplot(fig)

# 2. Toss Decisions Distribution
def toss_decisions():
    col1,col2=st.columns(2)
    with col1:
        st.header("Toss Decisions Distribution")
        toss_decision_counts = matches_df['toss_decision'].value_counts()
        fig, ax = plt.subplots(figsize=(5,4))
        toss_decision_counts.plot(kind='pie', autopct='%1.1f%%', startangle=70, colors=['#66b3ff', '#ffb366'], ax=ax)
        ax.set_title('Distribution of Toss Decisions', fontsize=8)
        ax.set_ylabel('')  # Remove the y-label
        st.pyplot(fig)
    with col2:
            st.header("Toss Winning Impact")
            toss_winner_match_winner = matches_df[matches_df['toss_winner'] == matches_df['winner']]
            impact = ['Won Match', 'Lost Match']
            counts = [len(toss_winner_match_winner), len(matches_df) - len(toss_winner_match_winner)]
            fig, ax = plt.subplots(figsize=(7,6))
            ax.pie(counts, labels=impact, autopct='%1.1f%%', startangle=90, colors=['#88c999', '#f88c9c'])
            ax.set_title('Impact of Toss on Match Results', fontsize=14)
            st.pyplot(fig)


# 3. Win Frequencies Across Cities and Seasons
def win_freq():
    st.header("Win Frequencies Across Cities and Seasons")
    # Group data by season and city
    win_counts_by_city_season = matches_df.groupby(['season', 'city'])['winner'].count().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(win_counts_by_city_season, cmap='YlGnBu', annot=True, fmt='d', linewidths=0.5, ax=ax)
    ax.set_title('Win Frequencies Across Cities and Seasons', fontsize=14)
    ax.set_xlabel('City', fontsize=12)
    ax.set_ylabel('Season', fontsize=12)
    st.pyplot(fig)

def top_players():
    st.header("Top Players of the Match")
    top_players = matches_df['player_of_match'].value_counts().head(10)  # Top 10 players
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=top_players.values, y=top_players.index, palette="viridis", ax=ax)
    ax.set_title('Top 10 Players of the Match', fontsize=16)
    ax.set_xlabel('Number of Awards', fontsize=12)
    ax.set_ylabel('Players', fontsize=12)
    st.pyplot(fig)

def match_outcomes():
    st.header("Match Outcomes by Runs and Wickets")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Matches Won by Runs")
        runs_wins = matches_df[matches_df['win_by_runs'] > 0]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(runs_wins['win_by_runs'], bins=20, kde=True, color='blue', ax=ax)
        ax.set_title('Distribution of Wins by Runs', fontsize=12)
        ax.set_xlabel('Win by Runs', fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        st.pyplot(fig)

    with col2:
        st.subheader("Matches Won by Wickets")
        wickets_wins = matches_df[matches_df['win_by_wickets'] > 0]
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(wickets_wins['win_by_wickets'], bins=10, kde=True, color='green', ax=ax)
        ax.set_title('Distribution of Wins by Wickets', fontsize=12)
        ax.set_xlabel('Win by Wickets', fontsize=10)
        ax.set_ylabel('Frequency', fontsize=10)
        st.pyplot(fig)


st.sidebar.title("Navigation")
option = st.sidebar.selectbox("Choose an analysis option:",
                              ("Team Performances", "Toss Decisions", "Win Frequencies", "Top Players", "Match Outcomes"))

if option == "Team Performances":
    team_performace()

elif option == "Toss Decisions":
    toss_decisions()

elif option == "Win Frequencies":
    win_freq()

elif option == "Top Players":
    top_players()

elif option == "Match Outcomes":
    match_outcomes()


# Footer
st.markdown("---")
