from flask import Flask
from flask import render_template, flash
from flask_bootstrap import Bootstrap
from flask import request
from flask_wtf import Form
from wtforms import StringField , validators, SubmitField
from flask_wtf.file import FileField, FileRequired

from youtoplay import youtoplay
class LinkForm(Form):
    url = StringField('URL:', [validators.URL])
    submit = SubmitField('Add Song')

class SongForm(Form):
    song = FileField(validators=[FileRequired('No file uploaded')])
    submit = SubmitField('Add File')

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'mukul123'
@app.route('/', methods=['GET', 'POST'])
def index():
    linkform = LinkForm(request.form)
    songform = SongForm(request.form)
    if request.method == 'POST' and (songform.validate() or linkform.validate()):
        ##Download here
        if linkform.validate():
            link = linkform.url.data
            if len(link)>0:
                youtoplay.youtube_download(link)
        if songform.validate():
            print("test")
            f = songform.song.data
            filename = secure_filename(f.filename)
            f.save(app.instance_path)
            youtoplay.upload_last()
        flash('success')
    return render_template('template.html', linkform=linkform, songform=songform)
