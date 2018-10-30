import os
import flask

from itsdangerous import json

app = flask.Flask('ingenix_test')

# You can override config file via CONFIG_FILE environment var
config_fn = os.environ.get('CONFIG_FILE') or 'config/default_config.py'
app.config.from_pyfile(config_fn)


# Preload jsonschema file
with open(app.config['APP_VALIDATION_SCHEMA_FILE'], 'r') as f:
    validation_schema = json.load(f)
