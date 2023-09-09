#!/usr/bin/env python
# coding: utf-8

# # NFL QuarterBack's
# ## Copious Amounts of Caffeine
# **Members:**  
#     * Joey Bush IV(joeybushiv)  
#         Function: Director  
#         Contribution: Part 4  
#     * Ved Patel(patelved122)  
#         Function: GitHub czar  
#         Contribution: Part 3  
#     * Cameron Taylor(ctaylor02)    
#         Function: Team Leader  
#         Contribution: Code Blocks   
#     * Kevin(kevinchandran)  
#         Function: Review Specialist  
#         Contribution: Part 1  
#     * Devanshu(devanshu)  
#         Function: Decider  
#         Contribution: Part 2  
#     
# **Agreement:**  
#     * We will use a text chat to communicate.  
#     * Meet at least once a week following class.  
#     * A gitlab will be used to distribute group material and updated documents.  
#     * Work will be distributed as needed with a strong emphasis on working together.  
#     * Three strike basis for communication and group work before instructor is contacted.  
# 
# **Project:** Our project consists of NFL QuarterBacks game data and how they compare to one another during the season and between the years. Our data consists of QB stats for each game from 1996-2016 split up by year.  
# We seek to answer questions such as which QBs have impacts on Superbowl wins, which QBs overperform compared to QB average and how does the quarter back rating change based on wins vs losses.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read csv files for each year of data we have
QB04 = pd.read_csv('QBStats_2004.csv');
QB05 = pd.read_csv('QBStats_2005.csv');
QB06 = pd.read_csv('QBStats_2006.csv');
QB07 = pd.read_csv('QBStats_2007.csv');
QB08 = pd.read_csv('QBStats_2008.csv');
QB09 = pd.read_csv('QBStats_2009.csv');
QB10 = pd.read_csv('QBStats_2010.csv');
QB11 = pd.read_csv('QBStats_2011.csv');
QB12 = pd.read_csv('QBStats_2012.csv');
QB13 = pd.read_csv('QBStats_2013.csv');
QB14 = pd.read_csv('QBStats_2014.csv');
QB15 = pd.read_csv('QBStats_2015.csv');
QB16 = pd.read_csv('QBStats_2016.csv');

# Scrape SuperBowl winners from wikipedia table
URL = "https://en.wikipedia.org/wiki/List_of_Super_Bowl_starting_quarterbacks"
SB = pd.read_html(URL)[1]
SB['Season'] = pd.to_numeric(SB['Season'], errors = 'coerce')
SB = SB.loc[(SB['Season']>=2004) & (SB['Season']<=2016)]
SB['Season'] = SB['Season'].astype(int)
SB['Winning QB'] = SB['Winning QB'].str.rstrip('MVP')
SB['Winning QB'] = SB['Winning QB'].str.rstrip('*')


# In[2]:


# name in format 'First LastI.\xa0Last'
# Returns players average stats for specified year
def playerAVG(name, year):
    groupData = year.groupby(['qb']).mean()
    groupData = groupData.reset_index()
    mask = groupData['qb'].values == name
    playerData = groupData[mask]
    return(playerData)

# Returns superbowl winners average stats for specified year
def superbowlWinnerData(sb, data, year):
    qb = sb[sb['Season'] == year]
    qb = str(qb['Winning QB'])
    names = qb.split()
    fn = names[1]
    ln = names[2]
    fi = (fn[0])
    inputName = str(fn + " " + ln + fi + ".\xa0" + ln)
    stats = playerAVG(inputName, data)
    return(stats)  

# Returns top 5 QBs based on avg game rating
def topFiveAVGRate(year):
    groupData = year.groupby(['qb']).mean()
    sort = groupData.sort_values(by='rate', ascending=False)
    top5 = sort.head(5).mean()
    return(top5['rate'])

# Returns top 5 QBs based on avg yards per game
def topFiveAVGYards(year):
    groupData = year.groupby(['qb']).mean()
    sort = groupData.sort_values(by='yds', ascending=False)
    top5 = sort.head(5).mean()
    return(top5['yds'])

# Returns top 5 QBs based on avg touchdowns per game
def topFiveAVGtds(year):
    groupData = year.groupby(['qb']).mean()
    sort = groupData.sort_values(by='td', ascending=False)
    top5 = sort.head(5).mean()
    return(top5['td'])

# Returns top 5 QBs based on avg points per game
def topFiveAVGpts(year):
    groupData = year.groupby(['qb']).mean()
    sort = groupData.sort_values(by='game_points', ascending=False)
    top5 = sort.head(5).mean()
    return(top5['game_points'])


# In[3]:


# Create Dataframe that holds the stats from all of the superbowl winners we have
sb04 = superbowlWinnerData(SB, QB04, 2004)
sb05 = superbowlWinnerData(SB, QB05, 2005)
sb06 = superbowlWinnerData(SB, QB06, 2006)
sb07 = superbowlWinnerData(SB, QB07, 2007)
sb08 = superbowlWinnerData(SB, QB08, 2008)
sb09 = superbowlWinnerData(SB, QB09, 2009)
sb10 = superbowlWinnerData(SB, QB10, 2010)
sb11 = superbowlWinnerData(SB, QB11, 2011)
sb12 = superbowlWinnerData(SB, QB12, 2012)
sb13 = superbowlWinnerData(SB, QB13, 2013)
sb14 = superbowlWinnerData(SB, QB14, 2014)
sb15 = superbowlWinnerData(SB, QB15, 2015)
sb16 = superbowlWinnerData(SB, QB16, 2016)
sbWinners = pd.concat([sb04, sb05, sb06, sb07, sb08, sb09, sb10, sb11, sb12, sb13, sb14, sb15, sb16], axis=0)

qb_years = [QB04, QB05, QB06, QB07, QB08, QB09, QB10, QB11, QB12, QB13, QB14, QB15, QB16]


# ## Question  
# We are seeking to answer questions about the NFL QuarterBacks and their impact on winning the season. We would like to analyze the differences in the SuperBowl winners stats and the top 5 QuarterBacks stats for a given season in order to determine a relationship between certain stats and championship winning QuarterBacks.

# In[32]:



copy = sbWinners.copy()


dz = copy[copy.qb == "Tom BradyT.\xa0Brady"]
dz


# ### Part 1 : Yards
# The “yards” section of our dataset provides information on the number of yards a QB has thrown the ball in a given year. This is quite an important characteristic when taking into consideration how a game is going to go, because the more yards thrown per throw, the faster the team will be able to progress to their endzone for a touchdown.  
#   
# We wanted to analyze this statistic because of its importance in the actual game. How does the average yards of the 5 QBs with the highest yards thrown in a given year compare to the yards thrown of the super bowl winning QB in that year?

# In[4]:


# Part 1 : Analyze difference in yards for SB winners and Top 5 for season
top5avgyds = [topFiveAVGYards(i) for i in qb_years]
compYds = pd.DataFrame()
compYds['Winner'] = sbWinners['yds']
compYds['AVG'] = top5avgyds

# Set plot info
N = 13
barWidth = .5
xloc = np.arange(N)
p1 = plt.bar(xloc, compYds['AVG'], width=barWidth)
p2 = plt.bar(xloc, compYds['Winner'], width=barWidth)

# Plot stats to visualize difference
plt.ylabel('Yards')
plt.xlabel('Year')
plt.title('avg yards vs sb winner yards')
plt.legend((p1[0], p2[0]), ('AVG', 'Winner'))
plt.show()

# Display avg difference
percYds = (compYds['Winner'] / compYds['AVG'])
print(percYds.mean())


# ### Results  
# The super bowl winners usually always have a lower value for yards thrown than the average value for the top 5 from that year (with the exception of spots 2 and 5 on the bar chart, which correspond to years 2006 and 2009). Based on the analysis, there is usually a small difference in the average yards from the top 5 QBs for yards thrown and the super bowl winning QB yards thrown of that year. The SuperBowl winners’ yards were calculated to be 84% of the average yards. 

# ### Part 2 : Touchdowns  
# The “yards” section of our dataset provides information on the number of yards a QB has thrown the ball in a given year. This is quite an important characteristic when taking into consideration how a game is going to go, because the more yards thrown per throw, the faster the team will be able to progress to their endzone for a touchdown. 
#   
# We wanted to analyze this statistic because of its importance in the actual game. How does the average yards of the 5 QBs with the highest yards thrown in a given year compare to the yards thrown of the super bowl winning QB in that year?

# In[5]:


# Part 2 : Analyze difference in tds for SB winners and Top 5 for season
top5avgtds = [topFiveAVGtds(i) for i in qb_years]
compTds = pd.DataFrame()
compTds['Winner'] = sbWinners['td']
compTds['AVG'] = top5avgtds

# Set plot info
N = 13
barWidth = .5
xloc = np.arange(N)
p1 = plt.bar(xloc, compTds['AVG'], width=barWidth)
p2 = plt.bar(xloc, compTds['Winner'], width=barWidth)

# Plot stats to visualize difference
plt.ylabel('TDs')
plt.xlabel('Year')
plt.title('avg tds vs sb winner yards')
plt.legend((p1[0], p2[0]), ('AVG', 'Winner'))
plt.show()

# Display avg difference
percTds = (compTds['Winner'] / compTds['AVG'])
print(percTds.mean())


# ### Results  
# As you can see, for each year the average number of touchdowns is always more than the number of touchdowns by the Super Bowl winners, with the exception of spots 2 and 5 on the bar chart, which correspond to years 2006, 2009, and 2016. These differences were observed to be on average the SuperBowl winner has 77% of the avg touchdown amount.

# ### Part 3 : QB Rating  
# The rating of a particular player may differ from game to game. Further, the quarterback with the highest rating may only sometimes win or even play in the super bowl. In part three, we aim to see the difference in ratings for SB winners and the Top 5 QBs for the season.  
# What do we mean by rating?  
# Rating refers to passer rating and is calculated using a player's passing attempts, completions, yards, touchdowns, and interceptions.  
# Different aspects of passer rating:  
# Passing Attempts: Passes caught divided by passes attempted minus .30, multiplied by .05, and multiplied by 100.  
# Average Yards Gained: total passing yards separated by passes tried minus 3, then multiplied by .25.  
# Percentage of touchdown passes: touchdowns thrown divided by passes attempted multiplied by .2.  
# Percentage of interceptions: Interceptions thrown divided by passing attempts multiplied by .25, multiplied by 100, then minus this result from 2.375.

# In[6]:


# Part 3 : Analyze difference in ratings for SB winners and Top 5 for season
top5avgrate = [topFiveAVGRate(i) for i in qb_years]
compRate = pd.DataFrame()
compRate['Winner'] = sbWinners['rate']
compRate['AVG'] = top5avgrate

# Set plot info
N = 13
barWidth = .5
xloc = np.arange(N)
p1 = plt.bar(xloc, compRate['AVG'], width=barWidth)
p2 = plt.bar(xloc, compRate['Winner'], width=barWidth)

# Plot stats to visualize difference
plt.ylabel('Rate')
plt.xlabel('Year')
plt.title('avg rate vs sb winner yards')
plt.legend((p1[0], p2[0]), ('AVG', 'Winner'))
plt.show()

# Display avg difference
percRate = (compRate['Winner'] / compRate['AVG'])
print(percRate.mean())


# ### Results  
# Based on our analysis, we can see that the average passer rating of the quarterbacks in the Superbowl was lower than the average of the top 5. This indicates that the Superbowl quarterbacks are not usually the best performing QuarterBack in terms of passing attempts, average yards gained, percentage of touchdown passes, and share of interceptions. 

# ### Part 4 : Game Points  
# The average points analysis consists of a comparison with the winning football team, between the years of 2004 through 2016, and the top five teams that scored the most points. We questioned whether or not there would be a large difference between the total points of the winning team compared to the teams that fell short. We hypothesized that the difference of points scored would heavily sway towards the winning team. Our motivation behind this idea is to try and understand the precise relevance to how higher standing teams compare to the best in the league during that year.
# 
# In the code, we extract the necessary inputs from our data set of the top five QBs based on average points per game. We then assemble our data frame, we align our data frame in a nice visual to help us make a comparison between the winning QB and the average of the top 5, and of course not forgetting to color code our two values. Establishing a clear understanding of the points scored.

# In[7]:


# Part 4 : Analyze difference in points for SB winners and Top 5 for season
top5avgpts = [topFiveAVGpts(i) for i in qb_years]
compPts = pd.DataFrame()
compPts['Winner'] = sbWinners['game_points']
compPts['AVG'] = top5avgpts

# Set plot info
N = 13
barWidth = .5
xloc = np.arange(N)
p1 = plt.bar(xloc, compPts['AVG'], width=barWidth)
p2 = plt.bar(xloc, compPts['Winner'], width=barWidth)

# Plot stats to visualize difference
plt.ylabel('Pts')
plt.xlabel('Year')
plt.title('avg pts vs sb winner pts')
plt.legend((p1[0], p2[0]), ('AVG', 'Winner'))
plt.show()

# Display avg difference
percPts = (compPts['Winner'] / compPts['AVG'])
print(percPts.mean())


# ### Results  
# Based on our analysis, we can see that the average points scored by the quarterbacks in the Superbowl was lower than the average of the top 5. This indicates that the Superbowl quarterbacks generally do not have to throw nearly as many yards as the most thrown in the league and in fact on average only throw 63% as many yards as the top 5. Due to this finding (and the others above); brainstorming on what constitutes a formula for a winning football team may be more complicated than what meets the eye. Our understanding and investigations will help with the seemingly never ending search for a purely winning football team formula. A potential caveat: computing the winning football team into the average of the top 5 football teams. For future works, it might be interesting to not include the winning football team into the average top 5 if said winning team QB made it into the top 5. In the future, we could compare that visual with the graph above to see how large of an impact that may potentially have. It would also be interesting to see if our results hold up over the seasons that are not found in our data set (such as the 2017 to the current football season).

# ## Combining Results  
# Now that we have the averages for the top 5 in each stat as well as the stats for our winners, we can use a t test between each stat to determine if there is statistical significance in the averages of these differences. If we determine there is a difference we will need to check whether the stat is closer or farther from 

# In[8]:


from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols

# Compile different stat data into usable format
data = []
data.append(percYds)
data.append(percTds)
data.append(percRate)
data.append(percPts)
df = pd.DataFrame(data).transpose()
df.columns=['Yards', 'Tds', 'Rate', 'Points']
dfStack = df.stack().to_frame()
dfStack = dfStack.reset_index()
dfStack.columns=['year', 'Stat', '%Diff']

# Box plot to show distribution of stat differences
dfStack.boxplot('%Diff', by='Stat', figsize=(12, 8))

# Calculate p value from f tests
fvalue, pvalue = stats.f_oneway(df['Yards'], df['Tds'], df['Rate'], df['Points'])
print(fvalue, pvalue)


# ### Results  
# From the independent anova tests we can conclude that with a p value < 0.05 there is statistical evidence that at least one of the stats avg difference is different from the others. Following this conclusion we can run a tukeys post HOC test to determine which pairs differ.

# In[9]:


from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Pairwise test between each Stat
tukey = pairwise_tukeyhsd(endog=dfStack['%Diff'], groups=dfStack['Stat'], alpha=0.05)
print(tukey)


# ## Conclusion
# From the pairwise comparisons we can see that yards was closer to the the top5 average when compared to Points and Rating. These differences lead us to believe that Yards thrown is the most important stat when it comes to determining a SuperBowl Winner as the winners avg yards per game puts them nearest to the top 5 QuarterBacks.
