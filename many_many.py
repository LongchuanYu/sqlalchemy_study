from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.orm import exc

Base = declarative_base()
engine = create_engine('sqlite:///many_many.db',echo=False)
Session = sessionmaker(bind=engine)
session = Session()

mid_table = Table(
    'mid_table',Base.metadata,
    Column('left_user_id',Integer,ForeignKey('users.id'),primary_key=True),
    Column('right_user_id',Integer,ForeignKey('users.id'),primary_key=True)
)
def insert(name):
    user = User(name = name)
    session.add(user)
    print('inser ok ...')

class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    name = Column(String)

    right_users = relationship(
        'User',
        secondary='mid_table',
        primaryjoin=(mid_table.c.left_user_id == id),
        secondaryjoin=(mid_table.c.right_user_id == id),
        backref = 'left_users'
    )
    def is_followed(self,user):
        '''current_user是否关注了user这个用户'''
        # for row in session.query(self.right_users).all():
        #     print(row)
        print(
            session.query(mid_table).filter(mid_table.c.left_user_id== self.id)\
                .filter(mid_table.c.right_user_id == user.id).count()
        )
        # return session.query(user.right_users)


    def following(self,user):
        '''关注user这个用户'''
        self.right_users.append(user)

    def __repr__(self):
        return "User:name=%s" % self.name
if __name__=='__main__':
    # Base.metadata.create_all(engine)
    # insert("aaa")
    # insert("bbb")
    # insert("ccc")
    # insert("ddd")
    # session.commit()
    current_user = session.query(User).get(1)
    target_user = session.query(User).get(2)
    # current_user.following(target_user)
    # session.commit()
    current_user.is_followed(target_user)
