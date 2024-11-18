# Worker to transform dataset and get climate data.

## Climate data

This service work with [power service](https://power.larc.nasa.gov/api/temporal/hourly/point) to get data from temperatue, precipitacion, uv and other.

You can see all variable on [clime.json](clima.json)

## To installe the python

To use pyenv to select the current version of python
The file .python-version has the current version of python to this proyect
```
3.12.2
```
Command to create a virtual env of python

```
python -m venv venv
```

## Run command with outpout

To run a scrip of python that continue the ejecution

```
nohup python app/main.py  > output.log 2>&1 &
```

Build docker
```
docker build --tag phen/transform-dataset:24.05 .
```

Run Docker
```
docker run  -itd --name transform -v ${PWD}:/phen phen/transform-dataset:24.05
```


# New documentation
Run contained on dev

Build the images
```
docker compose -f compose.dev.yaml build
```

Run the contained
```
docker compose -f compose.dev.yaml up -d
```
Access to docker
`docker compose -f compose.dev.yaml exec -it tasksdd bash`

To run the celery task

```

watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A tasks worker --loglevel=INFO
```

Run to some test

normalize file

```
python tasks_test.py normalize_dataset lrace_trueba_fill_clean.csv zero_to_one Rendimiento
```





