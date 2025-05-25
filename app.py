# --- Step 1: Import Libraries ---
import pandas as pd
import streamlit as st
import plotly.express as px
import os
from typing import Optional, Any

# --- Constants ---
DATA_FILE = 'FAOSTAT_data_en_4-12-2025.csv'
ITEM_UNDERNOURISHMENT = 'Prevalence of undernourishment (percent) (3-year average)'
DEFAULT_COUNTRIES = [
    'Indonesia', 'Viet Nam', 'Philippines', 'India', 'Egypt',
    'Brazil', 'Nigeria', 'Japan', 'Republic of Korea', 'China'
]
REGION_MAP = {
    'Indonesia': 'Southeast Asia', 'Malaysia': 'Southeast Asia', 'Thailand': 'Southeast Asia',
    'Vietnam': 'Southeast Asia', 'Viet Nam': 'Southeast Asia', 'Philippines': 'Southeast Asia',
    'China': 'East Asia', 'Japan': 'East Asia', 'South Korea': 'East Asia', 'Republic of Korea': 'East Asia',
    'Nigeria': 'Sub-Saharan Africa', 'Kenya': 'Sub-Saharan Africa', 'Egypt': 'MENA',
    'Brazil': 'Latin America', 'India': 'South Asia'
}

# --- Data Utilities ---
def get_middle_year(year_str: Any) -> Optional[int]:
    """Convert a year or year range string to its middle year as int."""
    try:
        if isinstance(year_str, str) and '-' in year_str:
            start_year, end_year = map(int, year_str.split('-'))
            return start_year + ((end_year - start_year) // 2)
        elif isinstance(year_str, str):
            return int(year_str.strip())
        else:
            return int(year_str)
    except Exception:
        return None

def clean_value(value: Any) -> Optional[float]:
    """Clean value field, handling <, >, and whitespace."""
    try:
        if isinstance(value, str):
            if value.startswith('<') or value.startswith('>'):
                return float(value[1:].strip())
            return float(value.strip())
        return float(value)
    except Exception:
        return None

def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """Load and clean the FAO data."""
    if not os.path.exists(filepath):
        st.error(f"Data file '{filepath}' not found. Please upload it to the app directory.")
        st.stop()
    data = pd.read_csv(filepath)
    data['Year'] = data['Year'].apply(get_middle_year)
    data['Value'] = data['Value'].apply(clean_value)
    data['Region'] = data['Area'].map(REGION_MAP)
    return data

# --- UI Sections ---
def show_keywords():
    st.markdown(
        """
        <div style='margin-bottom: 20px;'>
            <span style='background-color:#ffe066; color:#333; padding:6px 14px; border-radius:18px; margin-right:10px; font-weight:bold;'>Food Security</span>
            <span style='background-color:#b2f2ff; color:#333; padding:6px 14px; border-radius:18px; margin-right:10px; font-weight:bold;'>Agrarian Reform</span>
            <span style='background-color:#ffd6e0; color:#333; padding:6px 14px; border-radius:18px; font-weight:bold;'>Fertilizer Subsidy</span>
        </div>
        """,
        unsafe_allow_html=True
    )

def show_country_filter(data: pd.DataFrame) -> list:
    st.sidebar.markdown("""
    <style>
    /* Make the multiselect box taller and wider */
    section[data-testid="stSidebar"] .stMultiSelect > div {
        min-height: 300px;
        max-height: 400px;
        width: 100% !important;
    }
    /* Make the options easier to read */
    section[data-testid="stSidebar"] .stMultiSelect .css-1wa3eu0-placeholder {
        font-size: 1.1em;
    }
    </style>
    """, unsafe_allow_html=True)
    st.sidebar.markdown("**Select Countries to Compare:**")
    st.sidebar.caption("Tip: Start typing or scroll to find countries. You can select multiple.")
    selected = st.sidebar.multiselect(
        "",
        options=sorted(data['Area'].unique()),
        default=DEFAULT_COUNTRIES,
        key="country_multiselect"
    )
    # Add button below the filter
    st.sidebar.markdown("""
    <div style='margin-top: 20px; text-align: center;'>
        <a href="https://rudyprasetiya.com" target="_blank">
            <button style="padding:10px 24px; font-size:1em; background:#2b6cb0; color:white; border:none; border-radius:6px; cursor:pointer;">Go to Main Page<br><span style='font-size:0.9em;'>rudyprasetiya.com</span></button>
        </a>
    </div>
    """, unsafe_allow_html=True)
    return selected

def plot_country_trends(filtered: pd.DataFrame):
    fig = px.line(
        filtered,
        x="Year", y="Value", color="Area",
        labels={"Value": "Prevalence of Undernourishment (%)"},
        title="Trends in Undernourishment Across Selected Countries",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Safe  # colorblind-friendly
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    fig.update_layout(
        height=600,
        template="plotly_white",
        font=dict(size=15),
        legend=dict(font=dict(size=13)),
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)
    # Add narration in an expander below the plot
    with st.expander("What Does High Undernourishment Really Mean, and Why Does It Matter?"):
        st.markdown(
            """
            <div id='undernourishment-summary' style='font-size:0.95em; color:#666;'>
            <b>What Does High Undernourishment Really Mean, and Why Does It Matter?</b><br>
            Undernourishment means that people do not get enough food to meet their minimum daily energy (calorie) requirements. In simple terms, it's a measure of chronic hunger—when people regularly go to bed hungry or do not have enough nutritious food to lead healthy, active lives.<br><br>
            <b>What the Chart Shows</b><br>
            The chart displays the "Prevalence of Undernourishment (%)" for several countries over time. A high percentage means a large share of the population is not getting enough to eat. For example, if a country's line is at 15%, that means 15 out of every 100 people are undernourished.<br><br>
            <b>Why High Undernourishment Matters</b><br>
            <u>Human Health and Development</u><br>
            - Chronic undernourishment leads to stunted growth in children, weak immune systems, and higher risk of disease.<br>
            - It affects brain development, making it harder for children to learn and succeed in school.<br>
            - Adults who are undernourished are less productive and more likely to suffer from illness.<br>
            <u>Economic Impact</u><br>
            - A hungry population cannot work or learn effectively, which slows down economic growth.<br>
            - Countries with high undernourishment often struggle to break out of poverty because their people are not healthy enough to be productive.<br>
            <u>Social Stability</u><br>
            - Food insecurity can lead to social unrest, migration, and even conflict, as people compete for scarce resources.<br>
            - It can undermine trust in governments and institutions if people feel their basic needs are not being met.<br>
            <u>Intergenerational Effects</u><br>
            - Undernourished mothers are more likely to have underweight babies, continuing the cycle of hunger and poverty.<br><br>
            <b>Why Should We Care?</b><br>
            <b>Moral Responsibility:</b> In a world with enough food for everyone, chronic hunger is a tragedy that can and should be solved.<br>
            <b>Global Goals:</b> Reducing undernourishment is a key part of the United Nations' Sustainable Development Goals (SDG 2: Zero Hunger).<br>
            <b>Shared Prosperity:</b> Well-nourished populations are healthier, more innovative, and better able to contribute to society.<br><br>
            <b>In Summary</b><br>
            High undernourishment is not just a statistic—it represents millions of real people whose lives and futures are at risk. Tackling undernourishment is essential for building healthier, more prosperous, and more stable societies.
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <button id="tts-btn" style="margin-top:10px; padding:6px 16px; font-size:1em; background:#f0f0f0; border-radius:6px; border:1px solid #ccc; cursor:pointer;">🔊 Read Aloud</button>
            <script>
            const btn = window.parent.document.getElementById('tts-btn');
            if (btn) {
                btn.onclick = function() {
                    const text = window.parent.document.getElementById('undernourishment-summary').innerText;
                    if ('speechSynthesis' in window.parent) {
                        const utter = new window.parent.SpeechSynthesisUtterance(text);
                        utter.rate = 1.0;
                        utter.pitch = 1.0;
                        window.parent.speechSynthesis.speak(utter);
                    } else {
                        alert('Sorry, your browser does not support text-to-speech.');
                    }
                }
            }
            </script>
            """,
            unsafe_allow_html=True
        )

def plot_regional_trends(filtered: pd.DataFrame):
    st.subheader("Regional Trends")
    region_avg = filtered.dropna(subset=['Region']).groupby(['Region', 'Year'])['Value'].mean().reset_index()
    fig2 = px.line(
        region_avg,
        x='Year', y='Value', color='Region',
        title="Regional Average of Undernourishment"
    )
    st.plotly_chart(fig2)

def show_narrative():
    with st.expander("Narrative Analysis"):
        st.markdown(
            """
            - **Indonesia** shows consistent improvement in PoU due to expanding social protection and food policy.
            - **Brazil** and **Egypt** reversed their progress post-2015, likely due to policy rollbacks and macro shocks.
            - **China**, **Japan**, and **Korea** maintain very low PoU due to strong institutions and agrarian reform legacy.
            - **Nigeria** and **India** show volatility, highlighting gaps in governance and food system resilience.

            This supports the thesis that **institutional quality** and **policy consistency** are stronger predictors of hunger elimination than GDP growth alone.
            """
        )

def show_key_insights():
    with st.expander("Key Insights from International Organizations and Research"):
        st.markdown(
            """
            ### International Organizations' Perspectives
            #### World Bank
            - Food security is increasingly linked to climate resilience and sustainable agriculture
            - Indonesia's progress in reducing undernourishment is attributed to its comprehensive social protection system (JPS)
            - Key challenge: Balancing agricultural productivity with environmental sustainability
            #### United Nations
            - SDG 2 (Zero Hunger) progress is uneven across regions
            - Indonesia's success in reducing stunting through multi-sectoral approach
            - Emphasis on food system transformation for long-term sustainability
            #### Asian Development Bank
            - Southeast Asia's food security depends on regional cooperation
            - Indonesia's role as a regional food security leader
            - Investment in agricultural infrastructure is crucial for long-term food security
            ### Key Research Findings
            1. **"Why Nations Fail" (Acemoglu & Robinson, 2012)**
               - Indonesia's institutional reforms post-1998 have been crucial for food security
               - Inclusive economic institutions correlate with better food security outcomes
               - The role of political stability in maintaining food security policies
            2. **"Guns, Germs, and Steel" (Diamond, 1997)**
               - Geographic advantages in Indonesia's agricultural potential
               - Historical patterns of food production and distribution
               - Impact of natural resources on food security
            3. **"The Bottom Billion" (Collier, 2007)**
               - Indonesia's success in avoiding the "poverty trap"
               - Importance of governance in food security
               - Role of international trade in food security
            ### Indonesia-Specific Context
            #### Historical Context
            - From food importer to self-sufficiency in key commodities
            - Success of rice self-sufficiency programs
            - Challenges in maintaining food security during economic transitions
            #### Current Challenges
            - Urban-rural divide in food access
            - Climate change impact on agricultural productivity
            - Need for modern agricultural practices
            #### Future Outlook
            - Digital agriculture opportunities
            - Sustainable food systems development
            - Regional food security leadership role
            ### Interesting Facts from Literature
            #### From "Why Nations Fail"
            - Countries with extractive institutions tend to have higher food insecurity
            - Political stability is crucial for long-term food security
            - The role of property rights in agricultural development
            #### From "Guns, Germs, and Steel"
            - Indonesia's unique position in the "Fertile Crescent" of Southeast Asia
            - Historical patterns of agricultural innovation
            - Geographic advantages in food production
            #### From "The Bottom Billion"
            - Indonesia's success in avoiding common development traps
            - The importance of governance in food security
            - Role of international trade in food security
            """
        )

def show_fertilizer_analysis():
    with st.expander("Fertilizer Subsidy Analysis: Indonesia and Lessons from East Asia"):
        st.markdown(
            """
            ### Indonesia's Fertilizer Subsidy Policy
            - Indonesia has long used fertilizer subsidies to support smallholder farmers and boost rice production.
            - While subsidies have contributed to food self-sufficiency, they have also led to inefficiencies, overuse, and environmental concerns.
            - Recent reforms aim to better target subsidies and promote sustainable practices.
            ### Lessons from South Korea and Japan
            - **South Korea**: Transitioned from broad subsidies to targeted support, investing in rural infrastructure, education, and technology adoption. This shift improved productivity and environmental outcomes.
            - **Japan**: Focused on quality improvement, farmer cooperatives, and integrated rural development, rather than just input subsidies. Emphasis on innovation and value-added agriculture.
            ### What Indonesia Can Learn
            - Move from blanket subsidies to targeted, data-driven support for the most vulnerable farmers.
            - Invest in agricultural extension, digital tools, and farmer education to improve fertilizer efficiency.
            - Encourage crop diversification and sustainable practices to reduce environmental impact.
            - Foster farmer organizations and cooperatives for better bargaining power and knowledge sharing.
            ### Other Thriving Agriculture Countries
            - Countries like the Netherlands and Australia have succeeded through advanced technology adoption, efficient resource use, and strong research-extension linkages.
            - The Netherlands is the world's second-largest agricultural exporter, with over $100 billion in annual exports, despite its small land area.
            - Australia leads in water-efficient farming and precision agriculture, with wheat yields averaging over 2.0 tons/ha and significant investment in agri-tech R&D.
            - Both countries invest over 3% of their agricultural GDP in research and innovation, compared to less than 1% in many developing countries.
            - **Policy focus:** Innovation, sustainability, and market access rather than just subsidies.
            
            **In summary:** Indonesia's fertilizer subsidy reform should be part of a broader strategy for sustainable, resilient, and competitive agriculture, learning from both regional neighbors and global leaders.
            """
        )
    # Place buttons and author credit below the expander
    st.markdown("""
    <div style='margin-top: 32px; display: flex; gap: 24px; flex-wrap: wrap;'>
        <a href="https://rudyprasetiya.com" target="_blank" style="text-decoration: none;">
            <button style="padding:18px 32px; font-size:1.2em; background:#2b6cb0; color:white; border:none; border-radius:12px; cursor:pointer; min-width:200px; margin-bottom:10px;">🌐 Go to Main Page<br><span style='font-size:0.95em;'>rudyprasetiya.com</span></button>
        </a>
        <a href="https://www.linkedin.com/in/rudyprasetiya/" target="_blank" style="text-decoration: none;">
            <button style="padding:18px 32px; font-size:1.2em; background:#0077b5; color:white; border:none; border-radius:12px; cursor:pointer; min-width:200px; margin-bottom:10px;">🔗 Connect on LinkedIn<br><span style='font-size:0.95em;'>linkedin.com/in/rudyprasetiya</span></button>
        </a>
    </div>
    <div style='margin-top: 10px; font-size:1em; color:#888;'>Made by Rudy Prasetiya</div>
    """, unsafe_allow_html=True)

def show_descriptive_stats(filtered: pd.DataFrame):
    with st.sidebar.expander("Descriptive Statistics & Best Practices"):
        st.markdown("**Descriptive Statistics (Current Selection):**")
        stats = filtered['Value'].describe().rename({
            'count': 'Count', 'mean': 'Mean', 'std': 'Std Dev', 'min': 'Min', '25%': 'Q1', '50%': 'Median', '75%': 'Q3', 'max': 'Max'
        })
        st.table(stats)
        st.markdown("""
        **Best Practices for Data Analysis:**
        - Always check for missing or outlier values before drawing conclusions.
        - Compare both central tendency (mean, median) and spread (std, min, max).
        - Visualize trends over time and across groups (countries, regions).
        - Consider context: policy changes, economic shocks, and data limitations.
        - Use both descriptive and inferential statistics for robust insights.
        - Document your analysis steps for transparency and reproducibility.
        """)

# --- Main App ---
def main():
    st.title("Global Undernourishment Explorer")
    st.markdown(
        """
        This app presents a comparative exploration of **Prevalence of Undernourishment (PoU)** across selected countries,
        with focus on institutional, economic, and political dynamics.
        made by Rudy Prasetiya (rudyhendra@iuj.ac.jp) a.k.a asfalanoij | 2025-05-24
        Data source: https://www.fao.org/faostat/en/#data/FS
        """
    )
    data = load_and_clean_data(DATA_FILE)
    show_keywords()
    countries = show_country_filter(data)
    filtered = data[(data['Area'].isin(countries)) & (data['Item'] == ITEM_UNDERNOURISHMENT)]
    show_descriptive_stats(filtered)
    plot_country_trends(filtered)
    plot_regional_trends(filtered)
    show_narrative()
    show_key_insights()
    show_fertilizer_analysis()

if __name__ == "__main__":
    main()

# --- Step 7: File Management Notes (for Jupyter/Streamlit) ---
# - In Jupyter, use `Upload` button or `os.listdir()` to verify your file location
# - In terminal, make sure file path matches (e.g. `data = pd.read_csv('data.csv')`)
# - In Streamlit Cloud or HuggingFace, upload your dataset via app settings or include in repo
