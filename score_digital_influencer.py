import pandas as pd

df = pd.read_csv("dox_users_tweet_summary.csv", sep=',', header=0,index_col=False)
df['influencer_score'] = pd.Series(0, index = df.index)

##############################################
### Scoring - medical relevance #############
# Out of 100, give 50 pts to medical relevance
# Medical relevance includes count_medical_tweets

# df = pd.DataFrame(M, columns=['c%i'%i for i in range(6)])

bins = [0.0, 0.25, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
df['quantile_count_medical_tweets']=df[['count_medical_tweets']].apply(lambda s:pd.qcut(s, bins, bins[1:]).astype(float))
fbins = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
df['quantile_user_fav']=df[['user_favorites_count']].apply(lambda s:pd.qcut(s, fbins, fbins[1:]).astype(float))
df['quantile_user_followers']=df[['user_followers_count']].apply(lambda s:pd.qcut(s, fbins, fbins[1:]).astype(float))
rbins = [0.0, 0.25, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
df['quantile_count_retweets'] = df[['count_medical_retweets']].apply(lambda s:pd.qcut(s, rbins, rbins[1:]).astype(float))
df['quantile_count_retwitter_follower'] = df[['retweeters_follower_count_sum']].apply(lambda s:pd.qcut(s, fbins, fbins[1:]).astype(float))
df['quantile_tweet_retweet'] = df[['tweet_retweet_ratio']].apply(lambda s:pd.qcut(s, fbins, fbins[1:]).astype(float))
df['quantile_tweet_medical_ratio'] = df[['tweet_medical_ratio']].apply(lambda s:pd.qcut(s, fbins, fbins[1:]).astype(float))


###########################################################
###### Second part of Scoring - Engagement / Outreach########
# Look at all of these in terms of quantiles
#1. Tweet_retweet Ratio : 25%
#2. quantile_count_retweets --> Retweet_count : 30%
#3. quantile_user_followers --> Followers_count : 20%
##############################
#Potential Outreach
#4. quantile_count_retwitter_follower= 15%
#5. quantile_user_fav= 10%
new_df = df.fillna(0)
new_df['engagement_score'] = new_df['quantile_tweet_retweet']*.25 + new_df['quantile_count_retweets']*0.3 + new_df['quantile_user_followers']*0.2 + new_df['quantile_count_retwitter_follower']*.15 + new_df['quantile_user_fav']*0.1
new_df['medical_score'] = new_df['quantile_count_medical_tweets']*0.7 + new_df['quantile_tweet_medical_ratio']*0.3


new_df['influencer_score'] = new_df['engagement_score'] + new_df['medical_score']
#make influencer_score to be out of 10
new_df['influencer_score'] = new_df['influencer_score'] *5

# for i in range(new_df.index):
#     if new_df.loc[i,'count_medical_tweets'] == 0:
new_df = new_df.sort(columns = 'influencer_score', ascending = False)


final_df = new_df[['handle','influencer_score','engagement_score','medical_score', 'count_medical_tweets', 'user_followers_count', 'user_favorites_count', 'count_medical_retweets', 'retweeters_follower_count_sum']]


final_df.to_csv("influencer_score.csv", sep = ",", encoding='utf-8')
