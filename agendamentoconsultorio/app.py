from flask import Flask, redirect, url_for
from config import SECRET_KEY

from views.paciente_views import paciente_bp
from views.medico_views import medico_bp
from views.convenio_views import convenio_bp
from views.especialidade_views import especialidade_bp

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = SECRET_KEY

app.register_blueprint(paciente_bp)
app.register_blueprint(medico_bp)
app.register_blueprint(convenio_bp)
app.register_blueprint(especialidade_bp)


@app.route('/')
def index():

    return redirect(url_for('paciente.listar'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)