import sqlite3

class Contas:
    def __init__(self, arquivo):
        self.conn = sqlite3.connect(arquivo)
        self.cursor = self.conn.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS contas (
                numero_conta TEXT,
                nome_conta TEXT,
                saldo_anterior_corrente TEXT,
                saldo_dia_corrente TEXT,
                saldo_anterior_poupanca TEXT,
                saldo_dia_poupanca TEXT,
                dia_consulta TEXT
            )
        ''')
        self.conn.commit()

    def carrega_lista(self, lista_contas):
        lista_completa = []
        for conta in lista_contas:
            # Assegura que cada conta tenha 7 elementos, preenchendo os faltantes com ""
            while len(conta) < 7:
                conta.append("")
            lista_completa.append(conta)
        
        # Grava os dados no banco de dados
        self.gravar_contas(lista_completa)
        
        return lista_completa
    
    def gravar_contas(self, contas):
        self.cursor.executemany('''
            INSERT INTO contas (
                numero_conta, nome_conta, saldo_anterior_corrente, saldo_dia_corrente, 
                saldo_anterior_poupanca, saldo_dia_poupanca, dia_consulta
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', contas)
        self.conn.commit()

    def limpar_tabela(self):
        self.cursor.execute('DELETE FROM contas')
        self.conn.commit()

    def recuperar_contas(self):
        self.cursor.execute('SELECT * FROM contas')
        registros = self.cursor.fetchall()
        return registros

    def fechar(self):
        self.conn.close()

# Exemplo de uso
if __name__ == '__main__':
    ...
