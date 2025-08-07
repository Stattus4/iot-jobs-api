# IoT Jobs

## Non-Production Installation

### Clone the Repository

```
git clone https://github.com/Stattus4/iot-jobs-api.git
```

```
cd iot-jobs-api
```

### Start MongoDB

```
docker compose -f docker/docker-compose.yml up
```

### IoT Jobs API

Create `.env` file.

```
MONGODB_URI=mongodb://username:password@localhost:27017/iot_jobs?authSource=admin
```

Create virtual environment.

```
python3 -m venv .venv
```

Activate virtual environment.

```
source venv/bin/activate
```

Install dependencies.

```
pip install -r requirements.txt
```

Start application.

```
uvicorn app.main:app --reload
```
