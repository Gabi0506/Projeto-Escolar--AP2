from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError


engine = create_engine('sqlite:///gestao_professores.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Professor(Base):
    __tablename__ = "Professores"

    id = Column(Integer, primary_key=True)
    nome = Column(String)

    def __repr__(self):
        return f'<Professor(nome={self.nome}, ID={self.id})>'
    
    
    def adicionar_prof(nome):
        professor = session.query(Professor).filter_by(nome=nome).first()
        if not professor:
            professor = Professor(nome=nome)
            session.add(professor)
            session.commit()

    
    def consultar_prof():
        try:
            professores = session.query(Professor).all()
            if professores:
                for professor in professores:
                    print(professor.nome)
            else:
                print("Ainda não possuí professor registrado no sistema.")
        except OperationalError:
            print("Tabela de professores não existe ainda. Por favor, adicione um professor primeiro.")
        
def main():
   
    Base.metadata.create_all(engine)

    while True:
        print('\nEscolha uma opção:')
        print('1. Adicionar Professor')
        print('2. Consultar Professor')
        print('3. Sair')

        opcao = input('Opção: ')
        if opcao == '1':
            nome = input('Nome do Professor: ')
            id = input('Digite o ID do professor: ')
            Professor.adicionar_prof(nome, id)
        elif opcao == '2':
            Professor.consultar_prof()
        elif opcao == '3':
            break
        else:
            print('Opção inválida. Tente novamente.')

if __name__ == "__main__":
    main()
