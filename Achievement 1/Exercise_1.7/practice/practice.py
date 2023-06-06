from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base


# think of engine as the bridge connection between the SQL DB and this Python code
engine = create_engine("mysql://cf-python:password@localhost/my_database")

# Session is the class that binds to engine
Session = sessionmaker(bind=engine)

# session interacts with the DB
session = Session()

# Base is an object template from sqlalchemy used to create the Recipe class
Base = declarative_base()

class Recipe(Base):
  __tablename__ = "practice_recipes"

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"

try:
  Base.metadata.create_all(engine)
except:
  print("couldn't create that table... it probably exists already 🤷‍♂️")

tea = Recipe(
  name = "Tea",
  cooking_time = 5,
  ingredients = "Tea Leaves, Water, Sugar"
)

session.add(tea)
session.commit()
