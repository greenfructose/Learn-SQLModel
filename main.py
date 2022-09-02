from typing import Optional
from sqlmodel import Field, Session, SQLModel, create_engine, or_, select

class Hero(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  name: str = Field(index=True)
  secret_name: str
  age: Optional[int] = Field(default=None, index=True)

sqlite_filename = 'database.db'
sqlite_url = f'sqlite:///{sqlite_filename}'

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

def create_heroes():
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    hero_4 = Hero(name="Tarantula", secret_name="Natalia Roman-on", age=32)
    hero_5 = Hero(name="Black Lion", secret_name="Trevor Challa", age=35)
    hero_6 = Hero(name="Dr. Weird", secret_name="Steve Weird", age=36)
    hero_7 = Hero(name="Captain North America", secret_name="Esteban Rogelios", age=93)

    with Session(engine) as session:
      session.add(hero_1)
      session.add(hero_2)
      session.add(hero_3)
      session.add(hero_4)
      session.add(hero_5)
      session.add(hero_6)
      session.add(hero_7)

      session.commit()


def select_heroes():
  with Session(engine) as session:
    heroes = session.exec(select(Hero)).all()
    print(heroes)

def select_heroes_limit(limit:int):
  with Session(engine) as session:
    heroes = session.exec(select(Hero).limit(limit)).all()
    print(heroes)

def select_heroes_limit_offset(limit:int, offset:int):
  with Session(engine) as session:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    print(heroes)

def select_hero_by_name(name:str, session:Session):
  with session:
    hero = session.exec(select(Hero).where(Hero.name == name)).one()
    return hero

def select_hero_by_id(id:int):
  with Session(engine) as session:
    hero = session.get(Hero, id)
    print(hero)

def select_hero_age_lt(age:int):
  with Session(engine) as session:
    result = session.exec(select(Hero).where(Hero.age < age))
    for hero in result:
      print(hero)

def select_hero_age_lt_eq(age:int):
  with Session(engine) as session:
    result = session.exec(select(Hero).where(Hero.age <= age))
    for hero in result:
      print(hero)

def select_hero_age_gt(age:int):
  with Session(engine) as session:
    result = session.exec(select(Hero).where(Hero.age > age))
    for hero in result:
      print(hero)

def select_hero_age_gt_eq(age:int):
  with Session(engine) as session:
    result = session.exec(select(Hero).where(Hero.age >= age))
    for hero in result:
      print(hero)

def select_hero_age_gt_eq_lt_eq(gt_age:int, lt_age:int):
  with Session(engine) as session:
    result = session.exec(select(Hero).where(Hero.age >= gt_age, Hero.age <= lt_age))
    for hero in result:
      print(hero)

def update_hero_age_by_name(age:int, name:str):
  with Session(engine) as session:
    hero = select_hero_by_name(name, session)
    hero.age = age
    session.add(hero)
    session.commit()
    session.refresh(hero)
    print(hero)

def delete_hero_by_name(name:str):
  with Session(engine) as session:
    hero = select_hero_by_name(name, session)
    print(f'Deleting Hero: {hero}')
    session.delete(hero)
    session.commit()

def main():
  # create_db_and_tables()
  # create_heroes()
  # select_heroes()
  # select_hero_by_name('Deadpond')
  # select_hero_age_lt(35)
  # select_hero_age_gt_eq(35)
  # select_hero_age_gt_eq_lt_eq(35, 40)
  # select_hero_by_id(20)
  # select_heroes_limit(3)
  # select_heroes_limit_offset(3, 3)
  # update_hero_age_by_name(16, 'Spider-Boy')
  delete_hero_by_name('Spider-Boy')

if __name__ == "__main__":
    main()