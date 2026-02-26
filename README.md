# **MLOps Engineering Technical Assessment:-JEET M Dave**



This project implements a simple, reproducible MLOps-style batch pipeline for generating trading signals based on rolling statistics from cryptocurrency OHLCV data.



* The application is designed to:
* Execute deterministically using a configuration file
* Emit structured metrics in JSON format
* Log the full execution lifecycle
* Run locally and inside a Docker container

## Dataset Note

The project uses a 10,000-row cryptocurrency OHLCV dataset (data.csv) as specified in the assignment requirements.

The dataset includes the following columns:

1. timestamp
2. open
3. high
4. low
5. close
6. volume_btc
7. volume_usd

In accordance with the task instructions, only the close column is used for rolling mean computation and signal generation.
The dataset has been validated for structure, formatting, and completeness to ensure correct processing within both local and Docker environments.



## Project Structure



mlops-task/

│

├── run.py

├── config.yaml

├── data.csv

├── requirements.txt

├── Dockerfile

├── README.md

├── metrics.json

└── run.log



## Configuration



The configuration file (config.yaml) contains:

seed: 42

window: 5

version: "v1"



* seed ensures reproducibility
* window controls the rolling mean window size
* version is included in the metrics output



## Logic Overview



* Load configuration
* Validate input dataset
* Compute rolling mean on the close column
* Generate trading signals:

&nbsp;	1 if close > rolling\_mean

&nbsp;	0 otherwise

* Compute signal rate
* Output metrics as JSON
* Log execution steps
* Only the close column is used for calculations, as required.



## Setup Instructions

Install dependencies locally:

**pip install -r requirements.txt**



## **Local Execution**



**Run the pipeline locally:**



**python run.py --input data.csv --config config.yaml \\**

    **--output metrics.json --log-file run.log**



## **This will:**



* **Generate metrics.json**
* **Generate run.log**
* **Print metrics to stdout**





## Docker Execution

Build the Docker image:

**docker build -t mlops-task .**



**Run the container:**

**docker run --rm mlops-task**



The container:



* Executes the batch job automatically
* Prints metrics to stdout
* Exits with code 0 on success
* Generates metrics.json and run.log inside the container



## **Example Metrics Output**

**{**

  **"version": "v1",**

  **"rows\_processed": 7,**

  **"metric": "signal\_rate",**

  **"value": 0.4286,**

  **"latency\_ms": 26,**

  **"seed": 42,**

  **"status": "success"**

**}**



**Dependencies:-**



1. **pandas**
2. **numpy**
3. **pyyaml**



**Error Handling**

* **The application handles:**
* **Missing input file**
* **Invalid CSV format**
* **Empty dataset**
* **Missing required columns**
* **Invalid configuration file**



**On error, a structured JSON response is returned:**

**{**

  **"version": "v1",**

  **"status": "error",**

  **"error\_message": "Description of the issue"**

**}**



**Notes**

* **No hard-coded paths are used.**
* **Results are reproducible across runs due to fixed random seed.**
* **Logging provides full traceability of the execution process.**




