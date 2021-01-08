from flask import Blueprint, render_template, flash, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from app import db
from app.album.forms import CreateAlbumForm
from app.album.models import Album
from app.helpers.utilities import save_image_upload
from flask_babel import _

bp_album = Blueprint('album', __name__, template_folder='templates')


@bp_album.route('/')
@login_required
def albums_list():
    albums = Album.query.all()
    return render_template('list_albums.html', albums=albums)


@bp_album.route('/create')
@login_required
def create():
    form = CreateAlbumForm()

    if form.validate_on_submit():
        album = Album(
            form.title.data,
            form.artist.data,
            form.description.data,
            form.genre.data,
            save_image_upload(form.image),  # uwaga! podajemy caly obiekt a nie data!!
            form.release_date.data,
            current_user.id
        )

        db.session.add(album)
        db.session.commit()
        flash(_("The new album has been added", 'success'))
        return redirect(url_for('album.albums_list'))

    return render_template('create_album.html')
