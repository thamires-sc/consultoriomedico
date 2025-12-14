from db_connection import get_db_connection
import mysql.connector
from datetime import date


class Paciente:
    def __init__(self, id_paciente, nome, cpf, data_nascimento, telefone, convenio_id=None):
        self.id_paciente = id_paciente
        self.nome = nome
        self.cpf = cpf
        if isinstance(data_nascimento, date):
             self.data_nascimento = data_nascimento.isoformat()
        else:
             self.data_nascimento = data_nascimento
        self.telefone = telefone
        self.convenio_id = convenio_id

class PacienteDAO:
    def buscar_todos(self):
        conn = get_db_connection()
        if conn is None: return []
        
        pacientes = []
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT idPaciente, Nome, CPF, Data_Nascimento, Telefone, Convenio_idConvenio FROM Paciente"
        cursor.execute(sql) 
        
        for row in cursor:
            pacientes.append(Paciente(row['idPaciente'], row['Nome'], row['CPF'], row['Data_Nascimento'], row['Telefone'], row['Convenio_idConvenio']))
            
        cursor.close()
        conn.close()
        return pacientes

    def buscar_por_id(self, id_paciente):
        conn = get_db_connection()
        if conn is None: return None

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT idPaciente, Nome, CPF, Data_Nascimento, Telefone, Convenio_idConvenio FROM Paciente WHERE idPaciente = %s"
        cursor.execute(sql, (id_paciente,))
        
        row = cursor.fetchone()
        paciente = None
        if row:
            paciente = Paciente(row['idPaciente'], row['Nome'], row['CPF'], row['Data_Nascimento'], row['Telefone'], row['Convenio_idConvenio'])
            
        cursor.close()
        conn.close()
        return paciente

    # CREATE (Criar)
    def criar(self, paciente):
        conn = get_db_connection()
        if conn is None: return None
            
        cursor = conn.cursor()
        sql = "INSERT INTO Paciente (Nome, CPF, Data_Nascimento, Telefone, Convenio_idConvenio) VALUES (%s, %s, %s, %s, %s)"
        values = (paciente.nome, paciente.cpf, paciente.data_nascimento, paciente.telefone, paciente.convenio_id)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    # UPDATE (Atualizar)
    def atualizar(self, paciente):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = "UPDATE Paciente SET Nome = %s, CPF = %s, Data_Nascimento = %s, Telefone = %s, Convenio_idConvenio = %s WHERE idPaciente = %s"
        values = (paciente.nome, paciente.cpf, paciente.data_nascimento, paciente.telefone, paciente.convenio_id, paciente.id_paciente)
        
        cursor.execute(sql, values)
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0

    # DELETE (Deletar)
    def deletar(self, id_paciente):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = "DELETE FROM Paciente WHERE idPaciente = %s"
        
        cursor.execute(sql, (id_paciente,))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0