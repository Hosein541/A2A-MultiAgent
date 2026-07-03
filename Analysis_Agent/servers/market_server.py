from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
import yfinance as yf

mcp = FastMCP("Market Server")


class MarketData(BaseModel):
    symbol: str
    company: str
    current_price: float | None
    currency: str | None
    previous_close: float | None
    open: float | None
    day_high: float | None
    day_low: float | None
    volume: int | None
    market_cap: int | None


@mcp.tool()
def get_market_data(symbol: str) -> MarketData:
    """
    Retrieve the latest market information for a financial asset.
    
    Use this tool when the user asks for the current price or market statistics of
    stocks, ETFs, cryptocurrencies, commodities, or market indices.
    
    Examples:
    - What is the current price of Apple?
    - How much is Bitcoin worth?
    - Show today's Gold price.
    """

    ticker = yf.Ticker(symbol)
    info = ticker.info

    return MarketData(
        symbol=symbol.upper(),
        company=info.get("longName", ""),
        current_price=info.get("currentPrice"),
        currency=info.get("currency"),
        previous_close=info.get("previousClose"),
        open=info.get("open"),
        day_high=info.get("dayHigh"),
        day_low=info.get("dayLow"),
        volume=info.get("volume"),
        market_cap=info.get("marketCap"),
    )


@mcp.tool()
def get_historical_data(
    symbol: str,
    period: str = "1mo",
    interval: str = "1d",
) -> list[dict]:
    """
    Retrieve historical market data for a financial asset.

    Use this tool when the user asks about past prices, trends, or historical
    performance over a specified period.

    Examples:
    - Show Tesla prices over the last month.
    - Bitcoin price history for the last week.
    - Apple stock during the past year.


    IMPORTANT:
    
    If the ticker symbol is unknown, first call search_symbol().
    """

    ticker = yf.Ticker(symbol)

    history = ticker.history(
        period=period,
        interval=interval,
    )

    history = history.reset_index()

    return [
        {
            "date": str(row["Date"]),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        }
        for _, row in history.iterrows()
    ]


@mcp.tool()
def search_symbol(query: str, max_results: int = 5) -> list[dict]:
    """
    Search for financial symbols by company name or asset name.

    Use this tool when the ticker symbol is unknown or ambiguous.

    Examples:
    - Apple
    - Tesla
    - Bitcoin
    - Gold
    """

    search = yf.Search(query)
    quotes = search.quotes[:max_results]

    return [
        {
            "symbol": q.get("symbol"),
            "name": q.get("shortname") or q.get("longname"),
            "exchange": q.get("exchange"),
            "type": q.get("quoteType"),
        }
        for q in quotes
    ]


if __name__ == "__main__":
    mcp.run()