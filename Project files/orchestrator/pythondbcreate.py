import sqlite3

conn = sqlite3.connect('./pythondatabase.db')

c = conn.cursor()

c.execute('''drop table if exists users''')
conn.commit()


c.execute('''drop table if exists rides''')
conn.commit()


c.execute('''drop table if exists rides_id''')
conn.commit()

c.execute('''drop table if exists ride_users''')
conn.commit()


c.execute('''CREATE TABLE users(
  username varchar(30),
  password varchar(40)
  
  );''')
conn.commit()


c.execute('''CREATE TABLE rides(

  created_by varchar(30),
  timestamp1 varchar(40),
  source1 int,
  destination1 int,
  rideid varchar(40)
  
  );''')
conn.commit()


c.execute('''CREATE TABLE rides_id(
  
    ridestart int
    
    );''')
conn.commit()


c.execute(''' CREATE TABLE ride_users(
   
    rideid varchar(30),
    userz varchar(30)
    
    );''')
conn.commit()




print('Created ')