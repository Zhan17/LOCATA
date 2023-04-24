from st_pages import Page, show_pages, add_page_title
import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
import pandas as pd
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns
import tenacity
import plotly.express as px
#import scipy
import plotly.figure_factory as ff
import ast
# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be

y=st.session_state.key
st.set_page_config(layout="wide")
show_pages(
    [
        Page("About.py", "About"),
        Page("Locata_Main.py", "Locata"),
        Page("pages/Analysis.py", "Analysis"),
        Page("pages/Dashboard.py", "Dashboard")
        
    ]
)

class Analysis():
    def __init__(self,y):
        self.condition = False
        self.counter = 0
        self.title = "<div class='title'> 𝔸𝕟𝕒𝕝𝕪𝕤𝕚𝕤 </div>"
        self.subtitle = "<div class='subtitle'> Analysis on {} Busssiness type </div>".format(y[0])
        self.underlined_title = '________________________________________________________________ '
        self.team = "<div class='team'> \U0001F4D2 MongoUSC :  <code>Zihao Han</code>,  <code>Niantong Zhou</code>,  <code>Yuxuan Shi</code>,  <code>Gordon Su</code> </div>"
        self.mainpage_img= 'image2.png'
        self.y=y
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

    #st.experimental_get_query_params
    def page(self):
        st.markdown(self.title, unsafe_allow_html=True)
        st.markdown(self.subtitle, unsafe_allow_html=True)
        st.write(self.underlined_title)
        def open_business_graph(df_la):
            """
            :param zipcode str, from input widges
            :param df_la: 'open_business_Q.csv'
            :param years: year range
            :return: line chart
            """
            st.write("#### Los angeles Open business Trend from 1999 to 2023")
            def filter(years: list, zipcode, df):
                if zipcode == 'ALL':
                    df = df[(df['Year.1'] >= years[0]) & (df['Year.1'] <= years[1])]
                    df = df.groupby('time').count()
                    return df['Year']
                else:
                    # select zipcode == zipcode
                    df = df[df['ZIP CODE'] == int(zipcode)]
                    df = df[(df['Year.1'] >= years[0]) & (df['Year.1'] <= years[1])]
                    df = df.groupby('time').count()
                    return df['Year']

            Zipcode = st.text_input("You can enter Zip Code to check new business open trend for this location", 'ALL')
            years = st.slider("Select years:", 1999, 2023, value=(1999, 2023), step=1)
            df3=filter(years,Zipcode,df_la)
            st.line_chart(df3)
        def competitor_df_avg(y,df_yelp):
            """
            :param y: zipcode list
            :param df_yelp:
            :return: df and a text
            """
            st.write("#### Recommended zipcode Average Rating and Review Count")
            def avg(zipcode, name, df_yelp):
                """ calculate the average rating/Review Count of a business type in a zipcode, if no competitors in the zipcode, return 0
                :param zipcode: str
                :param name: 'Rating' or 'Review Count'
                :param df_yelp
                :return: num
                """
                filtered_df = df_yelp[df_yelp.apply(filter_alias, axis=1, args=(y[0],))]
                df_test = filtered_df[filtered_df['Zip Code'] == int(zipcode)]
                # check if the dataframe is empty
                if df_test.empty:
                    return '0'
                else:
                    number = df_test[name].mean()
                    formatted_num = "{:.2f}".format(number)
                    return formatted_num
            data = {'zipcode': [str(y[1]),str(y[2]),str(y[3])],
                    'average rate': [avg(str(y[1]),'Rating',df_yelp), avg(str(y[2]),'Rating',df_yelp), avg(str(y[3]),'Rating',df_yelp)],
                    'Average reviews': [avg(str(y[1]),'Review Count',df_yelp), avg(str(y[2]),'Review Count',df_yelp), avg(str(y[3]),'Review Count',df_yelp)]}
            df4 = pd.DataFrame(data)
            st.dataframe(df4, height=150, width=500)
            #st.dataframe(df4)

            max_avg=df4['zipcode'].tolist()
            text="""Zipcode {} 's business type {} has higher average rating and number of reviews on Yelp""".format(max_avg[0],y[0])
            st.write(text)
        def average_income(df_income,y):
            st.write("#### Average Income of the Recommended Zipcode")
            df_income_zip = df_income[df_income['Zip Code'].isin([int(y[1]), int(y[2]), int(y[3])])]
            df_income_zip['Zip Code'] = df_income_zip['Zip Code'].astype(str)
            st.dataframe(df_income_zip,height=150, width=500)
            text2 = """ Based on the following chart, you can clearly know the average income of each area and choose a community that is more in line with your product price positioning"""
            st.write(text2)

        def filter_alias(row, value):
            return value in row['Type']
        def plot_business_type_pie_overall(df, spec_bus_type):
            business_types = []
            for i in df['Type']:
                lst = ast.literal_eval(i)
                for j in lst:
                    business_types.append(j)

            business_counts = pd.Series(business_types).value_counts()
            # print(business_counts[spec_bus_type]/business_counts.sum())
            business_counts_top8 = business_counts.nlargest(8)
            business_counts_others = pd.Series({'Others': business_counts.sum() - business_counts_top8.sum()})
            business_counts_top8 = business_counts_top8.append(business_counts_others)
            if spec_bus_type not in business_counts_top8.index.tolist():
                business_counts_top9 = business_counts_top8.nlargest(9)
                business_counts_top9[spec_bus_type] = business_counts[spec_bus_type]
            else:
                business_counts_top9 = business_counts_top8
            colors = ['#FF7F50', '#000080', '#808000', '#87CEEB', '#FFDB58', '#E6E6FA', '#800000', '#98FB98',
                    '#17becf', '#008080']
            # Create a Plotly Pie chart
            fig = go.Figure(data=[go.Pie(labels=business_counts_top9.index.tolist(),
                                        values=business_counts_top9.values.tolist(),marker=dict(colors=colors))])
            fig.update_layout(
                title={'text': f"Business Types in LA area (including {spec_bus_type})", 'y': 1, 'x': 0.2})
            t1,t2=st.columns([2,1])
            t1.plotly_chart(fig)
            
            # text format
            spec_type_percentage = business_counts[spec_bus_type] / business_counts.sum() * 100
            text_format = "<div style='text-align:center; font-size: 24px;'> Current Businesses of type <strong style='color:blue'>{}</strong> accounts for <strong style='color:red'>{per:.3f}%</strong> in LA Area"
            if spec_type_percentage < 0.5:
                full_text  = text_format.format(spec_bus_type,per=spec_type_percentage)\
                            +", there may be a lack of demand for this type of business, \
                            and this could be an opportunity to fill a gap in the market and " \
                            "meet the needs of customers who may be underserved in this area. \
                            It may be worth conducting market research to identify what customers are looking for in this \
                            type of business and tailor your offering to meet those needs</div>"
                t2.markdown(full_text,unsafe_allow_html=True)
            elif spec_type_percentage >= 0.5 and spec_type_percentage < 1.5:
                full_text  = text_format.format(spec_bus_type,per=spec_type_percentage)\
                            +", this could indicate that there is some demand for this type of business, \
                            but there is still room for growth and competition. Consider conducting research to \
                            identify what customers are looking for in this type of business and how you can differentiate \
                            yourself from existing competitors."
                t2.markdown(full_text,unsafe_allow_html=True)
            else:
                full_text = text_format.format(spec_bus_type, per=spec_type_percentage) \
                        + ", which suggests that there may be significant competition in this area. \
                        It is important to conduct thorough market research to identify what customers are looking for in this \
                        type of business and how you can differentiate yourself from existing competitors.\
                        Consider identifying a niche or unique selling proposition that sets you apart from the \
                        competition and meets the needs of customers in this market."
                t2.markdown(full_text,unsafe_allow_html=True)

        def price_review_rating_table(df, spec_bus_type):
            st.write("#### Price Range and Review Rating of the Recommended Business Type")
            df['Price Range'].fillna("Not Provided", inplace=True)
            df['Type'] = df['Type'].apply(ast.literal_eval)#####changed
            filtered_data = df[df['Type'].apply(lambda x: spec_bus_type in x)]
            total_count = len(filtered_data)
            price_options = ['all'] + list(filtered_data['Price Range'].unique())
            rating_options = ['all', '0-1', '1-2', '2-3', '3-4', '4-5']
            # Create the filter widgets
            price_filter = st.selectbox('Select Price Range', price_options, index=0)
            rating_filter = st.selectbox('Select Rating Range', rating_options, index=0)
            # Filter the data based on the selected filter values
            price_all_flag = True
            rating_all_flag = True
            if price_filter != 'all':
                price_all_flag = False
                filtered_data = filtered_data[filtered_data['Price Range'] == price_filter]

            if rating_filter != 'all':
                rating_all_flag = False
                filtered_data = filtered_data[(filtered_data['Rating'] >= float(rating_filter.split('-')[0])) &
                                            (filtered_data['Rating'] < float(rating_filter.split('-')[1]))]

            if price_all_flag is True and rating_all_flag is True:
                price_counts = filtered_data.groupby('Price Range').size().reset_index(name='Count')
                price_counts['Percentage'] = (price_counts['Count'] / total_count) * 100
                price_counts['Percentage'] = price_counts['Percentage'].apply(lambda x: str(round(x, 2)) + "%")
                rating_counts = \
                filtered_data.groupby(pd.cut(filtered_data['Rating'], bins=[-0.001, 1, 2, 3, 4, 5.001], right=True))[
                    'Business Name'].count().reset_index(name='Count')
                rating_counts['Rating Range'] = ['0-1', '1-2', '2-3', '3-4', '4-5']
                rating_counts = rating_counts[['Rating Range', 'Count']]
                rating_counts['Percentage'] = (rating_counts['Count'] / total_count) * 100
                rating_counts['Percentage'] = rating_counts['Percentage'].apply(lambda x: str(round(x, 2)) + "%")
                col1, col2 = st.columns(2)
                # col1.subheader("Price Range Counts")
                col1.dataframe(price_counts,height=215, width=500)
                # col2.subheader("Rating Range Counts")
                col2.dataframe(rating_counts,height=215, width=500)
                st.write("Total: " + str(len(filtered_data)))
            elif price_all_flag is False and rating_all_flag is False:
                st.write("In price range " + str(price_filter) + " and rating " + str(rating_filter) + \
                        " , there are " + str(len(filtered_data)) + " Businesses, which is " + \
                        str(round(len(filtered_data) / total_count * 100, 2)) + "% of total.")

            elif price_all_flag is True and rating_all_flag is False:
                price_counts = filtered_data.groupby('Price Range').size().reset_index(name='Count')
                price_counts['Percentage'] = (price_counts['Count'] / total_count) * 100
                price_counts['Percentage'] = price_counts['Percentage'].apply(lambda x: str(round(x, 2)) + "%")
                st.write("In Rating " + str(rating_filter) + ": ")
                st.dataframe(price_counts,height=215, width=500)
                st.write("Total number: " + str(len(filtered_data)) + ", which is " + \
                        str(round(len(filtered_data) / total_count * 100, 2)) + "% of total.")
            else:
                rating_counts = \
                    filtered_data.groupby(pd.cut(filtered_data['Rating'], bins=[-0.001, 1, 2, 3, 4, 5.001], right=True))[
                        'Business Name'].count().reset_index(name='Count')
                rating_counts['Rating Range'] = ['0-1', '1-2', '2-3', '3-4', '4-5']
                rating_counts = rating_counts[['Rating Range', 'Count']]
                rating_counts['Percentage'] = (rating_counts['Count'] / total_count) * 100
                rating_counts['Percentage'] = rating_counts['Percentage'].apply(lambda x: str(round(x, 2)) + "%")
                st.write("In Price range " + str(price_filter) + ": ")
                st.dataframe(rating_counts,height=215, width=500)
                st.write("Total number: " + str(len(filtered_data)) + ", which is " + \
                        str(round(len(filtered_data) / total_count * 100, 2)) + "% of total.")
            #st.markdown('Streamlit is **_really_ cool**.')
        def plotrace(df):
            df=df.set_index('Zip Code')
            st.bar_chart(df)
        def zipcode_filter(zipcode_list,zip_race_df):
            # zipcode_list = st.multiselect(
            #     'What Zipcode You are interested in ',
            #     [y[1], y[2], y[3]])
            st.write(
                "<div style='text-align:center; font-size: 28px;'><b>Demographics distribution in selected zipcodes</b></div>",
                unsafe_allow_html=True)

            #st.write("<div style='text-align:center'>Race distribution in selected zipcodes</div>", unsafe_allow_html=True)

            selected_df = zip_race_df.loc[zipcode_list]
            selected_df = selected_df.reset_index()
            colors = [ '#ADD8E6', '#DAF7A6','#B19CD9']
            fig = px.bar(selected_df, x="Race", y="%", color="Zip code",color_discrete_sequence=colors)
            fig.update_layout(width=1000, height=600)
            c1, c2 ,c3= st.columns([0.1, 1, 0.1])
            c2.plotly_chart(fig)
            df3 = selected_df.groupby('Race').sum()
            sorted_df = df3.sort_values('%', ascending=False)
            index = sorted_df.index.tolist()
            zip_max_race=[]
            for i in zipcode_list:
                selected_df2 = zip_race_df.loc[[i]]
                sorted_df2 = selected_df2.sort_values('%', ascending=False)
                value=sorted_df2.values.tolist()
                zip_max_race.append([value[0][0],round(value[0][1],2),i])
            overall_max=index[0]
            str1="""<div style='text-align:left; font-size: 24px;'> This Bar plot shows zipcode {zip1},{zip2},{zip3}, has a greater proportion of Race{overall_max}. 
            There are more {race1} in {max1} which is {p1}%,more {race2} in {max2} which is {p2}% ,more {race3} in {max3} which is {p3}%.</div>""".format(
                zip1=zipcode_list[0],
                zip2 = zipcode_list[1],
                zip3 = zipcode_list[2],
                overall_max=overall_max,
                race1=zip_max_race[0][0],
                p1=zip_max_race[0][1],
                max1=zip_max_race[0][2],
                race2=zip_max_race[1][0],
                p2=zip_max_race[1][1],
                max2=zip_max_race[0][2],
                race3=zip_max_race[2][0],
                p3=zip_max_race[2][1],
                max3=zip_max_race[0][2])
            st.write(str1, unsafe_allow_html=True)

        ####### input data#######
        st.set_option('deprecation.showPyplotGlobalUse', False)
        y=st.session_state.key
        #st.title("Business Type Analysis")
        df_yelp=pd.read_csv('ML_yelp_dataset.csv')
        df_yelp_select=df_yelp.iloc[:,[1,2,3,7]]
        df_income=pd.read_csv('new_income.csv')
        df_race=pd.read_csv('new_race.csv')
        df_race=df_race[(df_race['Zip Code'] == int(y[1])) | (df_race['Zip Code'] == int(y[2])) | (df_race['Zip Code'] == int(y[3]))]
        Race_df=pd.read_csv('new_race.csv')
        Race_df.set_index('Zip Code', inplace=True)
        zipcode=Race_df.index.tolist()
        com=Race_df.columns.tolist()[1:]
        list1=[]
        for i in zipcode:
            for j in com:
                value=Race_df.loc[i, j]
                list1.append([str(i),j,value])
        zip_race_df = pd.DataFrame(list1, columns=['Zip code', 'Race', '%'])
        zip_race_df.set_index('Zip code',inplace=True)
        la_open_business = pd.read_csv('open_business_Q.csv')
        #
        #
        # plot_business_type_pie_overall(df_yelp_select, y[0])
        # price_review_rating_table(df_yelp, y[0])
        ######## within tabs ########
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
        st.markdown(css, unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Geotemporal Statistic", "Competitors' Information", "Demographics"])
        with tab1:
            open_business_graph(la_open_business)
            t1, t2 = st.columns(2)
            with t1:
                competitor_df_avg(y, df_yelp_select)
            with t2:
                average_income(df_income, y)
        with tab2:

                plot_business_type_pie_overall(df_yelp_select, y[0])
                price_review_rating_table(df_yelp, y[0])
        with tab3:

            zipcode_filter(y[1:],zip_race_df)


if __name__ == "__main__":
    Analysis(y).page()  
