import streamlit as st
import pandas as pd

#@st.cache_data()
def compare(y1,y2,y3,input):
    def difference(zip,df,name):
        df2 = df[df['Zip Code'].isin([int(y1),int(y2),int(y3)])]
        average=int(df2[name].mean())
        t=df2[df2['Zip Code']==int(zip)]
        number=int(t[name].mean())/int(average)
        formatted_number = '{:,.0f}%'.format(round(number*100,3))
        return formatted_number
    
    def sum(zip,df,name):
    #data frame include 3 zip code
        df2 = df[df['Zip Code'].isin([int(y1),int(y2),int(y3)])]
        df3=df2[df2['Zip Code'] == int(zip)]
        total=len(df2[name])
        partial=len(df3[name])
        return [partial,round(partial/total,2)]
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
    col1, col2, col3, col4, col5,col6 = st.columns((0.002, 0.01, 0.002, 0.01, 0.002, 0.01))
    #input=pd.read_csv('ML_yelp_dataset.xlsx')
    
    with col2:
        #st.subheader(str(y1))
        st.markdown(":green[House value ] "+ avg(str(y1),"House Value",input))
        st.markdown(":orange[Income value ] " + avg(str(y1),"Estimated Median Income",input))
        sum1 = sum(str(y1), input, 'Estimated Median Income')
        st.markdown(":violet[Total Business] " + str(sum1[0]))
        st.markdown(":blue[Population ] " + avg(str(y1),"Population",input))

    with col4:
        #st.subheader(str(y2))
        st.markdown(":green[House value] "+ avg(str(y2),"House Value",input))
        st.markdown(":orange[Income value] " + avg(str(y2),"Estimated Median Income",input))
        sum2 = sum(str(y2), input, 'Estimated Median Income')
        st.markdown(":violet[Total Business] " + str(sum2[0]))
        st.markdown(":blue[Population] " + avg(str(y2),"Population",input))
    with col6:
        #st.subheader(str(y3))
        st.markdown(":green[House value] " + avg(str(y3),"House Value",input))
        st.markdown(":orange[Income value] " + avg(str(y3),"Estimated Median Income",input))
        sum3 = sum(str(y3), input, 'Estimated Median Income')
        st.markdown(":violet[Total Business] " + str(sum3[0]))
        st.markdown(":blue[Population] " + avg(str(y3),"Population",input))
    
