MENU_PRINCIPAL = """Menu Principal
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Remover Registros
5 - Sair
"""

MENU_RELATORIOS = """Relatórios
1 - Relatório de Tarefas por Funcionário
2 - Relatório de Todas as Tarefas
3 - Relatório de Funcionários
4 - Relatório de Setores
0 - Sair
"""

MENU_ENTIDADES = """Entidades
1 - SETOR
2 - FUNCIONÁRIO
3 - TAREFA
"""

def clear_console(wait_time:int=3):
    '''
       Esse método limpa a tela após alguns segundos
       wait_time: argumento de entrada que indica o tempo de espera
    '''
    import os
    from time import sleep
    sleep(wait_time)
    # Comando 'clear' funciona em Linux/macOS. Para Windows, use 'cls'
    os.system("clear" if os.name == 'posix' else 'cls')