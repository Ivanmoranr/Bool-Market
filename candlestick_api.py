from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

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
    return {"message": "Welcome to the Candlestick API"}

@app.get("/candlestick/{ticker}/{start_date}/{end_date}")
def get_candlestick_data(ticker: str, start_date: str, end_date: str):
    # Fetch and return candlestick data for the specified ticker and date range
    # You can use your existing code to fetch and process the candlestick data here
    # Return the data in JSON format

@app.post("/store")
def store_data(data: dict):
    # Store the received data (candlestick patterns and graphs) in your storage system
    # You can use Prefect to manage the storage and processing of this data
    # Return a response indicating success or failure

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
