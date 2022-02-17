# Inference Pipeline

Creates an Airflow container that can call an inference container from its DAGs.

## Design Rationale

This project relies on Airflow's ability to launch external containers through `DockerOperator`.  

The functionality is:
- Airflow is launched.
- When a task is triggered, a `DockerOperator` task is launched.
- The specific container will launch, with its associated command:
	- e.g., `docker run am_tf_inference:latest python3 inference.py -t <INFERENCE TYPE>`
	- `<INFERENCE_TYPE>` can be `rcon`, `new_rif`, or `fixpdf`

## Project Structure

- docker-compose.yaml: Contains the main entrypoint. Intended to launch Airflow.
- docker: contains the Dockerfiles to build the inference containers.  These containers get an inference type as an incoming command.