from db_connection import get_db_connection

class Especialidade:

    def __init__(self, id_especialidade, nome):
        self.id_especialidade = id_especialidade
        self.nome = nome

class EspecialidadeDAO:
    def buscar_todos(self):
        conn = get_db_connection()
        if conn is None: return []
        
        especialidades = []
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT idEspecialidade, Especialidade FROM Especialidade" 
        cursor.execute(sql) 
        
        for row in cursor:
            especialidades.append(Especialidade(row['idEspecialidade'], row['Especialidade']))
            
        cursor.close()
        conn.close()
        return especialidades