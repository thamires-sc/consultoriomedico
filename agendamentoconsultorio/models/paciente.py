from datetime import date

class Paciente:
    def __init__(self, id_paciente, nome, cpf, data_nascimento, telefone, convenio_id=None):
        self.id_paciente = id_paciente
        self.nome = nome
        self.cpf = cpf
        
        # Converte objeto date para string se necessário
        if isinstance(data_nascimento, date):
            self.data_nascimento = data_nascimento.isoformat()
        else:
            self.data_nascimento = data_nascimento
            
        self.telefone = telefone
        self.convenio_id = convenio_id