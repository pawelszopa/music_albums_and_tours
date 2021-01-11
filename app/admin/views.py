from functools import wraps

from flask import Blueprint, render_template, url_for, flash
from flask.views import View, MethodView
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import db
from app.album.forms import UpdateAlbumForm
from app.album.models import Album
from app.auth.models import User
from app.tour.models import Tour
from flask_babel import _

bp_admin = Blueprint('admin', __name__, template_folder='templates')


# zewnetrzny przyjmuje funkcje wewnetrzny atrybuty tej funkcji
# wraps powoduje ze wszystko bedzie wykolane w odpowiedniej kolejnosci
# zamienia kolejnosc wywoływania funkcji
def admin_required(fn):
    @wraps(fn)
    def _admin_required(*args, **kwargs):
        if not current_user.is_admin:
            flash(_('You need to be administrator to access this page'), 'danger')
            return redirect(url_for('auth.login'))
        return fn(*args, **kwargs)

    return _admin_required


# istnieją klasy zamiast funkcji
# sa 2 rodzaje get post osobno tutaj robimy razem

class TableView(View):
    decorators = [admin_required, login_required]

    # kolejność od dolu do gory dlatego taka kolejnosc bo inaczej wyala jak nie zalogowany

    def __init__(self, model, edit_allowed=False):
        self.edit_allowed = edit_allowed
        self.model = model
        self.columns = self.model.__mapper__.columns.keys()
        self.resource_name = self.model.__name__.lower()
        super(TableView, self).__init__()  # wywola dunder init od views

    # model konkretny model np albumy/tour  przekazujemy jako parametr
    # mamy dostep do bazy danych z poziomuy tego modelu
    # pole statyczne w klasie które są dostepne z poziomu i obiektu i klasy
    # pola statyczne tworzą nam kolumny w db
    # sql alchemy  pobiera kolumny dlatego mozemy do columns przypisać
    # instances to wszystkie wystąpienia danego modelu - czyli np albus to chcemy all albums
    # __name__ trzyma nazwe clasy
    def dispatch_request(self):  # wywoływane na gdy wejdziemy endpointa
        return render_template('resource_table.html', columns=self.columns, instances=self.model.query.all(),
                               edit_allowed=True, resource_name=self.resource_name)


# żeby podpiąć klasę czy funkcję trzeba ją zarejestrować
# add url rule to dekorator bp.route()

bp_admin.add_url_rule('/tours', view_func=TableView.as_view('tour', model=Tour))
bp_admin.add_url_rule('/users', view_func=TableView.as_view('user', model=User))


# class args i kwargs to przekazujemy model to jest w funkcji asview

class ModifyResourceView(MethodView):
    decorators = [admin_required, login_required]

    def __init__(self, model, edit_form):
        self.model = model
        self.columns = self.model.__mapper__.columns.keys()
        self.edit_form = edit_form
        self.resource_name = self.model.__name__.lower()
        super(MethodView, self).__init__()

    def get(self, resources_id):
        form = self.edit_form()
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instance(resources_id)

        # wyciągamy dane do resurce edit. Ona sciagnie pola z obiektu i bedzie mozna edytowac kazdy resopurece
        for parameter in parameters:
            form_attr = getattr(form, parameter)
            form_attr.data = getattr(model_instance, parameter)

        return render_template('resource_edit.html', resources_name=self.resource_name, model_instance=model_instance,
                               form=form, parameters=parameters)

    def post(self, resource_id):
        form = self.edit_form()
        parameters = self.get_update_parameters(form)
        model_instance = self.get_model_instance(resource_id)
        if form.validate_on_submit():
            for parameter in parameters:
                form_attr = getattr(form, parameter).data
                setattr(model_instance, parameter, form_attr)
            db.session.add(model_instance)
            db.session.commit()
            return redirect(url_for(f"admin.{self.resource_name}_table"))
        return redirect(url_for(f"admin.{self.resource_name}", resource_id=model_instance.id))

    def delete(self, resource_id):
        model_instance = self.get_model_instance(resource_id)
        db.session.delete(model_instance)
        db.session.commit()
        return ""

    def get_model_instance(self, resource_id):
        return self.model.query.filter_by(id=resource_id).first()

    def get_update_parameters(self, form_instance):
        parameter_list = list(form_instance.__dict__.keys())
        parameter_list = [parameter for parameter in parameter_list if
                          parameter[0] != '_' and parameter not in ['submit', 'csrf_token', 'meta']]
        return parameter_list
        # __dict__ wyciaga wszystkie pola zbiór kolekcja wszystkich pól

bp_admin.add_url_rule('/albums', view_func=TableView.as_view('album', model=Album))
bp_admin.add_url_rule('/albums/<int:resources_id>', view_func=ModifyResourceView.as_view('album_edit', model=Album, edit_form=UpdateAlbumForm))