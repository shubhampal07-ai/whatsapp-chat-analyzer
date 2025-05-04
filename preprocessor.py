import re
import pandas as pd

def preprocess(data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}) - (.+?): (.+)'
    messages = []
    dates = []
    users = []

    matches = re.findall(pattern, data)
    for match in matches:
        date_str = match[0] + ", " + match[1]
        dates.append(date_str)
        users.append(match[2])
        messages.append(match[3])

    df = pd.DataFrame({'user_message': messages, 'user': users, 'message_date': dates})

    # Clean date
    df['message_date'] = df['message_date'].str.strip()
    df['date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %H:%M', errors='coerce')
    df = df.dropna(subset=['date']).reset_index(drop=True)

    # Extract features
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
