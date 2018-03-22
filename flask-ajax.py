from flask import Flask, render_template, redirect, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_wtf.csrf import CsrfProtect
import subprocess, os

class Config:
    SECRET_KEY = '111222333444'


app = Flask(__name__)
app.config.from_object(Config)
CsrfProtect(app)


class MyForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()])


@app.route('/', endpoint='home', methods=['GET', 'POST'])
def home():
    form = MyForm()
    submitted = False
    message = None
    if form.validate_on_submit():
        submitted = True
        message = 'Success'
    return render_template('home-angular.html', form=form, submitted=submitted, message=message)

@app.route('/my-ajax-endpoint', methods=['POST'])
def ajax_handler():
    form = MyForm()
    message = ""
    if form.validate_on_submit():
        my_env = os.environ.copy()
        with open('example.txt','w') as f:
            f.write(form.text.data)
            f.close()
            subprocess.check_output(['sh','scripts/parse.sh', 'example.txt'])
            output = open('out.txt').read()

        # result = subprocess.check_output(['pwd'], env=my_env)
        return jsonify({ 'success': True,
            'result': output,
            'message': 'Success!'})
    for field, errors in form.errors.items():
        for error in errors:
            message += (u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ))
    return jsonify({'success': False,
                    'message': message})


if __name__ == '__main__':
    app.run()
