import dlt
import pandas as pd
from io import StringIO
import yfinance as yf
 

@dlt.source
def y_finance_source():
    return extract_historical_data()


@dlt.resource(    
        table_name="stock_price_history",
        write_disposition="replace")
def extract_historical_data():

    list_tickers = ['hd' ,'low' ,'spy'] 
    data = yf.download(list_tickers,interval='1d',period="10y")
    yield data


if __name__ == "__main__":
    # specify the pipeline name, destination and dataset name when configuring pipeline,
    # otherwise the defaults will be used that are derived from the current script name
    pipeline = dlt.pipeline(
        pipeline_name='stock_prices',
        destination='bigquery',
        dataset_name='stock_prices_data',
    )

    # run the pipeline with your parameters
    load_info = pipeline.run(extract_historical_data)
    row_counts = pipeline.last_trace.last_normalize_info

    print(row_counts)
    print("------")
    print(load_info)
