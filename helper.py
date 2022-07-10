from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter



extract = URLExtract()
def fetch_stats(selected_user, df):
    df1 = df.copy()
    if selected_user!="Over All":
        df1 = df[df.user == selected_user]
    num_msg = df1.shape[0]
    words = []
    for msg in df1.message:
        words.extend((msg))
    #fetch the number of media messages
    num_media_msg = df1[df1['message']=='<Media omitted>\n'].shape[0]

    #fetch the number of links shared
    links=[]
    for msg in df1.message:
        links.extend(extract.find_urls(msg))


    return num_msg, len(words), num_media_msg,len(links)

def most_busy_user(df):
    x = df.user.value_counts().head()
    new_df = round((df.user.value_counts()/df.shape[0])*100,2).reset_index().rename(columns = {'index':'Name', 'user':'Percent'})
    return x,new_df


#Word Cloud
def word_cloud(selected_user, df):
    if selected_user !='Over All':
        df = df[df.user==selected_user]
    f = open('stop_hinglish.txt','r')
    stopwords = f.read()
    temp = df[df.user != 'group_notification']
    temp = temp[temp.message != '<Media omitted>\n']
    temp = temp[temp.message != 'deleted']
    def remove_stopwords(message):
        y = []
        for word in message.lower().split():
            if word not in stopwords:
                y.append(word)
        return " ".join(y)
    temp.message = temp.message.apply(remove_stopwords)
    wc =WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp.message.str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open("stop_hinglish.txt", 'r')
    stop_words = f.read()


    if selected_user!='Over All':
        df = df[df.user==selected_user]
    temp = df[df.user!='group_notification']
    temp = temp[temp.message!='<Media omitted>\n']

    words=[]

    for msg in temp.message:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return return_df

# def emoji(selected_user, df):
#     emojis=[]
#     ls =[emoji.UNICODE_EMOJI['en']]
#
#     for message in df.message:
#         emojis.extend([c for c in message if c in ls])
#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
#     return emoji_df
