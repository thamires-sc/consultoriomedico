from flask import Flask, render_template, request, redirect, url_for, flash

from dao.PacienteDAO import PacienteDAO, Paciente
from dao.MedicoDAO import MedicoDAO, Medico
from dao.EspecialidadeDAO import EspecialidadeDAO 
from dao.ConvenioDAO import ConvenioDAO, Convenio 

from datetime import datetime 


from config import SECRET_KEY


app = Flask(__name__)
app.config.from_object('config') 
app.secret_key = SECRET_KEY 

paciente_dao = PacienteDAO()
medico_dao = MedicoDAO()
especialidade_dao = EspecialidadeDAO() 
convenio_dao = ConvenioDAO() 

@app.route('/')
def index():
    return redirect(url_for('listar_pacientes'))

# ====================================================================
# CRUD: PACIENTES
# ====================================================================

# READ (Listar Pacientes)
@app.route('/pacientes')
def listar_pacientes():
    lista = paciente_dao.buscar_todos()
    return render_template('pacientes/listar.html', pacientes=lista)

# GET (Formulário de Criação)
@app.route('/pacientes/novo')
def novo_paciente():
    paciente_vazio = Paciente(id_paciente=None, nome='', cpf='', data_nascimento='', telefone='')
    return render_template('pacientes/form.html', titulo='Novo Paciente', paciente=paciente_vazio)

# GET (Formulário de Edição)
@app.route('/pacientes/editar/<int:id_paciente>')
def editar_paciente(id_paciente):
    paciente = paciente_dao.buscar_por_id(id_paciente)
    if paciente:
        return render_template('pacientes/form.html', titulo='Editar Paciente', paciente=paciente)
    return redirect(url_for('listar_pacientes'))

# POST (Salvar - Criação ou Edição)
@app.route('/pacientes/salvar', methods=['POST'])
def salvar_paciente():
    id_paciente = request.form.get('id_paciente', None)
    
    paciente_obj = Paciente(
        id_paciente=id_paciente if id_paciente and id_paciente != 'None' else None,
        nome=request.form['nome'],
        cpf=request.form['cpf'],
        data_nascimento=request.form['data_nascimento'],
        telefone=request.form['telefone'],
        convenio_id=1 # ID fixo para simplificar
    )

    if paciente_obj.id_paciente:
        paciente_dao.atualizar(paciente_obj)
    else:
        paciente_dao.criar(paciente_obj)
        
    return redirect(url_for('listar_pacientes'))

# DELETE (Excluir)
@app.route('/pacientes/deletar/<int:id_paciente>')
def deletar_paciente(id_paciente):
    paciente_dao.deletar(id_paciente)
    return redirect(url_for('listar_pacientes'))


# ====================================================================
# CRUD: MÉDICOS
# ====================================================================

# READ (Listar Médicos)
@app.route('/medicos')
def listar_medicos():
    lista = medico_dao.buscar_todos()
    return render_template('medicos/listar.html', medicos=lista)

# GET (Formulário de Criação)
@app.route('/medicos/novo')
def novo_medico():
    medico_vazio = Medico(id_medico=None, nome='', crm='', telefone='')
    lista_especialidades = especialidade_dao.buscar_todos()
    
    return render_template('medicos/form.html', 
                           titulo='Novo Médico', 
                           medico=medico_vazio, 
                           especialidades=lista_especialidades)

# GET (Formulário de Edição)
@app.route('/medicos/editar/<int:id_medico>')
def editar_medico(id_medico):
    medico = medico_dao.buscar_por_id(id_medico)
    lista_especialidades = especialidade_dao.buscar_todos()

    if medico:
        return render_template('medicos/form.html', 
                               titulo='Editar Médico', 
                               medico=medico, 
                               especialidades=lista_especialidades)
    return redirect(url_for('listar_medicos'))

# POST (Salvar - Criação ou Edição)
@app.route('/medicos/salvar', methods=['POST'])
def salvar_medico():
    id_medico = request.form.get('id_medico', None)
    
    medico_obj = Medico(
        id_medico=id_medico if id_medico and id_medico != 'None' else None,
        nome=request.form['nome'],
        crm=request.form['crm'],
        telefone=request.form['telefone'],
        especialidade_id=request.form['especialidade_id'] 
    )

    if medico_obj.id_medico:
        medico_dao.atualizar(medico_obj)
    else:
        medico_dao.criar(medico_obj)
        
    return redirect(url_for('listar_medicos'))

# DELETE (Excluir)
@app.route('/medicos/deletar/<int:id_medico>')
def deletar_medico(id_medico):
    medico_dao.deletar(id_medico)
    return redirect(url_for('listar_medicos'))


# ====================================================================
# CRUD: CONVÊNIOS (SOLUÇÃO PARA O BuildError)
# ====================================================================

# READ (Listar Convênios) - Rota necessária para o link funcionar
@app.route('/convenios')
def listar_convenios():
    lista = convenio_dao.buscar_todos()
    return render_template('convenios/listar.html', convenios=lista)

# GET (Formulário de Criação)
@app.route('/convenios/novo')
def novo_convenio():
    convenio_vazio = Convenio(id_convenio=None, nome='', cnpj='', contato='')
    return render_template('convenios/form.html', titulo='Novo Convênio', convenio=convenio_vazio)

# GET (Formulário de Edição)
@app.route('/convenios/editar/<int:id_convenio>')
def editar_convenio(id_convenio):
    convenio = convenio_dao.buscar_por_id(id_convenio)
    if convenio:
        return render_template('convenios/form.html', titulo='Editar Convênio', convenio=convenio)
    return redirect(url_for('listar_convenios'))

# POST (Salvar - Criação ou Edição)
@app.route('/convenios/salvar', methods=['POST'])
def salvar_convenio():
    id_convenio = request.form.get('id_convenio', None)
    
    convenio_obj = Convenio(
        id_convenio=id_convenio if id_convenio and id_convenio != 'None' else None,
        nome=request.form['nome'],
        cnpj=request.form['cnpj'],
        contato=request.form['contato']
    )

    if convenio_obj.id_convenio:
        convenio_dao.atualizar(convenio_obj)
    else:
        convenio_dao.criar(convenio_obj)
        
    return redirect(url_for('listar_convenios'))

# DELETE (Excluir)
@app.route('/convenios/deletar/<int:id_convenio>')
def deletar_convenio(id_convenio):
    convenio_dao.deletar(id_convenio)
    return redirect(url_for('listar_convenios'))


# --------------------------
# EXECUÇÃO
# --------------------------

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)