import argparse
import time
import json
import pandas as pd
import numpy as np
import yaml
import os
import sys
import logging


def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def load_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    required_keys = ["seed", "window", "version"]
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    return config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()

    setup_logger(args.log_file)

    start_time = time.time()
    logging.info("Job started")

    try:
        config = load_config(args.config)
        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        logging.info(f"Config loaded: seed={seed}, window={window}, version={version}")

        np.random.seed(seed)

        if not os.path.exists(args.input):
            raise FileNotFoundError("Input file not found.")

        df = pd.read_csv(args.input)

        if df.empty:
            raise ValueError("Input file is empty.")

        if "close" not in df.columns:
            raise ValueError("Missing required 'close' column.")

        logging.info(f"Data loaded: {len(df)} rows")

        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        logging.info(f"Rolling mean calculated with window={window}")

        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        logging.info("Signals generated")

        rows_processed = len(df)
        signal_rate = df["signal"].mean()

        latency_ms = int((time.time() - start_time) * 1000)

        logging.info(
            f"Metrics: signal_rate={round(float(signal_rate), 4)}, rows_processed={rows_processed}"
        )

        output = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate), 4),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(output, f, indent=2)

        logging.info(f"Job completed successfully in {latency_ms}ms")

        print(json.dumps(output, indent=2))
        sys.exit(0)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")

        error_output = {
            "version": "v1",
            "status": "error",
            "error_message": str(e)
        }

        with open(args.output, "w") as f:
            json.dump(error_output, f, indent=2)

        print(json.dumps(error_output, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()