from db_connection import get_db_connection
import mysql.connector


class Medico:
    def __init__(self, id_medico, nome, crm, telefone, especialidade_id=None):
        self.id_medico = id_medico
        self.nome = nome
        self.crm = crm
        self.telefone = telefone
        self.especialidade_id = especialidade_id
        # Campo extra para armazenar o nome da especialidade para exibição
        self.especialidade = '' 

class MedicoDAO:
    
    def buscar_todos(self):
        conn = get_db_connection()
        if conn is None: return []
        
        medicos = []
        cursor = conn.cursor(dictionary=True)
        sql = """
        SELECT m.idMedico, m.Nome, m.CRM, m.Telefone, m.Especialidade_idEspecialidade, e.Especialidade AS nome_especialidade
        FROM Medico m
        JOIN Especialidade e ON m.Especialidade_idEspecialidade = e.idEspecialidade
        """
        cursor.execute(sql) 
        
        for row in cursor:
            medico = Medico(row['idMedico'], row['Nome'], row['CRM'], row['Telefone'], row['Especialidade_idEspecialidade'])
            medico.especialidade = row['nome_especialidade']
            medicos.append(medico)
            
        cursor.close()
        conn.close()
        return medicos

    def buscar_por_id(self, id_medico):
        conn = get_db_connection()
        if conn is None: return None

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT idMedico, Nome, CRM, Telefone, Especialidade_idEspecialidade FROM Medico WHERE idMedico = %s"
        cursor.execute(sql, (id_medico,))
        
        row = cursor.fetchone()
        medico = None
        if row:
            medico = Medico(row['idMedico'], row['Nome'], row['CRM'], row['Telefone'], row['Especialidade_idEspecialidade'])
            
        cursor.close()
        conn.close()
        return medico

    def criar(self, medico):
        conn = get_db_connection()
        if conn is None: return None
            
        cursor = conn.cursor()
        sql = "INSERT INTO Medico (Nome, CRM, Telefone, Especialidade_idEspecialidade) VALUES (%s, %s, %s, %s)"
        values = (medico.nome, medico.crm, medico.telefone, medico.especialidade_id)
        
        try:
            cursor.execute(sql, values)
            conn.commit()
            last_id = cursor.lastrowid
            return last_id
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erro ao criar médico: {err}")
            return None
        finally:
            cursor.close()
            conn.close()

    def atualizar(self, medico):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = """
        UPDATE Medico SET 
            Nome = %s, 
            CRM = %s, 
            Telefone = %s, 
            Especialidade_idEspecialidade = %s 
        WHERE idMedico = %s
        """
        values = (medico.nome, medico.crm, medico.telefone, medico.especialidade_id, medico.id_medico)
        
        try:
            cursor.execute(sql, values)
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erro ao atualizar médico: {err}")
            return False
        finally:
            cursor.close()
            conn.close()

    def deletar(self, id_medico):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = "DELETE FROM Medico WHERE idMedico = %s"
        
        try:
            cursor.execute(sql, (id_medico,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Erro ao deletar médico: {err}")
            return False
        finally:
            cursor.close()
            conn.close()