from flask import Blueprint, render_template, request, redirect, url_for
from dao.MedicoDAO import MedicoDAO, Medico
from dao.EspecialidadeDAO import EspecialidadeDAO

medico_bp = Blueprint('medico', __name__)
medico_dao = MedicoDAO()
especialidade_dao = EspecialidadeDAO()

@medico_bp.route('/medicos')
def listar():
    lista = medico_dao.buscar_todos()
    return render_template('medicos/listar.html', medicos=lista)

@medico_bp.route('/medicos/novo')
def novo():
    medico_vazio = Medico(None, '', '', '')
    lista_especialidades = especialidade_dao.buscar_todos()
    return render_template('medicos/form.html', titulo='Novo Médico', medico=medico_vazio, especialidades=lista_especialidades)

@medico_bp.route('/medicos/editar/<int:id_medico>')
def editar(id_medico):
    medico = medico_dao.buscar_por_id(id_medico)
    lista_especialidades = especialidade_dao.buscar_todos()
    if medico:
        return render_template('medicos/form.html', titulo='Editar Médico', medico=medico, especialidades=lista_especialidades)
    return redirect(url_for('medico.listar'))

@medico_bp.route('/medicos/salvar', methods=['POST'])
def salvar():
    id_medico = request.form.get('id_medico')
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
    return redirect(url_for('medico.listar'))

@medico_bp.route('/medicos/deletar/<int:id_medico>')
def deletar(id_medico):
    medico_dao.deletar(id_medico)
    return redirect(url_for('medico.listar'))