# ui/components/charts.py
import flet as ft
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class OHLCChart(ft.UserControl):
    def __init__(self, width=800, height=400):
        super().__init__()
        self.width = width
        self.height = height

    def build(self):
        # Создаем заглушку для графика
        self.chart_container = ft.Container(
            width=self.width,
            height=self.height,
            border=ft.border.all(1, ft.Colors.OUTLINE),
            border_radius=5,
            alignment=ft.alignment.center,
            content=ft.Text("График будет здесь", size=16)
        )
        return self.chart_container

    def update_chart(self, ohlc_data):
        """Обновить график OHLC данными"""
        if not ohlc_data:
            return

        # Создаем график Plotly
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data['timestamp'],
            open=ohlc_data['open'],
            high=ohlc_data['high'],
            low=ohlc_data['low'],
            close=ohlc_data['close']
        )])

        fig.update_layout(
            title="Ценовой график",
            yaxis_title="Цена",
            xaxis_title="Время",
            template="plotly_dark",
            height=self.height,
            width=self.width
        )

        # Конвертируем в изображение (в реальном проекте нужно использовать plotly.io)
        # Здесь упрощенная версия

        self.chart_container.content = ft.Image(
            src_base64=self.fig_to_base64(fig),
            width=self.width,
            height=self.height,
            fit=ft.ImageFit.CONTAIN
        )
        self.update()

    def fig_to_base64(self, fig):
        """Конвертация графика в base64"""
        import io
        import base64

        buf = io.BytesIO()
        fig.write_image(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode()
        return f"data:image/png;base64,{img_str}"
