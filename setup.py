from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey, Integer, String, Column, Float
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///MerchManager.db', echo=True)
Session = sessionmaker(bind=engine)


# Table 1: Merch: merch name, price (ex: CD, 15.00)
class Merch(Base):

    __tablename__ = 'merch'

    item = Column(String, primary_key=True)
    price = Column(Float)

    def __repr__(self):
        return 'Item: {} Price: ${}'.format(self.item, self.price)


# Table 2: Shows: show ID, date, venue (ex: 01, 11/11/11, Myth)
class Shows(Base):

    __tablename__ = 'shows'

    show_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    venue = Column(String)

    def __repr__(self):
        return 'Show ID: {} Date: {} Venue: {}'.format(self.show_id, self.date, self.venue)


# Table 3: Sales: show ID, merch name, price, number sold (ex: 01, CD, 15.00, 10)
class Sales(Base):

    __tablename__ = 'sales'

    show_id = Column(Integer, ForeignKey('shows.show_id'), primary_key=True)
    item = Column(String, ForeignKey('merch.item'), primary_key=True)
    price = Column(Float, ForeignKey('merch.price'))
    sold = Column(Integer)

    def __repr__(self):
        return 'Show ID: {} Item: {} Price: {} Sold: {}'.format(self.show_id, self.item, self.price, self.sold)


# Create the tables
Base.metadata.create_all(engine)


# Check if sample data has already been created, returns true or false
# Issue adding to db.py due to Python not liking circular dependencies
def check_sample_present():
    check_session = Session()
    num_items = check_session.query(Merch).count()
    check_session.close()
    if num_items > 0:
        return True
    else:
        return False


# Create sample data if not already present
if not check_sample_present():
    merch1 = Merch(item='Record', price=20.0)
    merch2 = Merch(item='CD', price=15.0)
    merch3 = Merch(item='Shirt', price=30.0)

    show1 = Shows(date='July 15 2017', venue='Spyhouse Coffee')
    show2 = Shows(date='July 20 2017', venue='First Avenue')
    show3 = Shows(date='July 30 2017', venue='Myth')

    sale1 = Sales(show_id=1, item='Record', price=20.0, sold=10)
    sale2 = Sales(show_id=2, item='CD', price=15.0, sold=15)
    sale3 = Sales(show_id=3, item='Shirt', price=30.0, sold=5)

    save_samples = Session()
    save_samples.add_all([merch1, merch2, merch3, show1, show2, show3, sale1, sale2, sale3])
    save_samples.commit()
    save_samples.close()
