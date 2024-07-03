from sqlalchemy import create_engine, text

# Informations de connexion à la base de données Neon
PGHOST = 'ep-silent-scene-a24zq74q.eu-central-1.aws.neon.tech'
PGDATABASE = 'tessiChequesDB'
PGUSER = 'tessiChequesDB_owner'
PGPASSWORD = 'xrGShCHD6Yf2'

# Création de l'URL de connexion à la base de données PostgreSQL NEON
DATABASE_URL = f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}/{PGDATABASE}"

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        # Utilisation de la classe text de sqlalchemy pour encapsuler la requête SQL
        query = text("SELECT * FROM cheque")
        
        # Exécution de la requête avec des paramètres, juste la requête query en l'occurence
        result = connection.execute(query)

        for row in result:
            print(row) 

except Exception as e:
    print(f"Erreur lors de l'exécution de la requête : {e}")

finally:
    engine.dispose()
