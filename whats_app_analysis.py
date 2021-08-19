import re
import pandas as pd
import emoji
from collections import defaultdict
import plotly.graph_objs as go


# %matplotlib inline
class whatsapp_grp:
    def __init__(self):
        self.margin_style = dict(l=100, r=20, t=110, )
        self.axis_style = dict(
            fixedrange=True,
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
            tickfont=dict(family='Arial', size=12, color='rgb(82, 82, 82)', )
        )
        self.pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
        self.parsedData = []
        self.top = 10

    def startsWithDateAndTimeAndroid(self, s):
        result = re.match(self.pattern, s)
        if result:
            return True
        return False

    def FindAuthor(self, s):
        s = s.split(":")
        if len(s) == 2:
            return True
        else:
            return False

    def getDataPointAndroid(self, line):
        splitLine = line.split(' - ')
        dateTime = splitLine[0]
        date, time = dateTime.split(', ')
        message = ' '.join(splitLine[1:])
        if self.FindAuthor(message):
            splitMessage = message.split(':')
            author = splitMessage[0]
            message = ' '.join(splitMessage[1:])
        else:
            author = None
        return date, time, author, message

    def getDataPointios(self, line):
        splitLine = line.split('] ')
        dateTime = splitLine[0]
        if ',' in dateTime:
            date, time = dateTime.split(',')
        else:
            date, time = dateTime.split(' ')
        message = ' '.join(splitLine[1:])
        if self.FindAuthor(message):
            splitMessage = message.split(':')
            author = splitMessage[0]
            message = ' '.join(splitMessage[1:])
        else:
            author = None
        if time[5] == ":":
            time = time[:5] + time[-3:]
        else:
            if 'AM' in time or 'PM' in time:
                time = time[:6] + time[-3:]
            else:
                time = time[:6]
        return date, time, author, message

    def split_count(self, text):
        text = emoji.demojize(text)
        text = re.findall(r'(:[^:]*:)', text)
        list_emoji = [emoji.emojize(x) for x in text]
        return list_emoji

    # List to keep track of data so it can be used by a Pandas dataframe

    def startsWithDateAndTimeios(line):
        pass

    def read_file(self, path):
        with open(path, encoding="utf-8") as fp:
            device = ''
            first = fp.readline()
            if '[' in first:
                device = 'ios'
            else:
                device = "android"
            messageBuffer = []
            date, time, author = None, None, None  # message contains 4 things-"date","time","author","message"
            while True:
                line = fp.readline()

                if not line:
                    break
                else:
                    line = line.strip()
                    if self.startsWithDateAndTimeAndroid(line):
                        if len(messageBuffer) > 0:
                            self.parsedData.append([date, time, author, ' '.join(messageBuffer)])
                        messageBuffer.clear()
                        date, time, author, message = self.getDataPointAndroid(line)
                        messageBuffer.append(message)
                    else:
                        messageBuffer.append(line)
            if device == 'android':
                self.df = pd.DataFrame(self.parsedData, columns=['Date', 'Time', 'Author', 'Message'])
                self.df["Date"] = pd.to_datetime(self.df["Date"])
                self.df["Time"] = pd.to_datetime(self.df["Time"])
                self.df['Year'] = self.df.Date.map(lambda x: x.year)
                self.df['Month'] = self.df.Date.map(lambda x: x.month)
                self.df['Month_Name'] = self.df.Date.map(lambda x: x.month_name())
                self.df['Day'] = self.df.Date.map(lambda x: x.day)
                self.df['Day_Number'] = self.df.Date.map(lambda x: x.isoweekday())
                self.df['Day_Of_Week'] = self.df.Date.map(lambda x: x.day_name())
                self.df['Hour'] = self.df.Time.map(lambda x: x.hour)
                self.df['Mins'] = self.df.Time.map(lambda x: x.minute)
                self.df.dropna(inplace=True, axis=0)
                # print(self.df)

    def find_top_most_active(self):
        self.messages_data_frame = self.df.groupby('Author').count().iloc[:, 1:2].rename(
            columns={'Time': "Total_Messages"})
        return self.messages_data_frame.sort_values('Total_Messages', ascending=False).head(self.top)
        # inplace=True

    def find_top_5_media(self):
        self.df_with_media = self.df[['Date', 'Author', 'Message']].copy()
        self.df_with_media['Message'] = self.df_with_media.Message.map(
            lambda x: "Media is present" if ("<Media omitted>" in x) else "No Media")
        # df_with_media.drop(df_with_media[df_with_media.Message=='No Media'], axis=1, inplace=True)
        self.df_with_media = self.df_with_media[self.df_with_media.Message == 'Media is present'].reset_index(drop=True)
        self.df_with_media.dropna()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().iloc[:, 1:2].rename(
            columns={'Message': "Total_Medias"})
        return self.medias_data_frame.sort_values('Total_Medias', ascending=False).head(self.top)

    def find_top_links(self):
        self.df_without_media = self.df[['Date', 'Author', 'Message']].copy()
        self.df_without_media['Message'] = self.df_without_media.Message.map(
            lambda x: x if "<Media omitted>" not in x else None)
        self.df_without_media = self.df_without_media.dropna().reset_index(drop=True)
        # df_without_media.head(5)
        self.ls_msg = self.df_without_media.Message.tolist()
        ls_link = []
        for msg in self.ls_msg:
            links = re.findall(r'(https?://\S+)', msg)
            for link in links:
                ls_link.append(re.findall("^https?://([\w.]*)/", link))
        link_df = pd.DataFrame(ls_link).replace(
            {"youtu.be": "www.youtube.com", "instagram.com": "www.instagram.com"}).rename(
            columns={0: 'Overall links'})
        overall_link_df = pd.DataFrame(
            link_df.groupby("Overall links")['Overall links'].count()).rename(
            columns={'Overall links': 'Total_Count'}).sort_values("Total_Count",
                                                                  ascending=False)  # .total.sum()
        return overall_link_df.head(self.top)

    def link_send_by_author(self):
        ls_authors = self.df_without_media.Author.unique().tolist()
        dic_links_authors_df = {}
        for author in ls_authors:
            ls_msg = self.df_without_media[['Author', 'Message']][
                self.df_without_media.Author == author].Message.tolist()
            ls_link = []
            for msg in ls_msg:
                links = re.findall(r'(https?://\S+)', msg)
                for link in links:
                    ls_link.append(re.findall("(https?://\S+)", link))
            if len(ls_link) > 0:
                link_df = pd.DataFrame(ls_link).rename(columns={0: 'Links'})
                link_df = pd.DataFrame(link_df.groupby("Links").Links.count()).rename(columns={'Links': 'Total_Count'}) \
                    .sort_values("Total_Count", ascending=False).reset_index().rename(
                    columns={"Links": "Links sent by " + author})
                dic_links_authors_df[author] = link_df
        ls_links_author = []
        ls_total_count = []
        for i in dic_links_authors_df:
            ls_links_author.append(i)
            ls_total_count.append(dic_links_authors_df[i].Total_Count.sum())
        self.links_data_frame = pd.DataFrame([ls_links_author, ls_total_count]).T.rename(
            columns={0: 'Author', 1: 'Total_Links'}).set_index('Author').sort_index()
        return self.links_data_frame.sort_values('Total_Links', ascending=False).head(self.top)

    def find_top_5_emoji(self):
        df_without_media = self.df[['Date', 'Author', 'Message']].copy()
        df_without_media['Message'] = df_without_media.Message.map(lambda x: x if "<Media omitted>" not in x else None)
        df_without_media = df_without_media.dropna().reset_index(drop=True)
        str_without_media = ' '.join(df_without_media.Message)
        emoji_list = [i['emoji'] for i in emoji.emoji_lis(str_without_media)]

        default_emoji = defaultdict(int)
        for i in emoji_list:
            default_emoji[i] += 1
        emoji_df = pd.DataFrame([default_emoji.keys(), default_emoji.values()]).T.rename(
            columns={0: 'Emoji', 1: 'Total_Count'}).sort_values(['Total_Count'], ascending=False).set_index('Emoji')
        # emoji_df['Name'] = emoji_df.index.map(lambda x: ' '.join(emoji.demojize(x).strip(":").split("_"))).tolist()
        #
        # emoji_df['Name'] = emoji_df.Name.map(lambda x: x if not (x.endswith('tone') or x.startswith('regional') or (
        #         (x.startswith('male') or x.startswith('female')) and x.endswith('sign'))) else None)  # .dropna()
        # emoji_df.dropna(inplace=True)

        overall_emoji_df = emoji_df
        return overall_emoji_df.head(self.top)

    def top5mostemojiuser(self):
        self.df_without_media = self.df[['Date', 'Author', 'Message']].copy()
        self.df_without_media['Message'] = self.df_without_media.Message.map(
            lambda x: x if "<Media omitted>" not in x else None)
        self.df_without_media = self.df_without_media.dropna().reset_index(drop=True)
        ls_author = self.df_without_media.Author.unique().tolist()
        dic_author_str_without_media = {}  # dictionary of message string per person
        dic_author_default_emoji = {}  # dictionary default dic
        dic_author_emoji_df = {}  # dictionary of data frames per emoji author
        for author in ls_author:
            str_without_media = ' '.join(
                self.df_without_media[['Author', 'Message']][self.df_without_media.Author == author].Message)
            dic_author_str_without_media[author] = str_without_media

            dic_author_emoji = [emo['emoji'] for emo in emoji.emoji_lis(str_without_media)]
            default_emoji = defaultdict(int)
            for emo in dic_author_emoji:
                default_emoji[emo] += 1

            dic_author_default_emoji[author] = dict(default_emoji)
            self.emoji_df = pd.DataFrame(
                [dic_author_default_emoji[author].keys(), dic_author_default_emoji[author].values()]).T \
                .rename(columns={0: 'Emojis used by ' + author, 1: "Total_Count"}).sort_values('Total_Count',
                                                                                               ascending=False).set_index(
                'Emojis used by ' + author)
            self.emoji_df['Name'] = self.emoji_df.index.map(
                lambda x: ' '.join(emoji.demojize(x).strip(":").split("_"))).tolist()
            self.emoji_df['Name'] = self.emoji_df.Name.map(
                lambda x: x if not (x.endswith('tone') or x.startswith('regional') or \
                                    ((x.startswith('male') or x.startswith('female')) \
                                     and x.endswith('sign'))) else None)  # .dropna()
            self.emoji_df.dropna(inplace=True)
            dic_author_emoji_df[author] = self.emoji_df

        ls_emoji_author = []
        ls_total_count = []
        for i in dic_author_emoji_df:
            ls_emoji_author.append(i)
            ls_total_count.append(dic_author_emoji_df[i].Total_Count.sum())
        self.emojis_data_frame = pd.DataFrame([ls_emoji_author, ls_total_count]).T.rename(
            columns={0: 'Author', 1: 'Total_Emojis'}).set_index('Author').sort_index()
        return self.emojis_data_frame.sort_values('Total_Emojis', ascending=False).head(self.top)

    def chart_data(self):
        selected_sort_columns = ['Total_Messages', 'Total_Medias', 'Total_Emojis', 'Total_Links']

        chat_analysis_data_frame = pd.concat(
            [self.links_data_frame, self.emojis_data_frame, self.medias_data_frame, self.messages_data_frame],
            axis=1).fillna(0)
        chat_analysis_data_frame.Total_Links = chat_analysis_data_frame.Total_Links.astype(int)
        # chat_analysis_data_frame.Total_Unique_Words = chat_analysis_data_frame.Total_Unique_Words.astype(int)
        # chat_analysis_data_frame.Total_Words = chat_analysis_data_frame.Total_Words.astype(int)
        chat_analysis_data_frame.Total_Emojis = chat_analysis_data_frame.Total_Emojis.astype(int)
        chat_analysis_data_frame.Total_Medias = chat_analysis_data_frame.Total_Medias.astype(int)
        chat_analysis_data_frame.Total_Messages = chat_analysis_data_frame.Total_Messages.astype(int)
        return chat_analysis_data_frame.sort_values(selected_sort_columns, ascending=False)[selected_sort_columns].head(
            50)

    def list_of_years(self):
        self.progress = self.df.copy()
        ls_years = list((self.progress.groupby('Year').groups.keys()))
        return ls_years

    def chart(self):
        self.progress = self.df.copy()
        ls_years = list((self.progress.groupby('Year').groups.keys()))
        ls_years.append('All')
        self.selected_year = ls_years[0]

        ls_years_df = []
        for i in ls_years[:-1]:
            monthly_progress = self.progress[self.progress.Year == i]
            ls_years_df.append(monthly_progress)

        ls_years_df.append(self.progress)

        OverAll_month_series = self.progress[['Month', 'Month_Name', 'Message']].groupby(
            ['Month', 'Month_Name']).count()

        ls_data = []

        counter = 0
        for year_df in ls_years_df[:-1]:
            dict_month = {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 'July': 0,
                          'August': 0, 'September': 0, 'October': 0, 'November': 0, 'December': 0}
            year_df = year_df[['Month', 'Month_Name', 'Message']].groupby(['Month', 'Month_Name']).count()
            index = year_df.index.get_level_values(1).tolist()
            value = year_df.Message.tolist()
            for i in range(len(index)):
                dict_month[index[i]] = value[i]

            ls_data.append(go.Scatter(x=list(dict_month.keys()), y=list(dict_month.values()),
                                      mode='lines+markers', marker=dict(size=1, line={'width': 2}),
                                      name=ls_years[counter]))
            counter += 1

        dict_month = {'January': 0, 'February': 0, 'March': 0, 'April': 0, 'May': 0, 'June': 0, 'July': 0, 'August': 0,
                      'September': 0, 'October': 0, 'November': 0, 'December': 0}

        index = OverAll_month_series.index.get_level_values(1).tolist()
        value = OverAll_month_series.Message.tolist()
        for i in range(len(index)):
            dict_month[index[i]] = value[i]

        ls_data.append(go.Scatter(x=list(dict_month.keys()), y=list(dict_month.values()),
                                  mode='lines+markers', marker=dict(size=1, line={'width': 2}), name="Overall",
                                  ))

        fig = go.Figure(data=ls_data)

        ls_buttons = [dict(label="Show All",
                           method="update",
                           args=[{"visible": True},
                                 {"title": "Analysis of Total Group Messages per Month"},
                                 ])]
        ls_true_false = [False] * len(ls_years)
        for i in range(len(ls_years)):
            ls_true_false[i] = True
            ls_buttons.append(dict(label=ls_years[i],
                                   method="update",
                                   args=[{"visible": ls_true_false},
                                         {"title": "Total Group Messages per month for the year {}".format(
                                             ls_years[i])}]))
            ls_true_false = [False] * len(ls_years)

        fig.update_layout(
            title_text="Analysis of Total Group Messages per Month",
            hovermode='x',
            xaxis_title="Months",
            yaxis_title="Total Number of messages",
            xaxis=self.axis_style,
            yaxis=self.axis_style,
            margin=self.margin_style,
            showlegend=True,
            plot_bgcolor='white')
        # )
        # pyo.plot(fig, filename='progress_byYear_chart.html')
        fig.write_image('linechartpermonth.png')

    def charts(self, selected_year):
        if selected_year != 'All':
            TotalMessages = self.progress.loc[self.progress.Year == int(selected_year)].groupby(
                'Author').count().rename(
                columns={'Message': "Total_Messages"}).sort_values('Total_Messages', ascending=False)
            TotalMessages['Percentage_Total'] = round(
                (TotalMessages.Total_Messages / TotalMessages.Total_Messages.sum() * 100), 2)
        else:
            TotalMessages = self.progress.groupby('Author').count().rename(
                columns={'Message': "Total_Messages"}).sort_values('Total_Messages', ascending=False)
            TotalMessages['Percentage_Total'] = round(
                (TotalMessages.Total_Messages / TotalMessages.Total_Messages.sum() * 100), 2)
        data = [
            go.Bar(x=TotalMessages.index, y=TotalMessages.Total_Messages, name='', customdata=TotalMessages,
                   hovertemplate='%{x}<br>' +
                                 'Total Messages = %{y}<br>' +
                                 'Percentage of Total Messages = %{customdata[1]}%',
                   text=TotalMessages.Total_Messages, textposition='outside',
                   )
        ]

        fig = go.Figure(data=data)

        fig.update_layout(
            title_text='Total Number of messages for the year {}'.format(selected_year),
            xaxis_title="Members",
            yaxis_title="Total Number of messages",
            xaxis=self.axis_style,
            yaxis=self.axis_style,
            margin=self.margin_style,
            plot_bgcolor='white',
        )

        ls_colours = []
        for i in range(len(TotalMessages)):
            ls_colours.append("rgb" + str((51 + i * 6, 190, 57 + i * 6)))

        fig.update_traces(
            marker={"color": "#ffcd36", }, opacity=0.8
        )
        fig.write_image('barchartpermonth.png')

    def active_days(self, selected_year):
        self.progress = self.df.copy()
        year_date_series = self.progress[['Year', 'Day', 'Message']].groupby(['Year', 'Day']).count().Message
        OverAll_date_series = self.progress[['Day', 'Message']].groupby('Day').count().Message

        ls_years = list((self.progress.groupby('Year').groups.keys()))
        ls_years.append('All')

        data = []
        for i in ls_years[:-1]:
            data.append(
                go.Bar(x=year_date_series.get(i).index.tolist(), y=year_date_series.get(i).values.tolist(), name='',
                       hovertemplate='          Day = %{x}<br>' +
                                     'Total Messages = %{y}<br>',
                       text=['{:,}'.format(i) for i in year_date_series.get(i).values.tolist()],
                       textposition='outside', ))
        x_axis, y_axis = OverAll_date_series.index.tolist(), OverAll_date_series.values.tolist()
        data.append(
            go.Bar(x=x_axis, y=y_axis, name='',
                   hovertemplate='          Day = %{x}<br>' +
                                 'Total Messages = %{y}<br>',
                   text=['{:,}'.format(i) for i in y_axis], textposition='outside',
                   )
        )

        fig = go.Figure(data=data[ls_years.index(selected_year)])

        fig.update_layout(
            title_text='Activity on Days of the month for the year {}'.format(selected_year),
            xaxis_title="Days of the month",
            yaxis_title="Total Number of messages",
            xaxis={**self.axis_style, **{'tick0': 0, 'dtick': 1}},
            # this tick0 sys show the starting tick and dtick says next tick,
            # if dtick was 2, then it wouold show alternate ticks
            yaxis=self.axis_style,
            margin=self.margin_style,
            plot_bgcolor='white',
        )
        fig.write_image('activedaysmonth.png')

    def active_hours(self, selected_year):
        year_hour_series = self.progress[['Year', 'Hour', 'Message']].groupby(['Year', 'Hour']).count().Message
        OverAll_hour_series = self.progress[['Hour', 'Message']].groupby('Hour').count().Message

        data = []
        ls_years = list((self.progress.groupby('Year').groups.keys()))
        ls_years.append('All')
        for i in ls_years[:-1]:
            data.append(
                go.Bar(x=year_hour_series.get(i).index.tolist(), y=year_hour_series.get(i).values.tolist(), name='',
                       hovertemplate='          Hour = %{x}<br>' +
                                     'Total Messages = %{y}<br>',
                       text=['{:,}'.format(i) for i in year_hour_series.get(i).values.tolist()],
                       textposition='outside', ))
        x_axis, y_axis = OverAll_hour_series.index.tolist(), OverAll_hour_series.values.tolist()
        data.append(
            go.Bar(x=x_axis, y=y_axis, name='',
                   hovertemplate='          Hour = %{x_axis}<br>' +
                                 'Total Messages = %{y_axis}<br>',
                   text=['{:,}'.format(i) for i in y_axis], textposition='outside',
                   )
        )

        fig = go.Figure(data=data[ls_years.index(selected_year)])
        fig.update_layout(
            hoverlabel=dict(bgcolor='white', bordercolor='grey'),
            title_text='Hourly Activity for the year {}'.format(selected_year),
            xaxis_title="Hours 12:00 A.M to 11:00 PM",
            yaxis_title="Total Number of messages",
            xaxis={**{'tick0': 0, 'dtick': 1}, **self.axis_style},
            yaxis=self.axis_style,
            margin=self.margin_style,
            plot_bgcolor='white',
        )
        fig.write_image('activehoursmonth.png')


# a = whatsapp_grp()
# a.read_file('C:/Users/Admin/Downloads/group_chat.txt')
# print(a.find_top_most_active())
# print(a.find_top_5_media())
# print(a.find_top_links())
# print(a.link_send_by_author())
# # print(a.find_top_5_emoji())
