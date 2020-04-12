from database.main import Database

def serve_index():
    with Database() as db:
        db.insert({'test': '1'})
        return str(list(db.find()))