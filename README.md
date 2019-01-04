# HotelsNow

You can use this repository to do the following tasks :

1- Use Tripadvisor API to get a list of hotels along with their information, for a user-specified destination, a checkin date and checkout date

2- Scrape reviews'ratings and texts for each hotel selected by tripadvisor, corresponding to a user-specified timeframe ; only hotels listed on the first page are considered (around 30 hotels). A csv file containing the hotels along with their reviews' texts and ratings is generated.

3- Rank hotels based on their reviews' ratings using the percentile rank of 4 and chi-square statistic

4- Analyze the reviews's texts for each hotel, extract the polarity scores for the hotel features, such as location, service, etc. 

Corresponding slides can be found here https://www.slideshare.net/JinaneHarmouche/hotelsnow-126219304



You will need to change the path of chromedriver.exe in reviews_parser.py



Run the script by typing hotelNow.main() in the Console window

