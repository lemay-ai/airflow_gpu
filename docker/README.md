# Container Provisioning

Creates a container which contains the `main_inference.py` script.

## Before building

Make sure that the volume path in your DAG maps to an accessible location.

## Building

Running `build.sh` will copy all of the files to a local tmp folder and add 
them to the container.

## Next Steps

You should add your own models and map to the model source folder.
