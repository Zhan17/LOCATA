LOCATA:https://zhan22-locata-locata-main-912uj4.streamlit.app/Locata
Decision Model and Simulation For Complex Commercial Site Selection Based On Existing Commercial Environment Analysis
Location Recommendation System
Zihao Han, Niantong Zhou, Yuxuan Shi, Gordon Su
MongoUSC

Business Case and Project Description
Small businesses account for almost half of all economic activity in the US. The pandemic, COVID-19 restrictions, and competition from large firms have had a significant impact on the small business scene. Quantitative methods can help new businesses make key decisions, including selecting the optimal location. Location decisions strongly influence a business's success, and relocation is often not financially viable. Locata aims to recommend the most suitable location for LA small business customers based on analysis of a holistic dataset of similar businesses, their locations, and the success they enjoy.

Project Goals
Recommend the top 3 zip codes for any user-selected business type and price range based on quantitative analysis.
Provide insights and visualizations for better understanding of the characteristics of the recommended zip codes; this includes business opening trends, competitor analysis, and demographic distributions.
Provide the aforementioned recommendation and insight functionalities in an attractive and user-friendly UI.
Methods
Data and Feature Engineering
Feature data was collected from various sources, including DataLA, Zillow, and LA Almanac. Yelp reviews and business data were scraped using Fusion API. Standard cleaning, imputations, and transformations were performed. The top 50 most frequent LA business types were filtered. Less frequent business types have insufficient data for accurate evaluation. The datasets were integrated and organized by zip code: Yelp business data (ratings, rating count, price point), house value data, population data, median income data, and racial demographic data.

ML Modeling Overview
Regression models were created of the relationship between various location/demographic features and business success. Features included population, median household income, house values, racial demographics, and business price point (where applicable). Outputs were a business success metric, S, where R is the Yelp rating, N is the fraction of the number of ratings relative to the category maximum, and a/b are parameters that affect the “decay curve” shape. Random forest regressors were used as models as they balance performance and interpretability. Features were selected by a meta-transformer based on importance weights. Hyperparameters were tuned via exhaustive search.

UI Development
Locata uses the Streamlit app framework and includes recommendations, analysis, and a zip code dashboard.

Improvements - Future Scope
More input features: More features for each business would allow for improved recommendation models.
More nuanced success scoring: Qualitative analysis of Yelp reviews via NLP or even direct quantitative data on business success (revenue statements, foot traffic data, etc.) would allow for more accurate model training.
More specific recommendations: Instead of recommending only zip codes, Locata could recommend specific addresses or business zones with available real estate. This would be more useful to real business customers.
References
Business News Daily. “Tips on Choosing The Right Location for Your Business” 2023. https://www.businessnewsdaily.com/15760-choosing-business-location.html
Forbes. “How Small Businesses Drive the American Economy” 2022. https://www.forbes.com/sites/forbesbusinesscouncil/2022/03/25/how-small-businesses-drive-the-american-economy/?sh=7762a6d41699
The New York Times. “After Enduring the Pandemic, Small Businesses Face New Worries” 2023. https://www.nytimes.com/2022/07/26/business/economy/small-business-recession.html

