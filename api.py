import flask
import jsonschema
import entities
import itertools
from app import app, validation_schema


@app.route('/api/v1/conditions', methods=('POST', 'GET'))
def conditions():
    data = flask.request.get_json(force=True)
    jsonschema.validate(data, validation_schema)  # Pre-validate common request structure

    if app.config['DEBUG'] and data.get('debug'):
        return flask.Response(
            debug_string(
                data['article'], data['conditions']['operator'], data['conditions']['rules'],
                data['conditions'].get('groups')
            ))

    errors = process_rules(
        data['article'], data['conditions']['operator'], data['conditions']['rules'],
        data['conditions'].get('groups')
    )
    return flask.jsonify(errors)


def process_rules(article: str, operator: str, rules: list, groups=None) -> dict:
    rules_res = []
    groups_res = []

    for rule in rules:
        try:
            obj = entities.get_object_class(rule['object'])(article)
            is_valid = obj.check(rule['property'], rule['expression'], rule['value'])
        except (KeyError, ValueError):
            flask.abort(400)

        if is_valid:
            rules_res.append({
                'is_valid': is_valid,
                'error': ''
            })
        else:
            rules_res.append({
                'is_valid': is_valid,
                'error': '{} is not {} {}'.format(rule['object'], rule['expression'], rule['value'])
            })

    res = {'rules': rules_res}

    if groups:
        for group in groups:
            group_res = process_rules(article, group['operator'], group['rules'])
            groups_res.append(group_res)

        res['groups'] = groups_res

    whole_valid = False
    if operator == 'and':
        whole_valid = all(x['is_valid'] for x in itertools.chain(rules_res, groups_res))
    elif operator == 'or':
        whole_valid = any(x['is_valid'] for x in itertools.chain(rules_res, groups_res))
    else:
        flask.abort(400, "Unknown operator '{}'".format(operator))

    res['is_valid'] = whole_valid
    return res


def debug_string(article, operator: str, rules: list, groups=None) -> str:
    """Build debug string"""
    chunks = []

    for rule in rules:
        # Perform dummy check to ensure that parameters are correct
        try:
            obj = entities.get_object_class(rule['object'])(article)
            obj.check(rule['property'], rule['expression'], rule['value'])
        except (KeyError, ValueError):
            flask.abort(400)

        chunks.append('{object} {property} {expression} {value}'.format(**rule))

    for group in groups:
        chunks2 = []
        for rule in group['rules']:
            # Perform dummy check to ensure that parameters are correct
            obj = entities.get_object_class(rule['object'])(article)
            try:
                obj.check(rule['property'], rule['expression'], rule['value'])
            except (KeyError, ValueError):
                flask.abort(400)

            chunks2.append(' {object} {property} {expression} {value} '.format(**rule))

        chunks.append('(' + group['operator'].join(chunks2) + ')')

    return ('\n' + operator + '\n').join(chunks)
