# creating a flask application that will fetch data from the database and display it on the web page

from flask import Flask, render_template
import mysql.connector

def connectToDatabase(user,password,host,database):
    # connecting to the database
    mydb = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database
    )
    return mydb

def fetchFromDatabase(mydb,query):
    # fetching data from the database
    mycursor = mydb.cursor()
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    return myresult

def createApp():
    # creating a flask application
    app = Flask(__name__)

    @app.route('/')
    def index():
        # connecting to the database
        mydb = connectToDatabase("root","root","localhost","c361")

        create_query = "CREATE TABLE IF NOT EXISTS test (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)"
        # creating a table in the database
        mycursor = mydb.cursor()
        mycursor.execute(create_query)

        insert_query = "insert into test (name,age) values (%s,%s)"

        # inserting data into the database

        data = [
            ("John",20),
            ("Amy",22),
            ("Peter",21),
            ("Hannah",23)
        ]

        mycursor.executemany(insert_query,data)
        mydb.commit()

        # fetching data from the database
        myresult = fetchFromDatabase(mydb,"SELECT * FROM test")

        # rendering the template
        return render_template("index.html", data=myresult)

    return app

if __name__ == "__main__":
    app = createApp()
    app.run()