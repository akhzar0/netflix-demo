import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Movie Data Analysis",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------
# TITLE
# ---------------------------------------

st.title("🎬 Movie Data Analysis Dashboard")

st.write(
    "An interactive data analysis project based on movie data "
    "using Python, Pandas and Streamlit."
)

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "mymoviedb.csv",
        lineterminator="\n"
    )

    # Convert release date
    df["Release_Date"] = pd.to_datetime(
        df["Release_Date"]
    )

    df["Release_Date"] = df["Release_Date"].dt.year

    # Drop unnecessary columns
    cols = [
        "Overview",
        "Original_Language",
        "Poster_Url"
    ]

    df.drop(
        cols,
        axis=1,
        inplace=True
    )

    # Categorize Vote Average

    labels = [
        "not_Popular",
        "below_avg",
        "average",
        "popular"
    ]

    edges = [
        df["Vote_Average"].describe()["min"],
        df["Vote_Average"].describe()["25%"],
        df["Vote_Average"].describe()["50%"],
        df["Vote_Average"].describe()["75%"],
        df["Vote_Average"].describe()["max"]
    ]

    df["Vote_Average"] = pd.cut(
        df["Vote_Average"],
        edges,
        labels=labels,
        duplicates="drop"
    )

    # Remove missing values

    df.dropna(inplace=True)

    # Split genres

    df["Genre"] = df["Genre"].str.split(", ")

    df = df.explode(
        "Genre"
    ).reset_index(drop=True)

    return df


df = load_data()

# ---------------------------------------
# SIDEBAR FILTER
# ---------------------------------------

st.sidebar.header("🔎 Filters")

genres = sorted(
    df["Genre"].unique()
)

selected_genre = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + genres
)

years = sorted(
    df["Release_Date"].unique(),
    reverse=True
)

selected_year = st.sidebar.selectbox(
    "Select Year",
    ["All"] + [int(year) for year in years]
)

# ---------------------------------------
# APPLY FILTER
# ---------------------------------------

filtered_df = df.copy()

if selected_genre != "All":

    filtered_df = filtered_df[
        filtered_df["Genre"] == selected_genre
    ]

if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["Release_Date"] == selected_year
    ]

# ---------------------------------------
# METRICS
# ---------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Total Movies",
        filtered_df["Title"].nunique()
    )

with col2:

    st.metric(
        "Genres",
        filtered_df["Genre"].nunique()
    )

with col3:

    st.metric(
        "Average Popularity",
        round(
            filtered_df["Popularity"].mean(),
            2
        )
    )

with col4:

    st.metric(
        "Total Votes",
        int(
            filtered_df["Vote_Count"].sum()
        )
    )

# ---------------------------------------
# MOVIE DATA
# ---------------------------------------

st.subheader("📊 Movie Dataset")

st.dataframe(
    filtered_df[
        [
            "Release_Date",
            "Title",
            "Popularity",
            "Vote_Count",
            "Vote_Average",
            "Genre"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------
# GENRE DISTRIBUTION
# ---------------------------------------

st.subheader("🎭 Genre Distribution")

genre_counts = (
    filtered_df["Genre"]
    .value_counts()
    .sort_values(ascending=True)
)

fig, ax = plt.subplots(
    figsize=(10, 6)
)

ax.barh(
    genre_counts.index,
    genre_counts.values
)

ax.set_xlabel("Number of Movies")
ax.set_ylabel("Genre")

ax.set_title(
    "Movie Genre Distribution"
)

st.pyplot(fig)

# ---------------------------------------
# VOTE AVERAGE
# ---------------------------------------

st.subheader("⭐ Vote Average Distribution")

vote_counts = (
    filtered_df["Vote_Average"]
    .value_counts()
)

fig2, ax2 = plt.subplots(
    figsize=(8, 5)
)

ax2.bar(
    vote_counts.index.astype(str),
    vote_counts.values
)

ax2.set_xlabel("Vote Category")
ax2.set_ylabel("Number of Movies")

ax2.set_title(
    "Vote Average Distribution"
)

st.pyplot(fig2)

# ---------------------------------------
# MOST POPULAR MOVIE
# ---------------------------------------

st.subheader("🔥 Most Popular Movie")

if not filtered_df.empty:

    max_index = filtered_df[
        "Popularity"
    ].idxmax()

    popular_movie = filtered_df.loc[
        max_index
    ]

    st.success(
        f"🎬 {popular_movie['Title']}"
    )

    st.write(
        f"**Popularity:** "
        f"{popular_movie['Popularity']}"
    )

    st.write(
        f"**Genre:** "
        f"{popular_movie['Genre']}"
    )

# ---------------------------------------
# YEAR ANALYSIS
# ---------------------------------------

st.subheader("📅 Movies Released by Year")

year_counts = (
    filtered_df["Release_Date"]
    .value_counts()
    .sort_index()
)

fig3, ax3 = plt.subplots(
    figsize=(12, 5)
)

ax3.plot(
    year_counts.index,
    year_counts.values
)

ax3.set_xlabel("Release Year")
ax3.set_ylabel("Number of Movies")

ax3.set_title(
    "Movies Released by Year"
)

st.pyplot(fig3)

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.markdown("---")

st.write(
    "Built using Python, Pandas, Matplotlib and Streamlit."
)