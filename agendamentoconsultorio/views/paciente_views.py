from flask import Blueprint, render_template, request, redirect, url_for
# Importação separada: O objeto de dados vem de models, o objeto de acesso de dao
from models.paciente import Paciente
from dao.PacienteDAO import PacienteDAO
from dao.ConvenioDAO import ConvenioDAO

paciente_bp = Blueprint('paciente', __name__)
paciente_dao = PacienteDAO()
convenio_dao = ConvenioDAO()

@paciente_bp.route('/pacientes')
def listar():
    lista = paciente_dao.buscar_todos()
    return render_template('pacientes/listar.html', pacientes=lista)

@paciente_bp.route('/pacientes/novo')
def novo():
    # Usando a classe Paciente importada de models.paciente
    paciente_vazio = Paciente(None, '', '', '', '')
    lista_convenios = convenio_dao.buscar_todos()
    return render_template('pacientes/form.html', titulo='Novo Paciente', paciente=paciente_vazio, convenios=lista_convenios)

@paciente_bp.route('/pacientes/editar/<int:id_paciente>')
def editar(id_paciente):
    paciente = paciente_dao.buscar_por_id(id_paciente)
    lista_convenios = convenio_dao.buscar_todos()
    if paciente:
        return render_template('pacientes/form.html', titulo='Editar Paciente', paciente=paciente, convenios=lista_convenios)
    return redirect(url_for('paciente.listar'))

@paciente_bp.route('/pacientes/salvar', methods=['POST'])
def salvar():
    id_paciente = request.form.get('id_paciente')
    
    # Instanciando o modelo Paciente com os dados do formulário
    paciente_obj = Paciente(
        id_paciente=id_paciente if id_paciente and id_paciente != 'None' else None,
        nome=request.form['nome'],
        cpf=request.form['cpf'],
        data_nascimento=request.form['data_nascimento'],
        telefone=request.form['telefone'],
        convenio_id=request.form.get('convenio_id')
    )
    
    if paciente_obj.id_paciente:
        paciente_dao.atualizar(paciente_obj)
    else:
        paciente_dao.criar(paciente_obj)
        
    return redirect(url_for('paciente.listar'))

@paciente_bp.route('/pacientes/deletar/<int:id_paciente>')
def deletar(id_paciente):
    paciente_dao.deletar(id_paciente)
    return redirect(url_for('paciente.listar'))