import streamlit as st
import openpyxl
import pandas as pd
import pydeck as pdk
import numpy as np
import plotly.express as px

#import scipy
import plotly.figure_factory as ff
#import Analysis
import Dashboard
import time
import concurrent.futures
import threading
import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages
#st.set_page_config(layout="centered", page_title="Locata",initial_sidebar_state="collapsed")
# from Locata_Main import Locata_Main



show_pages(
    [
        Page("About.py", "About"),
        Page("Locata_Main.py", "Locata")
        
    ]
)

class About():
    def __init__(self):
        self.condition = False
        self.counter = 0
        self.title = "<div class='title'> 𝕃𝕆ℂ𝔸𝕋𝔸 </div>"
        self.subtitle = "<div class='subtitle'> Decision Model and Simulation for Complex Commercial Site Selection Based on Existing Commercial Environment Analysis</div>"
        self.underlined_title = '________________________________________________________________ '
        self.team = "<div class='team'> \U0001F4D2 MongoUSC :  <code>Zihao Han</code>,  <code>Niantong Zhou</code>,  <code>Yuxuan Shi</code>,  <code>Gordon Su</code> </div>"
        self.mainpage_img= 'image2.png'
        self.y=[]
        st.markdown("""
        <style>
        .title {
          text-align: center;
          font-size: 3.5em;
          margin-bottom: 0em;
          margin-top: 0.01em;
          font-weight: bold;
        }

        .subtitle {
          text-align: center;
          font-size: 1.25em;
          margin-top: 0em;
          margin-bottom: 0em;
          font-style: italic;
        }
        .team {
            text-align: center;
            font-size: 1em;
            margin-top: 0.1em;
        }
        .team code {
            text-align: center;
            background-color: #f1f2f4;
            padding: 0.1em 0.2em;
            border-radius: 0.1em;
            font-size: 0.8em;
        }
        .notation {
            text-align: center; 
            font-size: 1em;
            margin-top: 0.1em;
        }

        .step {
        
            text-align: center; 
            font-size: 2em;
            margin-top: 0.5em;

        }

        <style>
        """, unsafe_allow_html=True)

    def main(self):
        st.markdown(self.title, unsafe_allow_html=True)
        st.markdown(self.subtitle, unsafe_allow_html=True)
        st.write(self.underlined_title)
        st.markdown(self.team, unsafe_allow_html=True)
        st.markdown("<div class='step'> How to use Locata </div>", unsafe_allow_html=True)
        st.image('image2.png', use_column_width=True)
        aboutlocata="""
        About Locata:
                + The recent pandemic has cast a shadow over small businesses,
                dealing a heavy blow to their profits. New businesses will 
                emerge rapidly in their wake, constituting a key force in 
                economic recovery.
                + One of the most salient influencing variables of the success 
                of small enterprises is their location.
                + Our product, Locata, advises the large number of entrepreneurs
                poised to enter the market in the post-pandemic era in selecting 
                locations that have the highest probabilities of success based 
                on historical data. 
        Use Case:
                + In a competitive and increasingly unforgiving landscape, new 
                entrepreneurs will do well to rely on quantitative methods when 
                making key business decisions. One such decision is the selection 
                of an appropriate location, which may be influenced by factors 
                such as accessibility, proximity to competitors, as well as the 
                nature of the local population. 
        """
        st.code(aboutlocata, language='javascript')
if __name__ == "__main__":
    about = About()
    about.main()
    # lm=Locata_Main()
    # if lm.Condition() is True:
    #   hide_pages([])  
    