from st_pages import Page, show_pages, add_page_title
import streamlit as st
import streamlit as st
import pandas as pd
import numpy as np
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
# Optional -- adds the title and icon to the current page

# Specify what pages should be shown in the sidebar, and what their titles and icons
# should be
st.set_page_config()
y=st.session_state.key
show_pages(
    [
        Page("About.py", "About"),
        Page("Locata_Main.py", "Locata"),
        Page("pages/Analysis.py", "Analysis"),
        Page("pages/Dashboard.py", "Dashboard")
        
    ]
)

class Dashboard():
    def __init__(self,y):
        self.condition = False
        self.counter = 0
        self.title = "<div class='title'> 𝔻𝕒𝕤𝕙𝕓𝕠𝕒𝕣𝕕 </div>"
        self.subtitle = "<div class='subtitle'> Dashboard on {} Busssiness type For Zip code:{}, {}, {}  </div>".format(y[0],y[1],y[2],y[3])
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
        # st.markdown(css, unsafe_allow_html=True)
        # #notation= "<div class='notation'>Please Selection for Bussiness</div>"
        # Tabs=[y[1],y[2],y[3]]
        # active_tab = st.tabs(Tabs)
        # with active_tab[0]:
        #     st.write('This is the content of tab 1')
        # with active_tab[1]:
        #     st.write('This is the content of tab 2')
        # with active_tab[2]:
        #     st.write('This is the content of tab 3')
        def open_business_graph(y,input,zip):
            def avg(zipcode,name,input):
                df_yelp=input[input['Zip Code'] == int(zipcode)]
                #df drop na
                #df_yelp=df_yelp.dropna()
                number = int(df_yelp[name].dropna().mean())
                if name=='Population':
                    formatted_number = '{:,.0f}'.format(number)
                else:
                    formatted_number = '${:,.0f}'.format(number)
                return formatted_number
            def difference(zip,df,name):
                df2 = df[df['Zip Code'].isin([int(y[0]),int(y[1]),int(y[2])])]
                average=int(df2[name].mean())
                t=df2[df2['Zip Code']==int(zip)]
                number=int(t[name].mean())/int(average)
                formatted_number = '{:,.0f}%'.format(round(number*100,3))
                return formatted_number
            def sum(zip,df,name):
                #data frame include 3 zip code
                df2 = df[df['Zip Code'].isin([int(y[0]),int(y[1]),int(y[2])])]
                df3=df2[df2['Zip Code'] == int(zip)]
                total=len(df2[name])
                partial=len(df3[name])
                return [partial,round(partial/total,2)]
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("House Value", avg(zip, "House Value", input), difference(zip, input, 'House Value'))
            col2.metric("Income", avg(zip, "Estimated Median Income", input), difference(zip, input, 'Estimated Median Income'))
            col4.metric("Population", avg(zip, "Population", input), difference(zip, input, 'Population'))
            sum1 = sum(zip, input, 'Estimated Median Income')
            formatted_number = '{:,.0f}%'.format(round(sum1[1] * 100, 3))
            col3.metric("Total Business", sum1[0], formatted_number)
                        
        def filter_alias(row, value):
            return value in row['Type']
        def plot_business_type_pie(df, zipcode, spec_bus_type):
            df_zip = df[df['Zip Code'] == int(zipcode)]
            business_types = []
            for i in df_zip['Type']:
                lst = ast.literal_eval(i) #####changed
                for j in lst:
                    business_types.append(j)

            business_counts = pd.Series(business_types).value_counts()
            business_counts_top8 = business_counts.nlargest(8)
            business_counts_others = pd.Series({'Others': business_counts.sum() - business_counts_top8.sum()})
            business_counts_top8 = business_counts_top8.append(business_counts_others)
            include_type_flag = True
            if spec_bus_type in business_counts.index.tolist():
                if spec_bus_type not in business_counts_top8.index.tolist():
                    business_counts_top9 = business_counts_top8.nlargest(9)
                    business_counts_top9[spec_bus_type] = business_counts[spec_bus_type]
                else:
                    business_counts_top9 = business_counts_top8
            else:
                include_type_flag = False
                business_counts_top9 = business_counts_top8
            css = """
                    <style>
                    .interp-text {
                            text-align: center; 
                        font-size: 1.25em;
                        margin-top: 0.1em;
                    }
                    </style>
                """
            # Create a Plotly Pie chart
            fig = go.Figure(data=[go.Pie(labels=business_counts_top9.index.tolist(),
                                        values=business_counts_top9.values.tolist())])
            if include_type_flag is True:
                fig.update_layout(
                    width=700,
                    height=500,
                )
                fig.update_layout(
                    title={'text': f"Business Types in Zipcode {zipcode} (including {spec_bus_type})", 'y': 0.95, 'x': 0.1})
            else:
                fig.update_layout(
                    width=700,
                    height=500,
                )
                fig.update_layout(
                    title={'text': f"Business Types in Zipcode {zipcode} (not including {spec_bus_type})", 'y': 0.95, 'x': 0.1})
                st.markdown(
                    f"**_:blue[{spec_bus_type}]_** currently not exist in the area of **_:green[{zipcode}]_**, you can be the **_:red[First!]_**")
            c1, c2 , c3 = st.columns([0.1,1,0.1])

            
            
            c2.plotly_chart(fig)
            if include_type_flag is True:
                if business_counts[spec_bus_type] / business_counts.sum() * 100 <= 2:
                    c2.markdown(
                        f"<div class='interp-text'>In <strong style='color:blue'>{zipcode}</strong> area, <strong style='color:red'>{spec_bus_type}</strong> type represents a small portion of the market, <br> \
                        This could indicate a niche market with potential for growth. Consider focusing on unique <br> \
                        offerings and targeted marketing strategies to attract customers.<br> \
                        <br> \
                        <br> \
                            </div>", unsafe_allow_html=True)
                elif business_counts[spec_bus_type] / business_counts.sum() * 100 <= 5:
                    c2.markdown(f"<div class='interp-text'>In <strong style='color:blue'>{zipcode}</strong> area, <strong style='color:red'>{spec_bus_type}</strong> type have moderate competition. <br> \
                                To differentiate your business, consider offering exceptional customer service, <br> \
                                enhancing the quality of your products or services, and implementing effective  <br> \
                                marketing campaigns.<br> \
                                <br> \
                                <br> \
                                </div>", unsafe_allow_html=True)
                else:
                    c2.markdown(f"In <strong style='color:blue'>{zipcode}</strong> area, <strong style='color:red'>{spec_bus_type}</strong> type accounts for a significant percentage of the market. <br> \
                                To stand out from the competition, analyze your competitors' strengths and weaknesses, <br> \
                                and find opportunities to differentiate your business through unique products, services, <br> \
                                or experiences.<br> \
                                <br> \
                                <br> \
                                </div>", unsafe_allow_html=True)

                    
        def scatter_plot(df, zip, spec_bus_type):
            df_yelp3 = df.iloc[:, [3, 5, 6, 7]]
            filtered_df = df_yelp3[df_yelp3.apply(filter_alias, axis=1, args=(spec_bus_type,))]
            # select Zip Code rows with zipcode 91303
            df4 = filtered_df[filtered_df['Zip Code'] == int(zip)]
            # change columns names
            df4.columns = ['Zip Code', 'lat', 'lon', 'Type']
            df5 = df4[['lat', 'lon']]
            if len(df5) == 0:
                pass
            # df2 = df[['lat', 'lon']][(df['PRIMARY NAICS DESCRIPTION'] == 'Full-service restaurants') & (df['ZIP CODE'] == int(zip))]
            else:
                st.map(df5)
                str2 = """ Upper map figure shows the density of {business_type} in the {selected_zip_code} base on business from Yelp. 
                        The area with more red dots means there are more {business_type} in that area which might have higher competition.""".format(
                    business_type=spec_bus_type, selected_zip_code=zip)
                st.caption(str2)
        def plot_house_value_and_percentage_bar_line(df,zipcode):
            date_columns = pd.to_datetime(df.columns[1:])
            df.columns = ['Zip Code'] + date_columns.tolist()
            zipcode_data = df[df['Zip Code'] == zipcode].iloc[:, 1:].T
            zipcode_data.columns = ['House Value']
            # Calculate the percentage change in house value
            zipcode_data['Percentage Change'] = zipcode_data['House Value'].pct_change() * 100

            # Create a combined bar and line chart
            fig = go.Figure()
            fig.add_trace(go.Bar(
            x=zipcode_data.index,
            y=zipcode_data['House Value'],
            name='House Value',
            marker_color='rgba(55, 83, 109, 0.7)',
            marker_line_color='rgba(55, 83, 109, 1.0)',
            marker_line_width=1.5,
            opacity=0.6,
            yaxis='y1'
            ))

            fig.add_trace(go.Scatter(
            x=zipcode_data.index,
            y=zipcode_data['Percentage Change'],
            name='Percentage Change',
            mode='lines+markers',
            line=dict(color='firebrick', width=2),
            marker=dict(symbol='circle', size=6),
            yaxis='y2'
            ))
            fig.update_layout(
                width=800,
                height=600,
            )
            fig.update_layout(
            title=f"House ZHVI Value and Percentage Change for Zipcode {zipcode}",
            xaxis_title="Date",
            yaxis_title="House ZHVI Value",
            yaxis=dict(title="House ZHVI Value", side="left", position=0.05),
            yaxis2=dict(title="Percentage Change", overlaying='y', side='right', position=0.95, tickformat='.2f'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(family="Arial", size=12, color="black"),
            )
            #c1,c2,c3 = st.columns([0.1,3,0.1])
            st.plotly_chart(fig)

            latest_date = zipcode_data.index.max()
            latest_house_value = zipcode_data.loc[latest_date, 'House Value']

            # Convert the index to a DatetimeIndex
            zipcode_data.index = pd.to_datetime(zipcode_data.index)

            # Calculate the house value change and percentage change for each year in the last three years
            last_3_years = zipcode_data.loc[latest_date - pd.DateOffset(years=3):]
            yearly_value_changes = last_3_years['House Value'].resample('Y').last().pct_change() * 100
            yearly_value_diff = last_3_years['House Value'].resample('Y').last().diff()

            # Calculate the average of the last three years' yearly house value change percentage and yearly house value change
            average_yearly_percentage_change = yearly_value_changes.mean()
            average_yearly_value_change = yearly_value_diff.mean()
            total_percentage_change = ((zipcode_data.loc[latest_date, 'House Value'] / zipcode_data.loc[
            latest_date - pd.DateOffset(years=3), 'House Value']) - 1) * 100

            css = """
                <style>
                .interp-text {
                        text-align: center; 
                    font-size: 1.25em;
                    margin-top: 0.1em;
                    margin-bottom:0.5em;
                }
                </style>
            """
            st.markdown(css, unsafe_allow_html=True)
            st.markdown(f"<div class='interp-text'> In zipcode {zipcode}, the latest house ZHVI value is ${latest_house_value:,.2f} as of {latest_date.strftime('%Y-%m-%d')}. </div>", unsafe_allow_html=True)

            #st.markdown(f"<div class='interp-text'> In zipcode {zipcode}, the latest house value is ${latest_house_value:,.2f} as of {latest_date.strftime('%Y-%m-%d')}. </div>", unsafe_allow_html=True)
            #st.write(
            #f"In zipcode {zipcode}, the latest house value is ${latest_house_value:,.2f} as of {latest_date.strftime('%Y-%m-%d')}.")
            st.markdown(f"<div class='interp-text'> The average of the last three years' yearly house ZHVI value change percentage is {average_yearly_percentage_change:.2f}%. </div>", unsafe_allow_html=True)
            #st.write(
            #f"Average of the last three years' yearly house value change percentage: {average_yearly_percentage_change:.2f}%")
            st.markdown(f"<div class='interp-text'> The average of the last three years' yearly house ZHVI value change is ${average_yearly_value_change:,.2f}. </div>", unsafe_allow_html=True)
            #st.write(f"Average of the last three years' yearly house value change: ${average_yearly_value_change:,.2f}")
            st.markdown(f"<div class='interp-text'> The total percentage of house ZHVI value change in the last three years is {total_percentage_change:.2f}%.  <br> \
             <br> \
              <br> \
              </div>", unsafe_allow_html=True)
            #st.write(f"Total percentage of house value change in the last three years: {total_percentage_change:.2f}%")
            q1,q2,q3=st.st.columns([0.1,3,0.1])
            q2.caption("Zillow Home Value Index (ZHVI): A measure of the typical home value and market changes across a given region and housing type. It reflects the typical value for homes in the 35th to 65th percentile range.")
        def competitor_bar_charts(df,b_type,zipcode):
            df['Price Range'].fillna("Not Provided", inplace=True)
            df_zip = df[df['Zip Code'] == zipcode]
            df_zip['Type'] = df_zip['Type'].apply(ast.literal_eval)#####changed
            filtered_data = df_zip[df_zip['Type'].apply(lambda x: b_type in x)]
            price_counts = filtered_data.groupby('Price Range').size().reset_index(name='Count')
            fig1 = go.Figure(go.Bar(x=price_counts['Price Range'], y=price_counts['Count'],
                                    text=(price_counts['Count'] / price_counts['Count'].sum() * 100).apply(lambda x: f'{x:.1f}%'),
                                    textposition='auto'))
            fig1.update_layout(width=200, height=400,title=dict(text='Price Range vs. Business Count',font=dict(size=13)))
            fig1.update_xaxes(title_text='Price Range')
            fig1.update_yaxes(title_text='Business Count')
            rating_counts = \
                filtered_data.groupby(pd.cut(filtered_data['Rating'], bins=[-0.001, 1, 2, 3, 4, 5.001], right=True))[
                'Business Name'].count().reset_index(name='Count')
            rating_counts['Rating Range'] = ['0-1', '1-2', '2-3', '3-4', '4-5']
            rating_counts = rating_counts[['Rating Range', 'Count']]
            fig2 = go.Figure(go.Bar(x=rating_counts['Rating Range'], y=rating_counts['Count'],
                                    text=(rating_counts['Count'] / rating_counts['Count'].sum() * 100).apply(
                                        lambda x: f'{x:.1f}%'), textposition='auto'))
            fig2.update_layout(width=200, height=400,title=dict(text='Rating Range vs. Business Count',font=dict(size=13)))
            fig2.update_xaxes(title_text='Rating Range')
            fig2.update_yaxes(title_text='Business Count')
            min_review_count = int(filtered_data['Review Count'].min())
            max_review_count = int(filtered_data['Review Count'].max())
            review_bins = np.linspace(min_review_count, max_review_count, 6).astype(int)
            review_counts = filtered_data.groupby(
                pd.cut(filtered_data['Review Count'], bins=review_bins, include_lowest=True)).size().reset_index(
                name='Count').rename(columns={'Review Count': 'Review Count Range'})
            review_counts['Review Count Range'] = review_counts['Review Count Range'].apply(
                lambda x: f'{int(x.left)}-{int(x.right)} reviews')
            fig3 = go.Figure(go.Bar(x=review_counts['Review Count Range'], y=review_counts['Count'],
                                    text=(review_counts['Count'] / review_counts['Count'].sum() * 100).apply(
                                        lambda x: f'{x:.1f}%'), textposition='auto'))

            fig3.update_layout(width=200, height=400,title=dict(text='Review Count Range vs. Business Count',font=dict(size=11)))
            fig3.update_xaxes(title_text='Review Count Range')
            fig3.update_yaxes(title_text='Business Count')
            # Display the three bar charts horizontally in Streamlit
            col1, col2, col3 = st.columns(3)
            with col1:
                st.plotly_chart(fig1)
                most_price_range_count = price_counts.loc[price_counts['Count'].idxmax()]
                st.markdown(
                f"The most common price range is **_:blue['{most_price_range_count['Price Range']}']_** with **_:red[{most_price_range_count['Count']}]_** businesses.")
            with col2:
                st.plotly_chart(fig2)
                rating_counts['Interval'] = rating_counts['Rating Range'].apply(
                lambda x: pd.Interval(float(x.split('-')[0]), float(x.split('-')[1]), closed='left'))
                ratings_gt_3_5 = rating_counts[rating_counts['Interval'].apply(lambda x: x.mid > 3.5)]
                count_ratings_gt_3_5 = ratings_gt_3_5['Count'].sum()
                percentage_ratings_gt_3_5 = count_ratings_gt_3_5 / rating_counts['Count'].sum() * 100
                st.markdown(
                f"There are **_:red[{count_ratings_gt_3_5}]_** businesses with good reputation(rating>3.5), making up **_:orange[{percentage_ratings_gt_3_5:.1f}%]_** of the total.")
            with col3:
                st.plotly_chart(fig3)
                low_price_range = filtered_data[filtered_data['Price Range'].isin(['$', '$$'])]
                high_price_range = filtered_data[filtered_data['Price Range'].isin(['$$$', '$$$$'])]
                avg_low_price_range_reviews = low_price_range['Review Count'].mean()
                avg_high_price_range_reviews = high_price_range['Review Count'].mean()
                st.markdown(f"Average review count for **:green[inexpensive]** businesses is **_:red[{avg_low_price_range_reviews:.1f}]_**, \
                and for **:violet[expensive]** businesses is **_:red[{avg_high_price_range_reviews:.1f}]_**")
        def top5_most_reviews_businesses(df,zipcode,b_type):
            df['Price Range'].fillna("Not Provided", inplace=True)
            df_zip = df[df['Zip Code'] == zipcode]
            df_zip['Type'] = df_zip['Type'].apply(ast.literal_eval)######changed
            df_zip['Business Name'] = df_zip['Business Name'].str.replace("-"," ").str.title()
            filtered_data = df_zip[df_zip['Type'].apply(lambda x: b_type in x)]
            sorted_df = filtered_data.sort_values(by='Review Count', ascending=False)
            head = 5
            if len(sorted_df)<5:
                head = len(sorted_df)
            top_5_businesses = sorted_df.head(head)
            # Format the 'ratings' column as a 1 decimal float
            top_5_businesses['Rating'] = top_5_businesses['Rating'].apply(lambda x: f"{x:.1f}")
            # Format the 'reviews number' column as an int
            top_5_businesses['Review Count'] = top_5_businesses['Review Count'].apply(lambda x: int(x))
            # Create the URL as a hyperlink in the business name
            top_5_businesses['Business Name'] = top_5_businesses.apply(
                lambda row: f'<a href="{row["url"]}" target="_blank">{row["Business Name"]}</a>', axis=1)
            # Select the columns to display
            columns_to_display = ['Business Name', 'Price Range', 'Rating', 'Review Count']
            top_5_businesses_display = top_5_businesses[columns_to_display]
            # Display the custom table in Streamlit using pandas' Styler
            st.markdown(f"#####  Top {head} most reviewed **_:violet[{b_type}]_** businesses in **_:green[{zipcode}]_** area: ")
            st.write("<div style='text-align:center'>"+top_5_businesses_display.style.set_properties(**{'text-align': 'center'}).hide_index().render()+ "</div>",
                    unsafe_allow_html=True)
            
        y=st.session_state.key
        df_yelp=pd.read_csv('ML_yelp_dataset.csv')
        #same as ML data set but with URL
        df3 = pd.read_csv('ML_yelp_dataset (1).csv')
        house_df = pd.read_csv('new_housevalue.csv')

        def main(yi,b_type,df_yelp,df3,house_df,y):
            
            #st.write(""" ## Dashboard for Zipcode {}""".format(yi))
            open_business_graph(y[1:],df_yelp,yi)
            tab1, tab2= st.tabs(["House ZHVI Trend", "Competitors"])
            
            
            with tab1:
                plot_house_value_and_percentage_bar_line(house_df, int(yi))
            with tab2:
                plot_business_type_pie(df_yelp, yi, b_type)
                C1,C2,C3=st.columns([0.1,1,0.1])
                try:
                    with C2.container():
                        top5_most_reviews_businesses(df3, int(yi), b_type)
                    with C2.container():
                        competitor_bar_charts(df_yelp, b_type, int(yi))
                    
                    with C2.container():
                        
                        scatter_plot(df_yelp, yi, b_type)


                except:
                    pass
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
        tab1,tab2,tab3=st.tabs([y[1],y[2],y[3]])
        with tab1:
            main(y[1],y[0],df_yelp,df3,house_df,y)
        with tab2:
            main(y[2],y[0], df_yelp,df3,house_df,y)
        with tab3:
            main(y[3],y[0], df_yelp,df3,house_df,y)



if __name__ == "__main__":
    Dashboard(y).page()
