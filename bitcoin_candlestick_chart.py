import pandas as pd
import plotly.graph_objects as go
from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()
bitcoin_data = cg.get_coin_market_chart_by_id(id="bitcoin", vs_currency="usd", days=30)
bitcoin_price_data = bitcoin_data["prices"]
data = pd.DataFrame(bitcoin_price_data, columns=["TimeStamp", "Price"])
data["Date"] = pd.to_datetime(data["TimeStamp"], unit="ms")
candlestick_data = data.groupby(data.Date.dt.date).agg(
    {"Price": ["min", "max", "first", "last"]}
)
fig = go.Figure(
    data=[
        go.Candlestick(
            x=candlestick_data.index,
            open=candlestick_data["Price"]["first"],
            high=candlestick_data["Price"]["max"],
            low=candlestick_data["Price"]["min"],
            close=candlestick_data["Price"]["last"],
        )
    ]
)
# Convert the DataFrame to a tuple of its values for hashing
candlestick_data_tuple = tuple(candlestick_data.itertuples(index=False))
# Calculate a hash for the tuple
candlestick_data_hash = hash(candlestick_data_tuple)

candlestick_figure_dict = {candlestick_data_hash: fig}

fig.update_layout(
    xaxis_rangeslider_visible=False,
    xaxis_title="Date",
    yaxis_title="Price(USD $)",
    title="Bitcoin Candlestick Chart Over Past 30 Days",
)
# fig.show()// this is another way, display the screen without create the file
fig.write_html("bitcoin_candlestick_graph.html")
