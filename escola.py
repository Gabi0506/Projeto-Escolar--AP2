from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine('sqlite:///biblioteca.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Aluno(Base):
    __tablename__ = 'alunos'

    ra = Column(String, primary_key=True)    
    nome = Column(String)                     
    idade = Column(Integer)                   
    turmas = relationship('Turma', secondary='aluno_turma')  

    def __repr__(self):
        return f'<Aluno(ra={self.ra}, nome={self.nome}, idade={self.idade})>'

class Turma(Base):
    __tablename__ = 'turmas'

    rt = Column(String, primary_key=True)  
    ano = Column(String)                     
    classe = Column(String)                   
    alunos = relationship('Aluno', secondary='aluno_turma')  

    def __repr__(self):
        return f'<Turma(rt={self.rt}, ano={self.ano}, classe={self.classe})>'


class AlunoTurma(Base):
    __tablename__ = 'aluno_turma'
    aluno_ra = Column(String, ForeignKey('alunos.ra'), primary_key=True)  
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)   

Base.metadata.create_all(engine)

def adicionar_aluno(ra, nome, idade): 
    
    novo_aluno = Aluno(ra=ra, nome=nome, idade=idade)  
    session.add(novo_aluno)  
    session.commit()  
    print(f'Aluno {nome} (RA: {ra}, idade: {idade}) adicionado com sucesso!') 


def consultar_alunos(): 

    alunos = session.query(Aluno).all()  
    for aluno in alunos: 
        print(f'RA: {aluno.ra}, Nome: {aluno.nome}, Idade: {aluno.idade}')  
        
def adicionar_turma(rt, ano, classe): 

    nova_turma = Turma(rt=rt, ano=ano, classe=classe)  
    session.add(nova_turma)  
    session.commit()  
    print(f'Turma {rt} (ano: {ano}, classe: {classe}) adicionada com sucesso!') 

def consultar_turmas(): 

    turmas = session.query(Turma).all()  
    for turma in turmas: # chama da lista turmas o obeto turmas especifico
        print(f'RT: {turma.rt}, Ano: {turma.ano}, Classe: {turma.classe}')  

def adicionar_aluno_a_turma(aluno_ra, turma_rt): 
    aluno = session.query(Aluno).filter_by(ra=aluno_ra).first()  
    turma = session.query(Turma).filter_by(rt=turma_rt).first()  
    if aluno and turma:  

        turma.alunos.append(aluno)  

        session.commit()  
        print(f'Aluno {aluno.nome} (RA: {aluno.ra}) adicionado à turma {turma.rt}.') 
    else:
        print("Aluno ou Turma não encontrados.")  

def consultar_alunos_por_turma(turma_rt): 

    turma = session.query(Turma).filter_by(rt=turma_rt).first() 
    if turma:  
        print(f'Alunos na turma {turma.rt} ({turma.ano} {turma.classe}):')
        for aluno in turma.alunos:  
            print(f' - {aluno.nome} (RA: {aluno.ra})')  
    else:
        print("Turma não encontrada.") 

def main():

    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Aluno')
        print('2. Consultar Alunos')
        print('3. Adicionar Turma')
        print('4. Consultar Turmas')
        print('5. Adicionar Aluno a Turma')
        print('6. Consultar Alunos por Turma')
        print('7. Sair')
        opcao = input('Opção: ')  

        if opcao == '1': 
            ra = input('RA do Aluno: ')
            nome = input('Nome do Aluno: ')
            idade = int(input('Idade do Aluno: '))
            adicionar_aluno(ra, nome, idade)  

        elif opcao == '2':
            print("Lista de Alunos:")
            consultar_alunos()  

        elif opcao == '3':
            rt = input('RT da Turma: ')
            ano = input('Ano da Turma: ')
            classe = input('Classe da Turma: ')
            adicionar_turma(rt, ano, classe)  

        elif opcao == '4':
            print("Lista de Turmas:")
            consultar_turmas()  

        elif opcao == '5':
            aluno_ra = input('RA do Aluno: ')
            turma_rt = input('RT da Turma: ')
            adicionar_aluno_a_turma(aluno_ra, turma_rt) 

        elif opcao == '6':
            turma_rt = input('RT da Turma: ')
            consultar_alunos_por_turma(turma_rt)  

        elif opcao == '7':
            break  
            
        else:
            print("Opção inválida. Tente novamente.")  

if __name__ == "__main__":
    main()  # Executa a função principal ao iniciar o programa
