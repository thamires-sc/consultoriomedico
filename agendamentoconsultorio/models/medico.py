from datetime import date

class Medico:
    def __init__(self, id_medico, nome, crm, telefone, especialidade_id=None):
        self.id_medico = id_medico
        self.nome = nome
        self.crm = crm
        self.telefone = telefone
        self.especialidade_id = especialidade_id
        self.especialidade = '' 