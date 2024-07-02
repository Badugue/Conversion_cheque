import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session

# Informations de connexion à la base de données Neon
PGHOST='ep-silent-scene-a24zq74q.eu-central-1.aws.neon.tech'
PGDATABASE='tessiChequesDB'
PGUSER='tessiChequesDB_owner'
PGPASSWORD='xrGShCHD6Yf2'

DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

# Vérifier la connexion à la base de données
try:
    connection = engine.connect()
    print("Connexion à la base de données réussie.")
    connection.close()
except Exception as e:
    print(f"Erreur de connexion : {e}")

# Chargement des fichiers CSV
listChqNB_csv = "C:/Users/remip/Documents/Projets/Tessi/ListeChqNB.csv"
# ensoleillement_csv = "C:\\Users\\Florian PESCOT\\OneDrive - DUPUY\\Bureau\\COURS\\bdd\\temps-densoleillement-par-an-par-departement-feuille-1.csv"

listChqNB_df = pd.read_csv(listChqNB_csv, delimiter=';')
#ensoleillement_df = pd.read_csv(ensoleillement_csv, delimiter=',')

# Renommer les colonnes
listChqNB_df.rename(columns={
    'NomFichier': 'id_cheque',
    'Zone4': 'zone4',
    'Zone3': 'zone3',
    'Zone2': 'zone2',
    'Montant': 'montant',
    'Cle': 'cle',
}, inplace=True)


# Assertions pour vérifier que les DataFrames ne sont pas vides
assert not listChqNB_df.empty, "Cheqyes DataFrame est vide"

# ORM Setup
Base = declarative_base()

class Cheque(Base):
    __tablename__ = 'cheque'
    id = Column(String, primary_key=True) 
    zone4 = Column(BigInteger)  # Utiliser BigInteger pour les valeurs potentiellement très grandes
    zone3 = Column(BigInteger)
    zone2 = Column(BigInteger)
    montant = Column(BigInteger)
    cle = Column(Integer)  # Gardez Integer si c'est approprié pour votre cas

Base.metadata.drop_all(engine)  # Supprimer les tables existantes pour les recréer
Base.metadata.create_all(engine)  # Créer les tables avec la nouvelle définition

# Utiliser ORM pour insérer des données avec bulk insert
try:
    session.no_autoflush = True

    print("Inserting Cheques...")
    unique_cheques = listChqNB_df.drop_duplicates(subset='id_cheque').to_dict(orient='records')
    
    # Créer une liste pour les données à insérer en s'assurant de spécifier id comme une chaîne
    data_to_insert = []
    for cheq in unique_cheques:
        data_to_insert.append({
            'id': str(cheq['id_cheque']),  # Assurez-vous que id est une chaîne de caractères
            'zone4': int(cheq['zone4']),   # Convertir en integer ou BigInteger si nécessaire
            'zone3': int(cheq['zone3']),
            'zone2': int(cheq['zone2']),
            'montant': int(cheq['montant']),
            'cle': int(cheq['cle']) if pd.notna(cheq['cle']) else None  # Assurez-vous que cle est int ou None
        })

    session.bulk_insert_mappings(Cheque, data_to_insert)
    session.commit()

    print("Toutes les données ont été insérées avec succès.")
except Exception as e:
    session.rollback()
    print(f"Erreur lors de l'insertion des données : {e}")



# Vérifier les données insérées
try:
    cheques = session.query(Cheque).all()

    print(f"Nombre de chèques insérés : {len(cheques)}")
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")