from flask import Blueprint, render_template, request, redirect, url_for
from models.convenio import Convenio
from dao.ConvenioDAO import ConvenioDAO

convenio_bp = Blueprint('convenio', __name__)
convenio_dao = ConvenioDAO()

@convenio_bp.route('/convenios')
def listar():
    lista = convenio_dao.buscar_todos()
    return render_template('convenios/listar.html', convenios=lista)

@convenio_bp.route('/convenios/novo')
def novo():
    convenio_vazio = Convenio(None, '', '', '')
    return render_template('convenios/form.html', titulo='Novo Convênio', convenio=convenio_vazio)

@convenio_bp.route('/convenios/editar/<int:id_convenio>')
def editar(id_convenio):
    convenio = convenio_dao.buscar_por_id(id_convenio)
    if convenio:
        return render_template('convenios/form.html', titulo='Editar Convênio', convenio=convenio)
    return redirect(url_for('convenio.listar'))

@convenio_bp.route('/convenios/salvar', methods=['POST'])
def salvar():
    id_convenio = request.form.get('id_convenio')
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
    return redirect(url_for('convenio.listar'))

@convenio_bp.route('/convenios/deletar/<int:id_convenio>')
def deletar(id_convenio):
    convenio_dao.deletar(id_convenio)
    return redirect(url_for('convenio.listar'))