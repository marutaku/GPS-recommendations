from lib.core import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class UserDB(object):
    def get_user_by_id(self, id):
        return db.session.query(User).filter(User.id == id)

    def create_user(self, name, password):
        try:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()

    def get_user_by_name(self, name):
        return db.session.query(User).filter(User.name==name).all()

    @staticmethod
    def init():
        db.create_all()


