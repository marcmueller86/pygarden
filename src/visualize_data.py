import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import plotly

class VisualizeData(object):

    def create_export(self, file_name):
        df = pd.read_csv(file_name)
        df['name'][5]='sensor_2'
        df['name'][15]='sensor_2'
        df['name'][19]='sensor_2'

        df['datetime'] = pd.to_datetime(df['date_iso'])
        df['datetime_rounded']=df.datetime.apply(lambda x: self.round_to_hour(x))
        df_resampled = df.groupby(by=['datetime_rounded','name'], axis=0).mean().reset_index()

        #df_sample = df[['datetime','name','temperature','light','battery','moisture','conductivity']].resample(rule='15Min', on='datetime').mean().dropna()
        df = df_resampled.reset_index()
        fig = make_subplots(
            rows=3, cols=2,
            shared_xaxes=True,
            vertical_spacing=0.15,
            specs=[[{"type": "scatter"},
                {"type": "scatter"}],
                [{"type": "scatter"},
                {"type": "scatter"}],
                [{"type": "table","colspan": 2}, None]],
                subplot_titles=("Temperatur","Feuchtigkeit", "Licht","Leitfähigkeit"),
                horizontal_spacing = 0.05
        )
        # Only a few colors, add more if you need more than 10 sensors
        cols = plotly.colors.DEFAULT_PLOTLY_COLORS

        for i, sensor in enumerate(df_resampled['name'].unique()):
            df_sensor = df[df['name'] == sensor] 
            fig = self.create_scatter_trace(cols[i], df_sensor, fig, 'temperature', sensor, 1, 1)
            fig = self.create_scatter_trace(cols[i], df_sensor, fig, 'moisture', sensor, 1, 2)
            fig = self.create_scatter_trace(cols[i], df_sensor, fig, 'light', sensor, 2, 1)
            fig = self.create_scatter_trace(cols[i], df_sensor, fig, 'conductivity', sensor, 2, 2)

        # fig.add_trace(
        #     go.Scatter(x=df['datetime'], y=df['battery'],name='Batterie Ladung'),
        #     row=3, col=1
        # )
        decimals = 2
        df = df.sort_values(by='datetime_rounded', ascending=False).head(10)
        fig.add_trace(
            go.Table(
            header=dict(values=['Sensor','Datum','Leitfähigkeit(us/cm)', 'Lichtstärke (Lux)', 'Feuchtigkeit (?%)', 'Temperatur (C°)', 'Batterie Ladung (%)'],
                        align='left'),
            cells=dict(values=[df.name, df.datetime_rounded, df.conductivity.apply(lambda x: round(x, decimals)), df.light.apply(lambda x: round(x, decimals)), df.moisture.apply(lambda x: round(x, decimals)), df.temperature.apply(lambda x: round(x, decimals)), df.battery],
                    align='left')),
                    row=3, col=1
        )
            # go.Table(df['datetime'],name='Zusammenfassung letzte 24h'),
            # row=3, col=2


        fig.update_layout(template='plotly_dark', showlegend=True)
        fig.update_layout(title='Messwerte Pflanzsensoren')
        #fig.show()
        pio.write_html(fig, file='output/html/charts.html')


    def create_scatter_trace(self, color, df, fig, y, name, row, col):
        fig.add_trace(
            go.Scatter(x=df['datetime_rounded'], y=df[y],name=name, line=dict(width=2, color=color)),
            row=row, col=col
        )
        return fig

    def round_to_hour(self, t):
        # Rounds to nearest hour by adding a timedelta hour if minute >= 30
        return (t.replace(second=0, microsecond=0, minute=0, hour=t.hour)
                    +timedelta(hours=t.minute//30))


if __name__ == '__main__':
    vd = VisualizeData()
    vd.create_export('output/sensor_data.csv')