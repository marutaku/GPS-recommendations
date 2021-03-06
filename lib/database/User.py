from lib.core import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    active_hour = db.Column(db.Integer, default=None)
    slack_id = db.Column(db.String(30), default=None)
    create_at = db.Column(db.DateTime, server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class UserDB(object):
    def get_user_by_id(self, id):
        return db.session.query(User).filter(User.id == id).one()

    def create_user(self, name, password):
        try:
            new_user = User(name=name, password=password)
            db.session.add(new_user)
            db.session.commit()
        except:
            db.session.rollback()

    def get_user_by_name(self, name):
        return db.session.query(User).filter(User.name==name).all()

    def get_all_user(self):
        return db.session.query(User).all()

    def update_password(self, username, hashed_password):
        user = db.session.query(User).filter(User.name == username).one()
        user.password = hashed_password
        db.session.commit()

    def get_all_user_name(self):
        return db.session.query(User.name).all()


    @staticmethod
    def init():
        db.create_all()


