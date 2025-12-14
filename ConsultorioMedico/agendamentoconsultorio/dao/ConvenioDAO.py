from db_connection import get_db_connection
import mysql.connector

class Convenio:
    def __init__(self, id_convenio, nome, cnpj, contato):
        self.id_convenio = id_convenio
        self.nome = nome
        self.cnpj = cnpj
        self.contato = contato
        

class ConvenioDAO:
    
    def buscar_todos(self):
        conn = get_db_connection()
        if conn is None: return []
        
        convenios = []
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT idConvenio, Nome, CNPJ, Contato FROM Convenio" 
        cursor.execute(sql) 
        
        for row in cursor:
            convenios.append(Convenio(row['idConvenio'], row['Nome'], row['CNPJ'], row['Contato']))
            
        cursor.close()
        conn.close()
        return convenios

    # 2. READ (Buscar por ID)
    def buscar_por_id(self, id_convenio):
        conn = get_db_connection()
        if conn is None: return None

        cursor = conn.cursor(dictionary=True)
        sql = "SELECT idConvenio, Nome, CNPJ, Contato FROM Convenio WHERE idConvenio = %s"
        cursor.execute(sql, (id_convenio,))
        
        row = cursor.fetchone()
        convenio = None
        if row:
            convenio = Convenio(row['idConvenio'], row['Nome'], row['CNPJ'], row['Contato'])
            
        cursor.close()
        conn.close()
        return convenio

    # 3. CREATE (Criar)
    def criar(self, convenio):
        conn = get_db_connection()
        if conn is None: return None
            
        cursor = conn.cursor()
        sql = "INSERT INTO Convenio (Nome, CNPJ, Contato) VALUES (%s, %s, %s)"
        values = (convenio.nome, convenio.cnpj, convenio.contato)
        
        cursor.execute(sql, values)
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id

    # 4. UPDATE (Atualizar)
    def atualizar(self, convenio):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = "UPDATE Convenio SET Nome = %s, CNPJ = %s, Contato = %s WHERE idConvenio = %s"
        values = (convenio.nome, convenio.cnpj, convenio.contato, convenio.id_convenio)
        
        cursor.execute(sql, values)
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0

    # 5. DELETE (Deletar)
    def deletar(self, id_convenio):
        conn = get_db_connection()
        if conn is None: return False
            
        cursor = conn.cursor()
        sql = "DELETE FROM Convenio WHERE idConvenio = %s"
        
        cursor.execute(sql, (id_convenio,))
        conn.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        conn.close()
        return rows_affected > 0