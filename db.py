from google.cloud import firestore

db:firestore.Client = None

def init_db():
    global db
    db = firestore.Client()
    print("db created")



def get_db():
    if db is None:
        init_db()
    return db