import matplotlib.pyplot as plt
from wordcloud import WordCloud
import streamlit as st
import  preprocess, helper
import pandas as pd

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocess.preprocess(data)

    #st.dataframe(df)
    # fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Over All")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    if selected_user=="Over All":
        st.dataframe(df)
    else:
        st.dataframe(df[df.user==selected_user])

    if st.sidebar.button("Show Analysis"):
         num_messages , length , num_media_msg, num_links = helper.fetch_stats(selected_user, df)
         col1, col2, col3, col4 = st.columns(4)

         with col1:
             st.header("Total Messages")
             st.title(num_messages)
         with col2:
                st.header("Totel Words")
                st.title(length)
         with col3:
             st.header("Media Shared")
             st.title(num_media_msg)
         with col4:
             st.header("Links Shared")
             st.title(num_links)

        #find the top 5  busiest users

         if selected_user=="Over All":
             st.title("Most Busy Users")
             x,new_df = helper.most_busy_user(df)
             fig,ax = plt.subplots()
             col1, col2 = st.columns(2)
             with col1:
                 ax.pie(x.values,labels = x.index,autopct = "%0.2f%%")
                 plt.xticks(rotation='vertical')
                 st.pyplot(fig)
             with col2:
                 st.dataframe(new_df)


         #Word Cloud

         st.title("World Cloud")
         df_wc = helper.word_cloud(selected_user,df)
         fig,ax = plt.subplots()
         ax.imshow(df_wc)
         st.pyplot(fig)

        #most common users

         most_common_df = helper.most_common_words(selected_user, df)
         fig,ax = plt.subplots()
         ax.barh(most_common_df[0],most_common_df[1])
         plt.xticks(rotation='vertical')
         st.title("Most Common Words")
         st.pyplot(fig)

        # #Emoji analysis
        #  emoji_df = helper.emoji(selected_user, df)
        #  fig,ax = plt.subplots()
        #  ax.pie(emoji_df.values, labels=emoji_df.index, autopct="%0.2f%%")
        #  st.pyplot(fig)