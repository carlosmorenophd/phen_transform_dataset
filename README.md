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

Run to celery by percentage



```
python test_task.py keep_percentage_of_no_empty pedigree_o_57_c_phenotypic.csv .80
```
