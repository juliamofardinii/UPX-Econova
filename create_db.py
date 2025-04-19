# create_db.py

from application import application, db, User, bcrypt

def create_database():
    with application.app_context():
        db.drop_all()
        db.create_all()

        hashed_password = bcrypt.generate_password_hash('adminpassword').decode('utf-8')
        admin_user = User(
            username='admin',
            email='admin@example.com',
            password=hashed_password,
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()

        print("Banco de dados recriado com sucesso!")

if __name__ == '__main__':
    create_database()
