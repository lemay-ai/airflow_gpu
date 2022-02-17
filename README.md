# Inference Pipeline

Creates an Airflow container that can call an inference container from its DAGs.

## Design Rationale

This project relies on Airflow's ability to launch external containers through `DockerOperator`.  

The functionality is:
- Airflow is launched.
- When a task is triggered, a `DockerOperator` task is launched.
- The specific container will launch, with its associated command:
	- e.g., `docker run inference:latest python3 main_inference.py -t <INFERENCE TYPE>`
	- `<INFERENCE_TYPE>` can be any inference activity added to `inference/main_inference.py`

## Project Structure

- dags: contains two example DAGs: one for testing `nvidia-smi` inside of the built container, and one for running inference.
- data: contains example data from [Kaggle](https://www.kaggle.com/ldorigo/full-sentences-only).
- docker: contains the Dockerfiles to build the inference containers.  These containers get an inference type as an incoming command. Copies over main_inference.py.
- docker-compose.yaml: Contains the main entrypoint. Intended to launch Airflow.
- inference: contains `main_inference.py`, the main file to be copied inside the `inference` container.
