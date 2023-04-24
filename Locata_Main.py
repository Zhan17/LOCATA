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


# Optional -- adds the title and icon to the current page
st.set_page_config(layout="centered")
show_pages(
    [
        Page("About.py", "About"),
        Page("Locata_Main.py", "Locata"),
        Page("pages/Analysis.py", "Analysis"),
        Page("pages/Dashboard.py", "Dashboard"),
        
    ]
)
class Locata_Main:
    def __init__(self):
        self.condition = False
        self.counter = 0
        self.title = "<div class='title'> 𝕃𝕆ℂ𝔸𝕋𝔸 </div>"
        self.subtitle = "<div class='subtitle'> Decision Model and Simulation for Complex Commercial Site Selection Based on Existing Commercial Environment Analysis</div>"
        self.underlined_title = '________________________________________________________________ '
        self.team = "<div class='team'> \U0001F4D2 MongoUSC :  <code>Zihao Han</code>,  <code>Niantong Zhou</code>,  <code>Yuxuan Shi</code>,  <code>Gordon Su</code> </div>"
        #self.mainpage_img= 'image2.png'
        self.y=[]
        #self.condition = True
        # self.pagelink = ["About Locata", "Locata"]
        # self.sidpage_title = st.sidebar.title("Choose a page")
        # self.sidpage = st.sidebar.radio("Select an option", self.pagelink)
        #self.update_page()
        #self.update_page()
        

        # Use the on_change method to update the sidpage variable
        #self.sidpage.on_change(self.update_page)
        # Add CSS styles to the head of the HTML document
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

        <style>
        """, unsafe_allow_html=True)
        
        #self.image = "Locata.png"
        #self.website = "https://locata.com/"
        #self.github = "https://github.com/zhan22"
    #def get_widget_key(self, widget_value):
        #return f"{widget_value}-{id(self)}"
    # def update_page(self):
    #     counter =1
    #     if self.sidpage == "Locata" and self.condition:
    #         new_pagelink = [ "Bussiness Type", "Analysis & Dashboard"]
    #         new_sidpage = st.sidebar.radio("", new_pagelink, key=counter)
    #     else:
    #         self.pagelink = ["About Locata", "Locata"]
    #     self.sidpage = st.sidebar.radio("", self.pagelink)

    # def run(self):
    #     if self.sidpage == "About Locata":
    #         self.main()
    #     elif self.sidpage == "Locata":
    #         self.Locata()
            
    #     elif self.sidpage == "Analysis & Dashboard":
    #         self.Analysis()
    def Condition(self):
        return self.condition
    
    def main(self):
        st.markdown(self.title, unsafe_allow_html=True)
        st.markdown(self.subtitle, unsafe_allow_html=True)
        st.write(self.underlined_title)
        st.markdown(self.team, unsafe_allow_html=True)
        st.image(self.mainpage_img, use_column_width=True)
        #st.write(self.team)

    def Locata(self):
        #setting css style
        st.markdown(self.title, unsafe_allow_html=True)
        css = '''
                <style>
                    
                    .stTabs [data-baseweb="tab-list"] {
                        display: flex;
                        justify-content: center;
                        margin-top: 0rem;  /* adjust the margin-top value to increase or decrease the space */
                        margin-bottom: 0rem; /* adjust the margin-bottom value to increase or decrease the space */
                    }

                    .stTabs [data-baseweb="tab-list"] button {
                        padding: 0.5rem 1rem;  /* adjust the padding values to increase or decrease the size of each tab */
                    }

                    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
                        font-size: 2rem;
                    }
                    .notation {
                        text-align: center; 
                        font-size: 1.1em;
                        margin-top: 0.1em;
                    }
                </style>
            '''
        #show page hear and layout
        st.markdown(css, unsafe_allow_html=True)
        notation= "<div class='notation'>Please Selection for Bussiness</div>"
        tabs = ['Bussiness']
        st.tabs(tabs)
        #load data
        st.markdown(notation,unsafe_allow_html=True)
        Final_zipcode_df1=pd.read_excel('FINAL_RECS.xlsx',sheet_name='Sheet1')
        Final_zipcode_df2=pd.read_excel('FINAL_RECS.xlsx',sheet_name='Sheet2')
        col_list = Final_zipcode_df1.columns.tolist()
        col_list.extend(['Mexican','Coffee & Tea','Nail Salons','Hair Salons','Sandwiches','Fast Food','Bars','Thai'])
        col_list=sorted(col_list[1:])
        df_coordinates=pd.read_csv('coordinates.csv')
        df_coordinates=df_coordinates.dropna()
        @st.cache_resource()
        def hexagonmap(df,radius):
            INITIAL_VIEW_STATE = pdk.ViewState(latitude=df["lat"].median(), longitude=df["long"].median(), zoom=11.5,
                                            max_zoom=16, pitch=55, bearing=22)
            polygon = pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[long, lat]',
                radius=radius,
                elevation_scale=5,
                elevation_range=[1, 1000],
                pickable=True,
                extruded=True,
                get_fill_color=[0, 0, 0, 20]
            )

            DATA_URL = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json"
            geojson = pdk.Layer(
                "GeoJsonLayer",
                DATA_URL,
                opacity=0.8,
                stroked=False,
                filled=True,
                extruded=True,
                wireframe=True,
                get_elevation=35,
                get_fill_color=[255, 255, 255],
                get_line_color=[255, 255, 255],
            )
            sunlight = {
                "@@type": "_SunLight",
                "timestamp": 1564696800000,  # Date.UTC(2019, 7, 1, 22),
                "color": [255, 255, 255],
                "intensity": 1.0,
                "_shadow": True,
            }

            ambient_light = {"@@type": "AmbientLight", "color": [255, 255, 255], "intensity": 1.0}
            lighting_effect = {
                "@@type": "LightingEffect",
                "shadowColor": [0, 0, 0, 0.5],
                "ambientLight": ambient_light,
                "directionalLights": [sunlight],
            }
            r = pdk.Deck(layers=[polygon, geojson], initial_view_state=INITIAL_VIEW_STATE,
                        map_style=pdk.map_styles.LIGHT)
            return r
        def handle_radio_change(new_value):
            st.write(f"The selected value is {new_value}")
        def run_in_background(func, *args):
            """
            Helper function to run a function in the background.
            """
            thread = threading.Thread(target=func, args=args)
            thread.start()
            return thread
        #@st.cache()
        def filter_alias(row, value):
            return value in row['alias']
        #@st.cache_data()
        def get_zipcode_list(business_type):
            return Final_zipcode_df1[business_type][:3].tolist()
        #@st.cache_data()
        def get_zipcode_list2(business_type,price):
            if price=='$':
                price='1'
            elif price=='$$':
                price='2'  
            elif price=='$$$':
                price='3'
            elif price=='$$$$':
                price='4'
            return Final_zipcode_df2[f"{business_type}{price}"][:3].tolist()
        #dropdown menu
        #@st.cache_resource()
        def suggested_zip(y):
            if len(y)==0:
                st.write("Sorry, we could not find any business for you")
            else:
                #time.sleep(3)
                st.write("""
                            #### Suggested Zipcode base on your selection is
                            """)
                t3, t4, t5, t6, t7, t8 = st.columns((0.002, 0.01, 0.002, 0.01, 0.002, 0.01))
                t3.image('Imagepin.png', width=40)
                t4.write(""" ### {}""".format(y[0]))
                t5.image('Imagepin.png', width=40)
                t6.write(""" ### {}""".format(y[1]))
                t7.image('Imagepin.png', width=40)
                t8.write(""" ### {}""".format(y[2]))
                
                # if t4.button(str(y[0]),use_container_width=True):
                #     st.experimental_set_query_params(tab='dasboard',zipcode=y[0])
                # if t6.button(str(y[1]),use_container_width=True):
                #     st.experimental_set_query_params(tab='dasboard',zipcode=y[1])
                # if t8.button(str(y[2]),use_container_width=True):
                #     st.experimental_set_query_params(tab='dasboard',zipcode=y[2])
                Dashboard.compare(y1=y[0],y2=y[1],y3=y[2],input=pd.read_excel('ML_yelp_dataset.xlsx'))


        dropdown=['Select']
        for i in range(len(col_list)):
            dropdown.append(col_list[i])
        business_type = st.selectbox('',dropdown)

        price_business_list = ['Mexican', 'Coffee & Tea', 'Nail Salons', 'Hair Salons', 'Sandwiches', 'Fast Food', 'Bars', 'Thai']
        
        #get zipcode
        
        
        if business_type !='Select':
            # with money or not
            if business_type in price_business_list:
              
                price = st.selectbox('What is your price range?', ['$', '$$', '$$$', '$$$$'])
                y=get_zipcode_list2(business_type,price)
                self.y=y
            else:
                y=get_zipcode_list(business_type)
                self.y=y
            #show map
            filtered_df = df_coordinates[df_coordinates.apply(filter_alias, axis=1, args=(business_type,))]
            loc_df = pd.DataFrame([filtered_df["long"].apply(float), filtered_df["lat"].apply(float)]).T
            r = hexagonmap(loc_df,100)
            with st.spinner('Running Model...'):
                suggested_zip(y)
                st.success('Done!')
            
            with st.expander("Heat Map", expanded=True):
                st.write("""##### This displays All {} businesses located in Los Angeles on a map""".format(business_type))
                st.pydeck_chart(r)

            self.condition=True
            if self.condition is True:
                hide_pages([])
            st.session_state['key']=[business_type]
            for i in y:
                st.session_state['key'].append(str(i))
            #self.pagelink.append("Analysis & Dashboard")
            # new_pagelink=["Business Type","Analysis & Dashboard"]
            # new_sidepage_title = st.sidebar.title("Analysis & Dashboard")
            # # Update the Radio object in the sidebar to include the new page
            # self.sidpage = st.sidebar.radio("",new_pagelink, key="sidpage")

            # # Update the content of the Streamlit app based on the selected page
            # if self.sidpage == "Bussiness Type":
            #     self.Locata()
            # elif self.sidpage == "Analysis & Dashboard":
            #     self.Analysis()
            
                    #st.bar_chart(Final_zipcode_df2[f"{business_type}{price}"])

        else:
            st.session_state['key']=[]
            self.condition=False
            y=[]
            st.write("""##### This displays all businesses located in Los Angeles on a map""")
            filtered_df = df_coordinates
            loc_df = pd.DataFrame([filtered_df["long"].apply(float), filtered_df["lat"].apply(float)]).T
            r=hexagonmap(loc_df,55)
            st.pydeck_chart(r)
            self.pagelink=["About Locata", "Locata"]
            if self.condition is False:
                hide_pages(["Analysis", "Dashboard"])
        

if __name__ == "__main__":
    app=Locata_Main().Locata() 
