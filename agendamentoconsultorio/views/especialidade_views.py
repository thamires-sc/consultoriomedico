from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.especialidade import Especialidade
from dao.EspecialidadeDAO import EspecialidadeDAO

especialidade_bp = Blueprint('especialidade', __name__)
especialidade_dao = EspecialidadeDAO()

@especialidade_bp.route('/especialidades')
def listar():
    lista = especialidade_dao.buscar_todos()
    return render_template('especialidade/listar.html', especialidades=lista)

@especialidade_bp.route('/especialidades/novo')
def novo():
    return render_template('especialidade/form.html', titulo='Nova Especialidade')

@especialidade_bp.route('/especialidades/salvar', methods=['POST'])
def salvar():
    nome = request.form.get('nome_especialidade').strip()
    if nome:
        nova_esp = Especialidade(id_especialidade=None, nome=nome)
        if especialidade_dao.criar(nova_esp):
            flash(f"Especialidade '{nome}' cadastrada com sucesso!", "success")
        else:
            flash(f"Erro: A especialidade '{nome}' já existe.", "danger")
    return redirect(url_for('especialidade.listar'))