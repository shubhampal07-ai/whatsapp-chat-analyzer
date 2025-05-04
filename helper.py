from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    num_media_messages = df[df['user_message'] == '<Media omitted>'].shape[0]
    links = []
    for message in df['user_message']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index':'name', 'user':'percent'})
    return x, df_percent

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user_message'] != '<Media omitted>']
    temp = temp[temp['user_message'] != 'group_notification']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(' '.join(temp['user_message']))

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user_message'] != '<Media omitted>']
    temp = temp[temp['user_message'] != 'group_notification']

    words = []

    for message in temp['user_message']:
        for word in message.lower().split():
            words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    most_common_df.columns = ['word', 'count']
    return most_common_df

import pandas as pd
import emoji
from collections import Counter

import pandas as pd
import emoji
import regex
from collections import Counter

def extract_emojis(s):
    return [c for c in regex.findall(r'\X', s) if any(char in emoji.EMOJI_DATA for char in c)]

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['user_message']:
        emojis.extend(extract_emojis(message))

    if not emojis:
        return pd.DataFrame(columns=['emoji', 'count'])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['emoji', 'count'])
    return emoji_df

def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['user_message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date').count()['user_message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='hour', values='user_message', aggfunc='count').fillna(0)
    return user_heatmap
