from flask import Blueprint, g, current_app, request, after_this_request

# Blueprinty nie służą tylko do views ale też można agregować kod

bp_url_processors = Blueprint('url_processors', __name__, )


# wykona się zanim request
@bp_url_processors.before_app_request
def before_request():
    if request.endpoint is 'static':  # pobrać obrazek czy coś takiego to robimy nic
        return

    if request.cookies.get('lang') != g.lang:
        @after_this_request
        def set_cookie(response):
            response.set_cookie('lang', g.lang, max_age=60 * 60 * 24 * 100)
            # max age jak dlugo powinno dzialac
            return response


# przed before reqyest sprawdzane jest czy lang ma takie samo jak g.lang i nic się nie dzieje
# po requescie dopisyjemy do uzytkownika cookies 'lang' na 100 dni


# dostarcza 2 parametry do  funkcji
@bp_url_processors.app_url_value_preprocessor
def pull_lang_code(endpoint, values):
    try:
        if endpoint == 'static':
            return

        g.lang = values.pop('lang')

    except Exception:
        if request.cookies.get('lang') and request.cookies.get('lang') in current_app.config['LANGUAGES']:
            g.lang = request.cookies.get('lang')
        else:
            g.lang = current_app.config['LANGUAGES'][0]


@bp_url_processors.app_url_defaults
def add_language_code(endpoint, values):
    if 'lang' in values:
        return

    if current_app.url_map.is_endpoint_expecting(endpoint, 'lang'):
        values['lang'] = g.lang

# current app proxy do aktualnie odpalonej apki
