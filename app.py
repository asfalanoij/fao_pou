# --- Step 1: Import Libraries ---
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Step 2: Load Data File ---
data = pd.read_csv('/Users/asfalanoi/DS/Python/FAO/FAOSTAT_data_en_4-12-2025.csv')


# --- Step 3: Clean 'Year' Field ---
def get_middle_year(year_str):
    try:
        if isinstance(year_str, str) and '-' in year_str:
            start_year, end_year = map(int, year_str.split('-'))
            return start_year + ((end_year - start_year) // 2)
        elif isinstance(year_str, str):
            return int(year_str.strip())
        else:
            return int(year_str)
    except:
        return None

data['Year'] = data['Year'].apply(get_middle_year)

# --- Step 4: Clean 'Value' Field ---
def clean_value(value):
    if isinstance(value, str):
        if value.startswith('<') or value.startswith('>'):
            return float(value[1:].strip())
        return float(value.strip())
    return value

data['Value'] = data['Value'].apply(clean_value)

# --- Step 5: Region Mapping ---
region_map = {
    'Indonesia': 'Southeast Asia', 'Malaysia': 'Southeast Asia', 'Thailand': 'Southeast Asia',
    'Vietnam': 'Southeast Asia', 'Viet Nam': 'Southeast Asia', 'Philippines': 'Southeast Asia',
    'China': 'East Asia', 'Japan': 'East Asia', 'South Korea': 'East Asia', 'Republic of Korea': 'East Asia',
    'Nigeria': 'Sub-Saharan Africa', 'Kenya': 'Sub-Saharan Africa', 'Egypt': 'MENA',
    'Brazil': 'Latin America', 'India': 'South Asia'
}
data['Region'] = data['Area'].map(region_map)

# --- Step 6: Streamlit UI ---
st.title("Global Undernourishment Explorer")
st.markdown("""
This app presents a comparative exploration of **Prevalence of Undernourishment (PoU)** across selected countries,
with focus on institutional, economic, and political dynamics.
""")

# Sidebar filter
countries = st.sidebar.multiselect(
    "Select Countries to Compare:",
    options=sorted(data['Area'].unique()),
    default=['Indonesia', 'Viet Nam', 'Philippines', 'India', 'Egypt', 'Brazil', 'Nigeria', 'Japan', 'Republic of Korea', 'China']
)

# Filter data
item = 'Prevalence of undernourishment (percent) (3-year average)'
filtered = data[(data['Area'].isin(countries)) & (data['Item'] == item)]

# Plot country trends
fig = px.line(
    filtered,
    x="Year", y="Value", color="Area",
    labels={"Value": "Prevalence of Undernourishment (%)"},
    title="Trends in Undernourishment Across Selected Countries",
    markers=True
)
fig.update_layout(height=600)
st.plotly_chart(fig)

# Regional average trends
st.subheader("Regional Trends")
region_avg = filtered.dropna(subset=['Region']).groupby(['Region', 'Year'])['Value'].mean().reset_index()
fig2 = px.line(
    region_avg,
    x='Year', y='Value', color='Region',
    title="Regional Average of Undernourishment"
)
st.plotly_chart(fig2)

# Narrative section
with st.expander("Narrative Analysis"):
    st.markdown("""
    - **Indonesia** shows consistent improvement in PoU due to expanding social protection and food policy.
    - **Brazil** and **Egypt** reversed their progress post-2015, likely due to policy rollbacks and macro shocks.
    - **China**, **Japan**, and **Korea** maintain very low PoU due to strong institutions and agrarian reform legacy.
    - **Nigeria** and **India** show volatility, highlighting gaps in governance and food system resilience.

    This supports the thesis that **institutional quality** and **policy consistency** are stronger predictors of hunger elimination than GDP growth alone.
    """)

# --- Step 7: File Management Notes (for Jupyter/Streamlit) ---
# - In Jupyter, use `Upload` button or `os.listdir()` to verify your file location
# - In terminal, make sure file path matches (e.g. `data = pd.read_csv('data.csv')`)
# - In Streamlit Cloud or HuggingFace, upload your dataset via app settings or include in repo
