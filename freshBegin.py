import db

username = "hating"
password = "youshallnotpass"
if __name__ == "__main__":
    db.createUser()
    print "Successfully create user table."
    db.createCraft()
    print "Successfully create craft table."
    db.insertUser(username,password)
    print "Successfully insert user."
    db.insertCraft()
    print "All done.Now you can run Shakespeare.py."
