# Where does the $$$ go?

(app_screenshot.png)

The goal of this project was to explore and visualize the World Inequality Database to provide users insight into how income inequality
has changed over time and across income segments. The massive size and comprehensiveness of the dataset (over 1 gigabit of csv data)
forced us to temper our scope; we decided to focus on income inequality in the United States, and use the data to illustrate a quote by 
James Madison that was originally published in Alexander Hamilton's 'New York Post' (https://washingtonmonthly.com/2011/10/11/who-needs-nostradamus-when-youve-got-james-madison/). The quote deals with inequality, the social good, and military spending, which we felt were all questions that we could address with the data at hand. 

## Project Goals

The question is "How has income inequality in the United States changed over time, and what spending choices are responsible for that change?" To answer this question we produced four charts. 

1) In the first chart, the user can select a range of years and an income percentile. The chart is a bar chart that will display the growth of income in that percentile over time. However, it leads the user to want to drill deeper into how the income of that percentile compares to that of others. Rather than toggling between percentiles, the user can simply click on a bar of the graph. 

2) This will populate a second bar chart, which displays, for the selected year, the average income in that percentile range, allowing easy comparison of different percentiles. 

3) In the third chart, we plot the book value of US Corporations against total social spending. This illustrates the suprisingly proportional growth in the two areas- a roughly six-fold increase in both between 1970 and 2018. This map is zoomable and panable to let the user focus in on certain time periods. 

4) Finally, we addressed a final aspect of Madison's quote with a chart that illustrates another major spending priority in the United States: military spending. In this case we compare it to total goverment revenue from personal taxes. It's interesting to note that defense spending annually is at least three times the level of social protection spending, and often orders of magnitude more. The zoom function included in this map allows users to better analyze the year-on-year rate of change in spending. 

## Design

Overall, inequality and the way a nation chooses to, or not to, address it is a massive scope for a project. The James Madison quote on inquality gave us a "narrative" to guide our exploration, and hopefully gives the user a good conceit with which to frame the concept, and consequences. This influenced our overall selection of visualizations and narrative. Specifically addressing the produced visualizations:

1) This chart is really meant to introduce the user to the subject and draw them into exploring and manipulating the data. Thus, we included easily accessible manipulations- the two sliders, as well as tooltips and the ability to select a bar to see more about it. Additionally, we included a question and an Easter Egg of sorts- a specific question is answered if you choose a sepecific value. We felt that a chart such as a bar chart would be more familiar and accessible to users. 

2) The second chart can only be manipulated by interaction with the first chart- it is meant to supplement it by allowing users to "drill down" into the spread of income across income percentiles in any given year. We were forced to use a logarithm scale because of the enormously disproportional amount of wealth, especially in the 99.9th percentile. However, we were not fully satisfied with this choice- even though it works out "mathmetically", something is lost in not being able to make immediate visual comparisons. When we had a normal scale my thought was "you can't see how much the poor people make because of how much the rich have!" Not great from a data visualization standpoint, but it kind of makes the point in and of itself doesn't it? A final thought on log scales: https://xkcd.com/1162/

3) Here we felt that if the user had stuck with us to the third slide they might tolerate a little more experimentation. I think this graph is perhaps our least functional, but our most "beautiful". Having the years as the plotted point, instead of an axis, takes a second to grasp, but ends up being a fairly eloquent way to show growth- as time goes on, the pointwise distance between any two dots increases, maintaining a roughly slope of 1. The curve invites exploration, which the tooltips and interaction such as zooming and panning enable \("why does it double back there? What year was that"\)

4) Finally, we show military spending plotted against total goveremnt income from personal taxes. The choice of overlaid area graphs rather than staked area is appropriate, as the area "spent" on the military is literally subtracted from the total area of taxes collected. Zooming allows the user to better see trends that otherwise might be obscured by the long timeline, such as the growth in defense spending following 2001. 

## Development

We tried to follow the process outlined in the course. After selecting a data set, but before looking at it, we brainstormed some questions that we wanted to answer, then set a five-minute time to produce three sketches each of those concepts. Of these we selected our three favorite and sought some outside feedback \(which TA Venkatesh Sivaraman was kind enough to provide\). Using these concepts we began exploring the dataset. Nate did a lot of the initial sketching and broad brushstrokes of project direction. Naman set up collaberative systems such as the github, a Notion project, and DeepNote, and did the data exploration, wrangling, and initial visualization. Nate finalized the draft and did the write-up. Thus, we did an asychnronous tag-team approach rather than trying to work on the same thing at the same time. In all, the project took about 30-35 hours. The majority of the work lay in data wrangling and initial visualization, for which Naman deserves full credit. 

## Success Story

It was really cool that the reading this week \(The Truthful Ary, Chapter 5 by Alberto Cairo\) specifically addressed some of the deficencies in interperatable visualization that marred the otherwise brilliant "Captial in the 21st Century" by Thomas Pikety. We chose this dataset because of that book, and it was neat to see that others felt his visualizations could have been better-produced. There is still enormous scope of work in this area- room for much, much more. 