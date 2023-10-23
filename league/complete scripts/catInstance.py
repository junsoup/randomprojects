import math
import random
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="cat"
)

db = mydb.cursor()

class Cat:

    def __init__(self, faces):
        self.faces = []
        self.load(faces)

    def load(self, file):
        # input faces
        f = open(file, 'r', encoding='utf8')
        count = 0
        face = ''
        for x in f:
            if x == '\n':
                self.faces.append(face)
                face = ''
                count += 1
            face += x
        self.faces.append(face)

        # load last cat state
        db.execute("SELECT * FROM state")
        state = db.fetchall()[0]
        self.health = state[1]
        self.happiness = state[2]
        self.lastStr = ''

    def needUpdate(self):
        catStr = str(self) 
        if self.lastStr == '' or self.lastStr != catStr:
            self.lastStr = catStr
            return True
            
        return False

    def __str__(self):
        # add inital emote line
        return self.faces[math.floor(self.happiness/2.01)] + self.getStatus() + self.faces[5]

    def save(self):
        values = (str(round(self.health)), str(round(self.happiness)))
        db.execute("UPDATE state SET health = %s, happiness = %s WHERE id = 1", values)
        mydb.commit()
        print(db.rowcount, " record(s) affected")


    def tick(self):
        # change by uniform random (range of -0.13 to +0.12)
        newHappiness = self.happiness + random.random()/4 - 0.13
        
        # bounds check
        newHappiness = max(0, min(10, newHappiness))

        # update value
        self.happiness = newHappiness
        
        # if happiness is low, lower health
        if self.happiness == 0:
            self.health = max(1, self.health - 1)
        if self.happiness > 9:
            self.health = min(10, self.health + .5)


        # save into database
        self.save()
        pass


    def getStatus(self):
        health = ""
        happiness = ""
        for i in range(5):
            if i < math.ceil(self.health/2):
                health += '█'
            else:
                health += '░'
            if i < math.ceil(self.happiness/2):
                happiness += '█'
            else:
                happiness += '░'
        return f'✚{health} ♡{happiness}　　　　　　　　　　　　　　　　　　　　　　　　　　　 '











