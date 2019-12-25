from sqlalchemy import create_engine,Column,Integer,String,ForeignKey,Table,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
from sqlalchemy.orm import exc
Base = declarative_base()
engine = create_engine('sqlite:///app.db',echo=False)
Session = sessionmaker(bind=engine)
post_keywords = Table(
    'post_keywords',
    Base.metadata,
    Column('post_id',ForeignKey('posts.id'),primary_key=True),
    Column('keyword_id',ForeignKey('keywords.id'),primary_key=True)
)
class User(Base):
    __tablename__='users'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)
    addresses = relationship('Address',order_by=id,back_populates='user')
    posts = relationship('BlogPost',back_populates='author')
    def __repr__(self):
        return "<User(name='%s',fullname='%s',nickname='%s')>" % \
        (self.name,self.fullname,self.nickname)
class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer,primary_key=True)
    email = Column(String,nullable=False)
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship('User',back_populates='addresses')
    def __repr__(self):
        return "<Address(email='%s')>" % self.email

class BlogPost(Base):
    __tablename__='posts'
    id = Column(Integer,primary_key=True)
    user_id = Column(Integer,ForeignKey('users.id'))
    headline=Column(String(255),nullable=True)
    body=Column(Text)

    author = relationship('User',back_populates='posts')

    keywords = relationship('Keyword',
        secondary=post_keywords,
        back_populates='posts')
    def __repr__(self):
        return "BlogPost(%r, %r, %r)" % (self.headline, self.body, self.author)
class Keyword(Base):
    __tablename__ = 'keywords'

    id = Column(Integer, primary_key=True)
    keyword = Column(String(50), nullable=False, unique=True)
    posts = relationship('BlogPost',
                         secondary=post_keywords,
                         back_populates='keywords')
    def __init__(self, keyword):
        self.keyword = keyword
def insert_user(name,fullname,nickname):
    session = Session()
    user = User(name=name,fullname=fullname,nickname=nickname)
    session.add(user)
    session.commit()
    print('inser ok ...')
def insert_address(email,user_id):
    session = Session()
    addr = Address(email=email,user_id=user_id)
    session.add(addr)
    session.commit()
if __name__=='__main__':
    session = Session()
    # try:
    #     wendy = session.query(User).filter_by(name='wendy').one()
    # except exc.NoResultFound:
    #     print("not found")
    # else:
    #     print('ok')
    # post = BlogPost(headline="Wendy's Blog Post",body="this is a test",author=wendy)

    # post.keywords.append(Keyword('wendyy'))
    # post.keywords.append(Keyword('firstpost'))
    # session.add(post)
    # session.commit()

    query = session.query(BlogPost).filter(BlogPost.keywords.any(keyword='firstpost')). \
        all()
    print(query)
    