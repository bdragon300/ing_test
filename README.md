# Installation

```
pip3 -r requirements.txt
```

Then specify `wsgi.app` as application object in wsgi configuration

Next, create site configuration file (`config.py` for instance) and put its path
to the `CONFIG_FILE` environment variable. As long as it is not specified the
default configuration from `default_config.py` will be used.

# Development server

Run `python3 wsgi.py` and development server will appear at 127.0.0.1:5000.

# Debugging

Firstly, set DEBUG = True in configuration.

Add `"debug": true` to the higher level of the request object to debug the
rules. The debug output will be returned as text as following:

```
text content contains 1
and
text length more 10
and
( category title equal Новости or category title equal Животные )
and
( category title in ['Животные', 'Новости'] )
```
