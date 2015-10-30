from app import db
from hashlib import md5

# Used WWW SQL Designer tool to sketch my idea
# Link: http://ondras.zarovi.cz/sql/demo/
# Click load and enter: rafeh01


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user_id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user_id'))
                     )


# noinspection PyUnresolvedReferences
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic'
                               )

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % self.nickname

    def avatar(self, size):
        # mm returns mystery man image if user does not have a gravatar account
        # the s=N option requests the avatar scaled to the given size in pixels
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    # noinspection PyUnboundLocalVariable
    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname=nickname).first() is None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            # check if the new username is in our database
            if User.query.filter_by(nickname=new_nickname).first() is None:
                break
            version += 1
        return new_nickname


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

