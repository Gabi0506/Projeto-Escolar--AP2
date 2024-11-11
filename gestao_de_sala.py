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
    professores = relationship('Professor', secondary='professor_turma')  

    def __repr__(self):
        return f'<Turma(rt={self.rt}, ano={self.ano}, classe={self.classe})>'

class AlunoTurma(Base):
    __tablename__ = 'aluno_turma'
    aluno_ra = Column(String, ForeignKey('alunos.ra'), primary_key=True)
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)

class Professor(Base):
    __tablename__ = 'professores'

    rp = Column(Integer, primary_key=True)  
    nome = Column(String)  
    
    def __repr__(self):
        return f'<Professor(nome={self.nome}, rp={self.rp})>'

class ProfessorTurma(Base):
    __tablename__ = 'professor_turma'
    professor_rp = Column(Integer, ForeignKey('professores.rp'), primary_key=True)
    turma_rt = Column(String, ForeignKey('turmas.rt'), primary_key=True)

Base.metadata.create_all(engine)

def adicionar_aluno(ra, nome, idade):
    aluno_existente = session.query(Aluno).filter_by(ra=ra).first()
    if not aluno_existente:
        novo_aluno = Aluno(ra=ra, nome=nome, idade=idade)
        session.add(novo_aluno)
        session.commit()
        print(f'Aluno {nome} (RA: {ra}, idade: {idade}) adicionado com sucesso!')
    else:
        print("Aluno com RA já existe!")

def consultar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f'RA: {aluno.ra}, Nome: {aluno.nome}, Idade: {aluno.idade}')

def adicionar_turma(rt, ano, classe):
    turma_existente = session.query(Turma).filter_by(rt=rt).first()
    if not turma_existente:
        nova_turma = Turma(rt=rt, ano=ano, classe=classe)
        session.add(nova_turma)
        session.commit()
        print(f'Turma {rt} (ano: {ano}, classe: {classe}) adicionada com sucesso!')
    else:
        print("Turma com RT já existe!")

def consultar_turmas():
    turmas = session.query(Turma).all()
    for turma in turmas:
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

def adicionar_professor(rp, nome):
    professor_existente = session.query(Professor).filter_by(rp=rp).first()
    if not professor_existente:
        professor = Professor(rp=rp, nome=nome)
        session.add(professor)
        session.commit()
        print(f'Professor {nome} (RP: {rp}) adicionado com sucesso!')
    else:
        print("Professor já existe no sistema.")

def consultar_professores():
    professores = session.query(Professor).all()
    if professores:
        for professor in professores:
            print(f'Nome: {professor.nome}, RP: {professor.rp}')
    else:
        print("Ainda não há professores registrados no sistema.")

def adicionar_professor_a_turma(professor_rp, turma_rt):
    professor = session.query(Professor).filter_by(rp=professor_rp).first()
    turma = session.query(Turma).filter_by(rt=turma_rt).first()
    if professor and turma:
        turma.professores.append(professor)
        session.commit()
        print(f'Professor {professor.nome} (RP: {professor.rp}) adicionado à turma {turma.rt}.')
    else:
        print("Professor ou Turma não encontrados.")

def consultar_professor_por_turma(turma_rt):
    turma = session.query(Turma).filter_by(rt=turma_rt).first()
    if turma:
        print(f'Professores da turma {turma.rt} ({turma.ano} {turma.classe}):')
        for professor in turma.professores:
            print(f' - {professor.nome} (RP: {professor.rp})')
    else:
        print("Turma não encontrada.")

def listar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f'RA: {aluno.ra}, Nome: {aluno.nome}, Idade: {aluno.idade}')

def remover_aluno_de_turmas():
    listar_alunos()  # Lista todos os alunos
    aluno_ra = input('Digite o RA do Aluno que deseja expulsar: ')
    aluno = session.query(Aluno).filter_by(ra=aluno_ra).first()
    
    if aluno:
        for turma in aluno.turmas:
            turma.alunos.remove(aluno)  

        session.delete(aluno) 
        session.commit()
        print(f'Aluno {aluno.nome} (RA: {aluno.ra}) foi removido de todas as turmas e excluído do sistema.')
    else:
        print("Aluno não encontrado.")
def main():
    while True:
        print('\nEscolha uma opção:')
        print("-----------------------------")
        print('1. Adicionar Aluno')
        print('2. Adicionar Turma')
        print('3. Adicionar Professor')
        print("-----------------------------")
        print('4. Consultar Aluno')
        print('5. Consultar Turmas')
        print('6. Consultar Professor')
        print("-----------------------------")
        print('7. Adicionar aluno a turma')
        print('8. Adicionar professor a turma')
        print("-----------------------------")
        print('9. Consultar lista de alunos da turma')
        print('10. Consultar Professor por Turma')
        print('11. Explusar Aluno da Turma')
        print("-----------------------------")
        print('20. Sair')

        opcao = input('Opção: ')

        if opcao == '1' or opcao == 'Adicionar Aluno' or opcao == 'adicionar aluno' or opcao == 'Adicionar aluno':
            print("RA é o codigo indentificador do Aluno")  
            ra = input('RA do Aluno: ')
            nome = input('Nome do Aluno: ')
            idade = int(input('Idade do Aluno: '))
            adicionar_aluno(ra, nome, idade)


        elif opcao == '2' or opcao == 'Adicionar Turma' or opcao == 'Adicionar turma' or opcao == 'adicionar turma':
            print("RT é o codigo indentificador da turma")
            rt = input('RT da Turma: ')
            ano = input('Ano da Turma: ')
            classe = input('Classe da Turma: ')
            adicionar_turma(rt, ano, classe)

        elif opcao == '3' or opcao == 'Adicionar Professor' or opcao == 'Adicionar professor' or opcao == 'adicionar professor':
            print("RP é o codigo indentificador do Professor")
            rp = input('RP do Professor: ')
            nome = input('Nome do Professor: ')
            adicionar_professor(rp, nome)



        elif opcao == '4' or opcao == 'Consultar Aluno' or opcao == 'Consultar aluno' or opcao == 'consultar aluno' :
            print("Lista de Alunos:")
            consultar_alunos()


        elif opcao == '5' or opcao == 'Consultar Turma' or opcao == 'Consultar turma' or opcao == 'consultar turma':
            print("Lista de Turmas:")
            consultar_turmas()

        elif opcao == '6' or opcao == 'Consultar Professor' or opcao == 'Consultar professor' or opcao == 'consultar professor':
            print("Lista de Professores:")
            consultar_professores()


        elif opcao == '7' or opcao == 'Adicionar Aluno a Turma' or opcao == 'Adicionar Aluno a turma' or opcao == 'Adicionar aluno a turma' or opcao == 'adicionar aluno a turma':
            aluno_ra = input('RA do Aluno: ')
            turma_rt = input('RT da Turma: ')
            adicionar_aluno_a_turma(aluno_ra, turma_rt)

        elif opcao == '8' or opcao == 'Adicionar Professor a Turma' or opcao == 'Adicionar Professor a turma' or opcao == 'Adicionar professor a turma' or opcao == 'adicionar professor a turma':
            professor_rp = int(input('RP do Professor: '))
            turma_rt = input('RT da Turma: ')
            adicionar_professor_a_turma(professor_rp, turma_rt)

        elif opcao == '9' or opcao == 'Consultar Lista de Alunos da Turma' or opcao == 'Consultar Lista de Alunos da turma' or opcao == 'Consultar Lista de alunos da turma' or opcao == 'consultar lista de alunos da turma':
            turma_rt = input('RT da Turma: ')
            consultar_alunos_por_turma(turma_rt)

        elif opcao == '10' or opcao == 'Consultar Professor por Turma' or opcao == 'Consultar Professor por turma' or opcao == 'Consultar professor por Turma' or opcao == 'consultar professor por turma':
            turma_rt = input('RT da Turma: ')
            consultar_professor_por_turma(turma_rt)

        elif opcao == '11':
            remover_aluno_de_turmas()

        elif opcao == '20' or opcao == 'Sair' or opcao == 'sair':
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()  


