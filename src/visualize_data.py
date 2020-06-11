import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff

class VisualizeData(object):

    def create_export(self, file_name):
        df = pd.read_csv(file_name)

        df['datetime'] = pd.to_datetime(df['date_iso'])
        df_sample = df[['datetime','name','temperature','light','battery','moisture','conductivity']].resample(rule='15Min', on='datetime').mean().dropna()
        df = df_sample.reset_index()
        fig = make_subplots(
            rows=3, cols=2,
            shared_xaxes=True,
            vertical_spacing=0.15,
            specs=[[{"type": "scatter"},
                {"type": "scatter"}],
                [{"type": "scatter"},
                {"type": "scatter"}],
                [{"type": "table","colspan": 2}, None]],
                subplot_titles=("Temperatur","Licht", "Feuchtigkeit","Leitfähigkeit", "Zusammenfassung"),
                horizontal_spacing = 0.05
        )

        fig = self.create_scatter_trace(df, fig, 'temperature', 'Temperatur', 1, 1)
        fig = self.create_scatter_trace(df, fig, 'moisture', 'Feuchtigkeit', 1, 2)
        fig = self.create_scatter_trace(df, fig, 'light', 'Licht', 2, 1)
        fig = self.create_scatter_trace(df, fig, 'conductivity', 'Leitfähigkeit', 2, 2)

        # fig.add_trace(
        #     go.Scatter(x=df['datetime'], y=df['battery'],name='Batterie Ladung'),
        #     row=3, col=1
        # )
        decimals = 2
        df = df.sort_values(by='datetime', ascending=False).head(5)
        fig.add_trace(
            go.Table(
            header=dict(values=['Datum','Leitfähigkeit(us/cm)', 'Lichtstärke (Lux)', 'Feuchtigkeit (%)', 'Temperatur (C°)', 'Batterie Ladung (%)'],
                        align='left'),
            cells=dict(values=[df.datetime, df.conductivity.apply(lambda x: round(x, decimals)), df.light.apply(lambda x: round(x, decimals)), df.moisture*100, df.temperature.apply(lambda x: round(x, decimals)), df.battery],
                    align='left')),
                    row=3, col=1
        )
            # go.Table(df['datetime'],name='Zusammenfassung letzte 24h'),
            # row=3, col=2


        fig.update_layout(template='plotly_dark', showlegend=False)
        fig.update_layout(title='Messwerte Pflanzsensoren')
        #fig.show()
        pio.write_html(fig, file='output/html/charts.html')


    def create_scatter_trace(self, df, fig, y, name, row, col):
        fig.add_trace(
            go.Scatter(x=df['datetime'], y=df[y],name=name),
            row=row, col=col
        )
        return fig

if __name__ == '__main__':
    vd = VisualizeData()
    vd.create_export('output/sensor_data.csv')