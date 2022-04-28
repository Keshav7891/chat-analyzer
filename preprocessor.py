import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]  # List to store the messages and removes the initial empty string

    dates = re.findall(pattern, data)  # List to store all dates

    # Creating Pandas Data Frame of user message and date
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # Converting date to date and type format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%Y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)


    # Seperate Message and User

    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # if its a single user
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # if its a group message
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    #Extract only_days
    df['only_date'] = df['date'].dt.date

    # Extract Year
    df['year'] = df['date'].dt.year

    #Extract month number
    df['month_num'] = df['date'].dt.month

    # Extract Month
    df['month'] = df['date'].dt.month_name()

    # Extract Day
    df['day'] = df['date'].dt.day

    #Ectract day_name
    df['day_name'] = df['date'].dt.day_name()

    # Extract Hour
    df['hour'] = df['date'].dt.hour

    # Extract minute
    df['minute'] = df['date'].dt.minute


    #extract hour-activity
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df