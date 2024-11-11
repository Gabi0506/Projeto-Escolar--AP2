from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Criação do engine e da sessão
engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
session = Session()

# os cod abaixo sao para declarar a base ou seja a onde os dados vao ser armazenados
Base = declarative_base()

# base para os alunos

class Aluno(Base):
    __tablename__ = 'alunos'

    ra = Column(String, primary_key=True)    # RA do aluno, é o numero que permite adiconar o aluno a lista
    nome = Column(String)                     # Nome do aluno
    idade = Column(Integer)                   # Idade do aluno
    turmas = relationship('Turma', secondary='aluno_turma')  # Relacionamento de alunos com turmas

    def __repr__(self):
        return f'<Aluno(ra={self.ra}, nome={self.nome}, idade={self.idade})>'

# base para a turma

class Turma(Base):
    __tablename__ = 'turmas'

    rt = Column(String, primary_key=True)    # RT da turma, é o numero que permite adiconar o aluno a lista de turmas
    ano = Column(String)                      # ano (ex: '7')
    classe = Column(String)                   # letra da turma (ex: 'A')
    alunos = relationship('Aluno', secondary='aluno_turma')  # Relacionamento de turmas com alunos

    def __repr__(self):
        return f'<Turma(rt={self.rt}, ano={self.ano}, classe={self.classe})>'

# base para a junção do aluno a lista turma

class AlunoTurma(Base):
    __tablename__ = 'aluno_turma'
    aluno_ra = Column(String, ForeignKey('alunos.ra'), primary_key=True)  # RA do aluno
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)   # RT da turma

# os cod abaixo sao para a Criação das tabelas

Base.metadata.create_all(engine)

def adicionar_aluno(ra, nome, idade): # serve para adicionar um novo aluno ao BC
    
    novo_aluno = Aluno(ra=ra, nome=nome, idade=idade)  # Cria uma instância de Aluno RA é usado como chae primaria
    session.add(novo_aluno)  # Adiciona o novo aluno à sessão
    session.commit()  # Salva as mudanças no banco de dados
    print(f'Aluno {nome} (RA: {ra}, idade: {idade}) adicionado com sucesso!') # printa as informações fornecidas


def consultar_alunos(): # consulta todos os alunos do banco de dados

    alunos = session.query(Aluno).all()  # Obtém todos os alunos
    for aluno in alunos: # é tipo para puchar da lista alunos o objeto aluno
        print(f'RA: {aluno.ra}, Nome: {aluno.nome}, Idade: {aluno.idade}')  # Exibe as informações de cada aluno individualmente

def adicionar_turma(rt, ano, classe): # função cria a turma

    nova_turma = Turma(rt=rt, ano=ano, classe=classe)  # Cria uma instância de Turma, RT é o cod que indentifica a turma e é usado como chave primaria
    session.add(nova_turma)  # Adiciona a nova turma à sessão
    session.commit()  # Salva as mudanças no banco de dados
    print(f'Turma {rt} (ano: {ano}, classe: {classe}) adicionada com sucesso!') # printa as informações salvas no banco

def consultar_turmas(): # consulta e exibe todas as turmas cadastradas no BC

    turmas = session.query(Turma).all()  # chama todas as turmas do banco
    for turma in turmas: # chama da lista turmas o obeto turmas especifico
        print(f'RT: {turma.rt}, Ano: {turma.ano}, Classe: {turma.classe}')  # Exibe as informações de cada turma

def adicionar_aluno_a_turma(aluno_ra, turma_rt): # esse codigo serve para associar o aluno a turma

    # aluno_ra: O RA do aluno (string) que será associado à turma.
    # turma_rt: O RT da turma (string) à qual o aluno será adicionado.
    
    aluno = session.query(Aluno).filter_by(ra=aluno_ra).first()  # Busca o aluno pelo RA, o cod filter serve para filtrar o aluno pelo RA
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT, o cod filter serve para filtrar a turma pelo RT
    if aluno and turma:  # Verifica se ambos foram encontrados no caso aluno e turma

        turma.alunos.append(aluno)  # Adiciona o aluno à turma esse bem dito cod serve para adionar o obj aluno a turma 

        session.commit()  # Salva as mudanças no banco de dados
        print(f'Aluno {aluno.nome} (RA: {aluno.ra}) adicionado à turma {turma.rt}.') # printa qual aluno foi a adionado a qual turma
    else:
        print("Aluno ou Turma não encontrados.")  # Mensagem de erro caso não encontrem

def consultar_alunos_por_turma(turma_rt): # consulta a lista de alunos da turma

    turma = session.query(Turma).filter_by(rt=turma_rt).first()  # Busca a turma pelo RT o cod filter serve para filtrar a turma pelo RT
    if turma:  # Verifica se a turma foi encontrada
        print(f'Alunos na turma {turma.rt} ({turma.ano} {turma.classe}):')
        for aluno in turma.alunos:  # tras os dados a da turma
            print(f' - {aluno.nome} (RA: {aluno.ra})')  # Exibe cada aluno
    else:
        print("Turma não encontrada.")  # Mensagem de erro caso a turma não seja encontrada

# ------------------------função principal--------------------------------------
#-------------------------tambem é o menu----------------------------------------

def main():

    while True: # esse é o loop, vcs sabem aquele enquanto tal função for true ele continua
#aqui é ja o menu onde o usuario deve digitar um numero para e executar a função por meio de um input
        print('\nEscolha uma opção:')
        print('1. Adicionar Aluno')
        print('2. Consultar Alunos')
        print('3. Adicionar Turma')
        print('4. Consultar Turmas')
        print('5. Adicionar Aluno a Turma')
        print('6. Consultar Alunos por Turma')
        print('7. Sair')


# é o cod principal que vai pegar o numero que o usuario adionou
        opcao = input('Opção: ')  
#----------------------------------------------------------------------

        if opcao == '1': 
            ra = input('RA do Aluno: ')
            nome = input('Nome do Aluno: ')
            idade = int(input('Idade do Aluno: '))
            adicionar_aluno(ra, nome, idade)  # Chama a função para adicionar aluno

        elif opcao == '2':
            print("Lista de Alunos:")
            consultar_alunos()  # Chama a função para consultar alunos

        elif opcao == '3':
            rt = input('RT da Turma: ')
            ano = input('Ano da Turma: ')
            classe = input('Classe da Turma: ')
            adicionar_turma(rt, ano, classe)  # Chama a função para adicionar turma

        elif opcao == '4':
            print("Lista de Turmas:")
            consultar_turmas()  # Chama a função para consultar turmas

        elif opcao == '5':
            aluno_ra = input('RA do Aluno: ')
            turma_rt = input('RT da Turma: ')
            adicionar_aluno_a_turma(aluno_ra, turma_rt)  # Chama a função para associar aluno à turma

        elif opcao == '6':
            turma_rt = input('RT da Turma: ')
            consultar_alunos_por_turma(turma_rt)  # Chama a função para consultar alunos por turma

        elif opcao == '7':
            break  # Encerra o loop e sai do programa
            
        else:
            print("Opção inválida. Tente novamente.")  # Mensagem de erro para opção inválida

if __name__ == "__main__":
    main()  # Executa a função principal ao iniciar o programa
