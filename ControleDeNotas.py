from sqlalchemy import Column, Integer, String, ForeignKey, Float, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
session = Session()

class Aluno(Base):
    __tablename__ = 'alunos'
    ra = Column(String, primary_key=True)
    nome = Column(String)
    notas = relationship("Nota", back_populates="aluno")

class Disciplina(Base):
    __tablename__ = "disciplinas"
    id = Column(Integer, primary_key=True)
    nome = Column(String, unique=True)
    notas = relationship("Nota", back_populates="disciplina")

class Nota(Base):
    __tablename__ = "notas"
    id = Column(Integer, primary_key=True)
    aluno_id = Column(String, ForeignKey('alunos.ra'))
    disciplina_id = Column(Integer, ForeignKey('disciplinas.id'))
    valor = Column(Float, nullable=False)
    aluno = relationship("Aluno", back_populates="notas")
    disciplina = relationship("Disciplina", back_populates="notas")

Base.metadata.create_all(engine)

def adicionar_aluno(ra, nome):
    try:
        novo_aluno = Aluno(ra=ra, nome=nome)
        session.add(novo_aluno)
        session.commit()
        print(f"Aluno {nome} adicionado com sucesso!")
    except IntegrityError:
        session.rollback()
        print(f"Erro: RA {ra} já existe!")

def adicionar_disciplina(nome):
    try:
        nova_disciplina = Disciplina(nome=nome)
        session.add(nova_disciplina)
        session.commit()
        print(f"Disciplina {nome} adicionada com sucesso!")
    except IntegrityError:
        session.rollback()
        print(f"Erro: Disciplina {nome} já existe!")
    except ValueError:
        session.rollback()
        print(f"Erro: Erro de valor, digite o nome de uma disciplina!")

def adicionar_nota(aluno_ra, nome_disciplina, valor):
    try:
        disciplina = session.query(Disciplina).filter_by(nome=nome_disciplina).first()
        if not disciplina:
            print(f"Erro: Disciplina '{nome_disciplina}' não encontrada.")
            return

        aluno = session.query(Aluno).filter_by(ra=aluno_ra).first()
        if not aluno:
            print(f"Erro: Aluno com RA '{aluno_ra}' não encontrado.")
            return

        nova_nota = Nota(aluno_id=aluno_ra, disciplina_id=disciplina.id, valor=valor)
        session.add(nova_nota)
        session.commit()
        print(f"Nota {valor} adicionada para o aluno {aluno_ra} na disciplina {nome_disciplina}.")
    except ValueError:
        print("Erro: Por favor, insira um número válido para a nota.")
    except IntegrityError:
        session.rollback()
        print("Erro ao adicionar a nota. Verifique se o aluno e a disciplina existem.")

def listar_alunos():
    alunos = session.query(Aluno).all()
    for aluno in alunos:
        print(f"RA: {aluno.ra}, Nome: {aluno.nome}")

def listar_disciplinas():
    disciplinas = session.query(Disciplina).all()
    for disciplina in disciplinas:
        print(f"Disciplina: {disciplina.nome}, ID: {disciplina.id}")

def listar_notas():
    notas = session.query(Nota).all()
    for nota in notas:
        aluno = session.query(Aluno).filter_by(ra=nota.aluno_id).first()
        disciplina = session.query(Disciplina).filter_by(id=nota.disciplina_id).first()
        print(f"Aluno: {aluno.nome}, RA: {aluno.ra}, Disciplina: {disciplina.nome}, Valor: {nota.valor}")

def main():
    while True:
        print("\nGerenciamento de Alunos, Disciplinas e Notas.")
        print("1. Adicionar Aluno")
        print("2. Adicionar Disciplina")
        print("3. Adicionar Nota")
        print("4. Listar Alunos")
        print("5. Listar Disciplinas")
        print("6. Listar Notas")
        print("7. Sair")

        try:
            opcao = int(input("Escolha uma opção: "))

            if opcao == 1:
                ra = int(input("Digite o RA do aluno: "))
                nome = input("Digite o nome do aluno: ")
                adicionar_aluno(ra, nome)

            elif opcao == 2:
                disciplinas_validas = {
                    "Matematica", "Geografia", "Ciências", "Língua Portuguesa",
                    "História", "Educação Física", "Artes"
                }

                nome = input("Digite o nome da disciplina: ").capitalize()

                if nome in disciplinas_validas:
                    adicionar_disciplina(nome)
                else:
                    print("Matéria inválida!")

            elif opcao == 3:
                aluno_ra = input("Digite o RA do aluno: ")
                nome_disciplina = input("Digite o nome da disciplina: ")
                valor = float(input("Digite a nota: "))
                adicionar_nota(aluno_ra, nome_disciplina, valor)

            elif opcao == 4:
                listar_alunos()

            elif opcao == 5:
                listar_disciplinas()

            elif opcao == 6:
                listar_notas()

            elif opcao == 7:
                print("Saindo do sistema...")
                break

            else:
                print("Opção inválida")

        except ValueError:
            print("Erro: Entrada inválida!")

if __name__ == "__main__":
    main()
