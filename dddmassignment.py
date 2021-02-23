import streamlit as st 
import pandas as pd 
import numpy as np 
import seaborn as sns 
from matplotlib import pyplot as plt 


new_data = 'nobel.csv'

@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv(new_data, encoding='latin1')
    return data

nobel = load_data()


st.title("Nobel Prize Laureats!")
st.subheader("Analysis by Jaafar Hoteit")
st.write("#")


st.markdown('_ Access the sidebar to view the dataset. _')
if st.sidebar.checkbox('Display/Hide Dataset'):
    st.write(nobel)
    len_nobel = len(nobel)
    st.write('There are ', len_nobel, ' Nobel Prize Leaureats!') 
    

st.write("#")
st.write('The following table displays the top 10 countries with the most prizes:')
if st.checkbox('Display/Hide'):
    by_country = nobel['birth_country'].value_counts()
    st.write(by_country.head(10))


st.write("#")
st.write('The following table displays the proportion of USA born winners per decade')
nobel['usa_born_winner'] = np.where(nobel['birth_country'] == 'United States of America', True, False)
def decade(year):
    return np.floor(year/10)*10
nobel['decade'] = nobel['year'].apply(decade).astype('int64')
prop_usa_winners = nobel.groupby(['decade'], as_index=False).usa_born_winner.mean()
if st.checkbox('Display/Hide '):
    st.write(prop_usa_winners)

plt.style.use('fivethirtyeight')
import matplotlib.ticker as mtick
from matplotlib.ticker import PercentFormatter 

st.write('#')
st.write('We can visualize when the USA started to dominate the Nobel Charts')
if st.checkbox('Display/Hide  '):
    #fig11, ax11 = plt.subplots() 
    ##plt.rcParams['figure.figsize'] = [11, 7]
    #nobel_decade = prop_usa_winners['decade']
    #nobel_usa_born_winner = prop_usa_winners['usa_born_winner']
    #ax11.plot(nobel_decade, nobel_usa_born_winner)
    #st.pyplot(fig11)
    plt.rcParams['figure.figsize'] = [11, 7]
    ax = sns.lineplot(x='decade', y='usa_born_winner', data=prop_usa_winners)
    ax.plot()
    perc = mtick.PercentFormatter(1.0)
    ax.yaxis.set_major_formatter(perc)
    st.pyplot()

st.write('#')
st.write("Let's have a look at the proportion of female winners!")
nobel['female_winner'] = np.where(nobel['sex'] == 'Female', True, False)
prop_female_winners = nobel.groupby(['decade', 'category'], as_index=False).female_winner.mean()  
   
if st.checkbox('Display/Hide   '):
    st.write(prop_female_winners)
    if st.checkbox('Display/Hide Graph'):
        f_usa = sns.lineplot(x='decade', y='female_winner', data=prop_female_winners, hue='category')
        perc = mtick.PercentFormatter(1.0)
        f_usa.yaxis.set_major_formatter(perc)
        st.pyplot()
    
#fig10, ax10 = plt.subplots()
#decade_female = prop_female_winners['decade']
#winner_female = prop_female_winners['female_winner']
#ax10.plot(decade_female, winner_female)

#st.pyplot(fig10)



st.write('#')
st.write('Are you interested in knowing who the first female winner is?')
first_female = nobel['sex'] == 'Female'
female = nobel.loc[first_female]
smallest_f_n = female.nsmallest(1, 'year', keep='first')
if st.checkbox('Display/Hide     '):
    st.write(smallest_f_n)

st.write('#')
st.write("Let's find out who won more than ONE prize!")
more_than_one = nobel.groupby('full_name').filter(lambda group: len(group) >= 2)
if st.checkbox('Display/Hide      '):
    st.write(more_than_one)


st.write('#')
st.write("Are you interested in knowing the winners' ages?")
st.write("We used datetime to figure it out!")
nobel['birth_date'] = pd.to_datetime(nobel['birth_date'])
nobel['birth_year'] = nobel['birth_date'].dt.year
nobel['age'] = nobel['year'] - nobel['birth_year']
if st.checkbox('Display/Hide       '):
    st.write(nobel[['full_name','age']])

st.write('#')
st.write("Let's plot the age of prize winners throughout the years.")
from statsmodels.nonparametric.smoothers_lowess import lowess
year_age = sns.lmplot(x='year', y='age', data=nobel, lowess=True, aspect=2, line_kws={'color':'black'})
st.set_option('deprecation.showPyplotGlobalUse', False)
if st.checkbox('Display/Hide        '):
    st.pyplot()

st.write('#')
st.write("Let's visualize the age difference between prize categories!")
year_age = sns.lmplot(x='year', y='age', data=nobel, lowess=True, aspect=2, line_kws={'color':'black'}, row='category')
if st.checkbox('Display/Hide         '):
    st.pyplot()


st.write('#') 
st.write("Would you like to know the oldest and youngest winners?")
oldest = nobel.nlargest(1, 'age', keep='first')
youngest = nobel.nsmallest(1, 'age', keep='last')
if st.checkbox('Oldest Winner'):
    st.write(oldest)
if st.checkbox('Youngest Winner'):
    st.write(youngest)

st.write('# ')
if st.sidebar.checkbox('Balloons'):
    st.balloons()
