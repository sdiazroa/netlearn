from cs50 import SQL

# Create SQL db
open("crm.db", "w").close()
db = SQL("sqlite:///crm.db")

#Create table within database
db.execute("CREATE TABLE network (id INTEGER, name TEXT, cohort TEXT, hometown TEXT, past_industry TEXT, goal_industry TEXT, PRIMARY KEY(id))")
