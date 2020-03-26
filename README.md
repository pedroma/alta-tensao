# alta-tensao
Alta Tensão PodCast Generator

The goal of this script is only to generate a podcast XML file and upload it to Digital Ocean Spaces.

Just create a virtualenv, set the enviroment variables described below and:

```
   pip install -r requirements.txt
   python alta_tensao_generator.py
```

Enviroment variables:

```
DO_BUCKET_REGION: digital ocean bucket region
DO_SPACE_KEY: digital ocean space key
DO_SPACE_SECRET: digital ocean space secret
DO_BUCKET_NAME: digital ocean space bucket name
```
