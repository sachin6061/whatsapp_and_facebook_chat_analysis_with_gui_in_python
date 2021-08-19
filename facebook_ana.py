import json
# import emoji
import plotly.graph_objs as go
import pandas as pd


class facebook_data:
    def __init__(self):
        self.top = 10
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

    def read_file(self, path):
        with open(path) as file:
            chat_hist = json.load(file)
        self.df = pd.DataFrame(chat_hist['messages'])
        self.df["Date"] = pd.to_datetime(self.df["timestamp_ms"])
        # print(self.df["Date"].head(150))
        self.df['Year'] = self.df.Date.map(lambda x: x.year)
        self.df['Month'] = self.df.Date.map(lambda x: x.month)
        self.df['Month_Name'] = self.df.Date.map(lambda x: x.month_name())
        self.df['Day'] = self.df.Date.map(lambda x: x.day)
        self.df['Day_Number'] = self.df.Date.map(lambda x: x.isoweekday())
        self.df['Day_Of_Week'] = self.df.Date.map(lambda x: x.day_name())
        self.df['Time'] = [d.time() for d in self.df['Date']]
        self.df['Hour'] = self.df.Time.map(lambda x: x.hour)
        self.df['Mins'] = self.df.Time.map(lambda x: x.minute)
        self.df=self.df.rename(columns={'sender_name': "Author"})
        self.df=self.df.rename(columns={'content': 'Message'})
        # self.df.dropna(inplace=True, axis=0)
        # print(self.df['Day'].head(10))

    def list_of_years(self):
        self.progress = self.df.copy()
        ls_years = list((self.progress.groupby('Year').groups.keys()))
        return ls_years

    def find_top_most_active(self):
        self.messages_data_frame = self.df.groupby('Author').count().iloc[:, 1:2].rename(
            columns={'Message': "Total_Messages"})
        return self.messages_data_frame.sort_values('Total_Messages', ascending=False).head(self.top)

    def find_top_5_photos(self):
        self.df_with_media = self.df[['Author', 'photos']].copy()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().rename(
            columns={'photos': "Total_Photos"})
        return self.medias_data_frame.sort_values('Total_Photos', ascending=False).head(self.top)

    def find_top_5_sticker(self):
        self.df_with_media = self.df[['Author', 'sticker']].copy()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().rename(
            columns={'sticker': "Total_sticker"})
        return self.medias_data_frame.sort_values('Total_sticker', ascending=False).head(self.top)

    def find_top_5_reactions(self):
        self.df_with_media = self.df[['Author', 'reactions']].copy()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().rename(
            columns={'reactions': "Total_reactions"})
        return self.medias_data_frame.sort_values('Total_reactions', ascending=False).head(self.top)

    def find_top_5_videos(self):
        self.df_with_media = self.df[['Author', 'videos']].copy()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().rename(
            columns={'videos': "Total_videos"})
        return self.medias_data_frame.sort_values('Total_videos', ascending=False).head(self.top)

    def find_top_5_gifs(self):
        self.df_with_media = self.df[['Author', 'gifs']].copy()

        self.medias_data_frame = self.df_with_media.groupby('Author').count().sort_index().rename(
            columns={'gifs': "Total_gifs"})
        return self.medias_data_frame.sort_values('Total_gifs', ascending=False).head(self.top)

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
        fig.write_image('faclinechartpermonth.png')

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
        fig.write_image('facbarchartpermonth.png')

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
            yaxis=self.axis_style,
            margin=self.margin_style,
            plot_bgcolor='white',
        )
        fig.write_image('facactivedaysmonth.png')

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
        fig.write_image('facactivehoursmonth.png')
