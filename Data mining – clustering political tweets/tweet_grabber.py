import re

import tweepy

import access_tokens as creds

auth = tweepy.OAuthHandler(creds.CONSUMER_KEY, creds.CONSUMER_SECRET)
auth.set_access_token(creds.ACCESS_TOKEN_KEY, creds.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

leaders = ['JustinTrudeau', 'realDonaldTrump', 'ElizabethMay',
           'AndrewScheer', 'theJagmeetSingh', 'elonmusk', 'BarackObama',
           'HillaryClinton', 'MittRomney', 'SpeakerRyan', 'JoeBiden',
           'SenJohnMcCain', 'narendramodi', 'algore', 'GavinNewsom',
           'SarahPalinUSA', 'SpeakerBoehner']
file_names = ['justin_trudeau', 'donald_trump', 'elizabeth_may',
              'andrew_scheer', 'jagmeet_singh', 'elon_musk', 'barack_obama', 'hillary_clinton',
              'mitt_romney', 'paul_ryan', 'joe_biden', 'john_mccain', 'narendra_modi', 'al_gore',
              'gavin_newsom', 'sarah_palin', 'john_boehner']
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" # emoticons
                           u"\U0001F300-\U0001F5FF" # symbols & pictographs
                           u"\U0001F680-\U0001F6FF" # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF" # flags (iOS)
                           "]+")
list_of_all_tweets = {}
leader_index = 0
number_en_tweets = 0
j = 0
for leader in leaders:
    tweets = api.user_timeline(
        screen_name=leader, count=200, tweet_mode='extended')
    # max requests = 200 for each UNIQUE request, tweet_mode='extended' means
    # full text of tweet
    for tweet in tweets:
        if tweet.lang == 'en':
            # only get english tweets
            if 'retweeted_status' in tweet._json:
                text_string = tweet._json['retweeted_status']['full_text']
            else:
                text_string = tweet.full_text

            list_of_all_tweets[number_en_tweets] = emoji_pattern.sub(
                r'', text_string)
            # remove any unicode characters that aren't the "regular"
            # characters
            number_en_tweets += 1
            # it is possible that tweets contain line breaks (\n) so we use a
            # dict to group each tweet together
    if (leader_index == 0 or leader_index == 3 or leader_index == 4):
        upper_bound = 4
    else:
        upper_bound = 2
    # some of the people post the same tweet in different languages, reduce the count by the number of languages used
    # time is bounded by the time it takes for each request
    for i in range(0, upper_bound):
        last_tweet_id = tweet._json['id_str']
        # we can continue with another 800 requests using max_id parameter
        # which refers to the every tweet before the last tweet id
        tweets = api.user_timeline(
            screen_name=leader, count=200, tweet_mode='extended', max_id=last_tweet_id)
        for tweet in tweets:
            if tweet.lang == 'en':
                if 'retweeted_status' in tweet._json:
                    text_string = tweet._json['retweeted_status']['full_text']
                else:
                    text_string = tweet.full_text
                list_of_all_tweets[number_en_tweets] = emoji_pattern.sub(
                    r'', text_string)
                number_en_tweets += 1

file_csv = open(
    "all_tweets_uncleaned.csv", "w", encoding='utf-8')
# encoding='utf-8' since there are possible unicode characters that aren't filtered by emoji_pattern
# we might be able to parse these later on once it's been added to the csv
count = 0

for key in list_of_all_tweets:
    line = list_of_all_tweets[key].strip().split()
#     file_csv.write(line)
    for token in line:
#         token = re.sub(r'[^\s]', '', token) # keep the - and _ chars
        if (token != "&amp;" and not token.startswith("https")):
            file_csv.write(token)
            file_csv.write(" ")
 
        count += 1
    file_csv.write("\n")
    count = 0
j = number_en_tweets
leader_index += 1
file_csv.close()
