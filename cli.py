import re

import click
from flask import current_app
from flask.cli import with_appcontext


@click.command('list_bp_endpoints')
@click.argument('blueprint')
@with_appcontext  # zapewnia dostep do stosu aplikacji
def list_bp_endpoints(blueprint):
    for endpoint in current_app.view_functions.keys():
        if re.search(f'^{blueprint}.', endpoint):
            click.echo(endpoint)


def register_click_commands(app):
    app.cli.add_command(list_bp_endpoints)


'''
app.config['ADMIN_VIEWS'] = [re.search('admin.(.*)_table', view).group(1) for view in list(app.view_functions.keys()) if
                                 re.search('admin.(.*)_table', view)]
'''
