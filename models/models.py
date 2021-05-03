from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dataclasses import dataclass
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id: int
    username: str
    email: str
    password: str
    create_at: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    trace_files = db.relationship('TraceFiles', backref='uploader', lazy=True)
    create_at = db.Column(db.DateTime(timezone=True),
                          default=datetime.utcnow)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"{self.username} created at {self.create_at}"


class TraceFiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    ext = db.Column(db.String(10), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"File('{self.filename}', '{self.date_posted}')"
