from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from candlesticks import create_data_stock, get_ticker_info, get_candlestick_patterns


DEBUG_MODE = True # change when in production/commited to some virtual machine
app = FastAPI(debug=DEBUG_MODE)

# Allowing all middleware is optional, but good practice for dev purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Candlestick API, man"}


# @app.get("/ticker_info")
# def get_ticker_info(ticker: str, start_date: str, end_date: str):
#     return {}

# @app.get("/patterns/charts")
# def get_list_of_charts_patterns(ticker: str, start_date: str, end_date: str):
#     return {}


# @app.get("/patterns/candlestick/{type}/{ticker}")
# def get_candlestick_data(type: str, ticker: str, start_date: str, end_date: str):
#     return {}

@app.get("/candlestick/{ticker}/{start_date}/{end_date}")
def get_candlestick_data(ticker: str, start_date: str, end_date: str):
    data = create_data_stock(ticker=ticker, start_date=start_date, end_date=end_date)
    print(data.keys())
    data['Date'] = data.Date.astype(str)
    return {'data': list(data.apply(dict, axis=1))}

# @app.get("/internal/")
# @app.post("/store")
# def store_data(data: dict):
#     # Store the received data (candlestick patterns and graphs) in your storage system
#     # You can use Prefect to manage the storage and processing of this data
#     # Return a response indicating success or failure

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=DEBUG_MODE)
