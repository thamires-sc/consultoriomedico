from db_connection import get_db_connection
from models.especialidade import Especialidade

class EspecialidadeDAO:
    def buscar_todos(self):
        conn = get_db_connection()
        if conn is None: return []
        
        especialidades = []
        try:
            cursor = conn.cursor(dictionary=True)
            sql = "SELECT IdEspecialidade, Especialidade FROM Especialidade" 
            cursor.execute(sql) 
            
            for row in cursor:
                especialidades.append(Especialidade(row['IdEspecialidade'], row['Especialidade']))
            
            cursor.close()
        except Exception as e:
            print(f"Erro ao buscar especialidades: {e}")
        finally:
            conn.close()
            
        return especialidades

    def criar(self, especialidade_obj):
        conn = get_db_connection()
        if conn is None: return False
        
        try:
            cursor = conn.cursor(dictionary=True)
            
            # 1. Verifica se já existe uma especialidade com esse nome (ignora maiúsculas/minúsculas)
            sql_check = "SELECT IdEspecialidade FROM Especialidade WHERE Especialidade = %s"
            cursor.execute(sql_check, (especialidade_obj.nome,))
            if cursor.fetchone():
                print("Erro: Especialidade já cadastrada.")
                return False 
            
            # 2. Se não existir, faz a inserção
            sql_insert = "INSERT INTO Especialidade (Especialidade) VALUES (%s)"
            cursor.execute(sql_insert, (especialidade_obj.nome,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao inserir especialidade: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
            
        return success