
## FastAPI InfluxDB Project

This project is a FastAPI application that connects to an InfluxDB database. It allows you to write data points to InfluxDB and query the latest data using REST API endpoints.

### Prerequisites

To run this project, ensure you have the following installed:
- [Python 3.7+](https://www.python.org/)
-  [Fast API](https://fastapi.tiangolo.com)

- [InfluxDB 2.x](https://www.influxdata.com/products/influxdb/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```
2. **Install InfluxDB and Config**:
     ```
   docker run \
     --name influxdb2 \
     --publish 8086:8086 \
     --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
     --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
     --env DOCKER_INFLUXDB_INIT_MODE=setup \
     --env DOCKER_INFLUXDB_INIT_USERNAME=ADMIN_USERNAME \
     --env DOCKER_INFLUXDB_INIT_PASSWORD=ADMIN_PASSWORD \
     --env DOCKER_INFLUXDB_INIT_ORG=ORG_NAME \
     --env DOCKER_INFLUXDB_INIT_BUCKET=BUCKET_NAME \
     influxdb:2
   ```
3. **Create a `.env` file** in the root directory of your project with the following content:

   ```env
   INFLUXDB_URL=http://influxdb:8086
   INFLUXDB_TOKEN=your-influxdb-token
   INFLUXDB_ORG=your-organization
   INFLUXDB_BUCKET=your-bucket
   ```

   Replace `your-influxdb-token`, `your-organization`, and `your-bucket` with your actual InfluxDB credentials.


### Running Locally 

If you prefer to run the application locally:

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI application**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. - The API docs are available at [localhost:8000/docs/](http://localhost:8000/api/v1/docs/)
### API Endpoints

The FastAPI application provides the following endpoints:

#### 1. Write Data to InfluxDB

- **Endpoint**: `/write`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "bucket": "your-bucket",
    "measurement": "your_measurement",
    "location": "your_location",
    "temperature": 25.3
  }
  ```
- **Response**:
  ```json
  {
    "message": "Data written successfully"
  }
  ```

Example `curl` request to write data:
```bash
curl -X POST "http://localhost:8000/write" -H "Content-Type: application/json" -d '{
  "bucket": "your-bucket",
  "measurement": "your_measurement",
  "location": "your_location",
  "temperature": 25.3
}'
```

#### 2. Get the Latest Data Point

- **Endpoint**: `/latest`
- **Method**: `GET`
- **Query Parameters**:
  - `bucket`: The bucket name in InfluxDB.
  - `measurement`: The measurement name to query.
- **Response**:
  ```json
  {
    "time": "2024-08-29T12:34:56Z",
    "value": 25.3,
    "location": "your_location",
    "field": "temperature"
  }
  ```

Example `curl` request to get the latest data:
```bash
curl -X GET "http://localhost:8000/latest?bucket=your-bucket&measurement=your_measurement"
```


### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Contributing

Feel free to submit issues or pull requests to improve the project.