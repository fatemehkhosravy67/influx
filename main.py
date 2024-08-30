from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os

load_dotenv()

# connect to InfluxDB
url = os.getenv("INFLUXDB_URL")
token = os.getenv("INFLUXDB_TOKEN")
org = os.getenv("INFLUXDB_ORG")



# CREATE InfluxDB

# InfluxDB Connection Manager Class
class InfluxDBManager:
    def __init__(self):
        self.client = None

    def __enter__(self):
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org
        )
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()


app = FastAPI()


class DataPoint(BaseModel):
    bucket: str = 'FATEMEH_BUCKET'
    measurement: str
    location: str
    temperature: float


@app.post("/write")
async def write_data(point: DataPoint):
    try:
        with InfluxDBManager() as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            p = influxdb_client.Point(point.measurement).tag("location", point.location).field("temperature",
                                                                                               point.temperature)
            write_api.write(bucket=point.bucket, org=org, record=p)
            return {"message": "Data written successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/latest")
async def get_latest_value(bucket: str, measurement: str):
    try:
        with InfluxDBManager() as client:
            query_api = client.query_api()

            query = f'''
            from(bucket: "{bucket}")
                |> range(start: -10m)
                |> filter(fn: (r) => r._measurement == "{measurement}")
                |> sort(columns: ["_time"], desc: true)
                |> limit(n: 1)
            '''

            tables = query_api.query(query=query, org=org)

            if tables and tables[0].records:
                latest_record = tables[0].records[0]
                return {
                    "time": latest_record.get_time(),
                    "value": latest_record.get_value(),
                    "location": latest_record.values.get("location"),
                    "field": latest_record.get_field()
                }
            else:
                return {"message": "No data found"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
