from flask import Flask, abort, current_app, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
from MySQLdb import IntegrityError
import bcrypt
from datetime import datetime
from database import Database
import random
import os
from werkzeug.utils import secure_filename
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'static\\img')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.secret_key = 'woljokerino'
db = Database("127.0.0.1",3306, "root", "furkan1907", "mydb")
mysql = MySQL(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    session["logged"] = False
    session["admin"] = False
    return render_template("index.html")

@app.route("/home")
def home_page():
    if session["logged"] == True:
        query = "SELECT * FROM mydb.user WHERE idUser = " + str(session["idUser"])
        db.cursor.execute(query)
        userFound = db.cursor.fetchone()
        return render_template("home.html", user = userFound)
    else:
        return render_template("index.html")
   


@app.route("/profile/<string:userNickname>")
def profile(userNickname):
    print("geldi")
    if session["logged"] == True:
        query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
        db.cursor.execute(query)
        profileHolder = db.cursor.fetchone()
        return render_template("profile.html", profile = profileHolder)
    else:
        return redirect(url_for("error"))

@app.route("/profile/<string:userNickname>/edit", methods=["GET", "POST"])
def editProfile(userNickname):
    if request.method == "GET":
        if session["logged"] == True:
            query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
            db.cursor.execute(query)
            profileHolder = db.cursor.fetchone()
            return render_template("edit_profile.html", profile = profileHolder)
        else:
            return redirect(url_for("error"))
    else:
        query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(session["idUser"]) + "\""
        db.cursor.execute(query)
        profileHolder = db.cursor.fetchone()
        nickname = request.form.get("nickname")
        password = request.form.get("password").encode('utf-8')
        password2 = request.form.get("passwordNew").encode('utf-8')
        password3 = request.form.get("passwordNew2").encode('utf-8')
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if(bcrypt.hashpw(password,profileHolder[3].encode('utf-8')) != profileHolder[3].encode('utf-8')):
            return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRE YANLIŞ, TEKRAR DENEYİNİZ.')
        if password2 != '':
            if password2 != password3:
                return render_template("edit_profile.html", profile= profileHolder, message = 'ŞİFRELER EŞLEŞMİYOR.')
        if request.form.get("change") == "changeProfile":
            if age != '':
                if fullname != '':
                    if password2 != '':
                        hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                        query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                        vals = (nickname, fullname, hashedPass, mail, age,str(session["idUser"]))
                        db.cursor.execute(query, vals)
                        db.con.commit()
                    else:
                        query = "UPDATE mydb.user SET nickname = %s, fullname = %s, mail = %s, age = %s WHERE idUser = %s"
                        vals = (nickname, fullname, mail, age, str(session["idUser"]) )
                        db.cursor.execute(query, vals)
                        db.con.commit()
                else:
                    if password2 != '':
                        hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                        query = "UPDATE mydb.user SET nickname = %s, password = %s, mail = %s, age = %s WHERE idUser = %s"
                        vals = (nickname, hashedPass, mail, age,str(session["idUser"]))
                        db.cursor.execute(query, vals)
                        db.con.commit()
                    else:
                        query = "UPDATE mydb.user SET nickname = %s, mail = %s, age = %s WHERE idUser = %s"
                        vals = (nickname, mail, age,str(session["idUser"]))
                        db.cursor.execute(query, vals)
                        db.con.commit()
            else:
                if fullname != '':
                    if password2 == '':
                        
                        query = "UPDATE mydb.user SET nickname = %s, fullname = %s, mail = %s WHERE idUser = %s"
                        val = (nickname, fullname, mail,str(session["idUser"]))
                        db.cursor.execute(query, val)
                        db.con.commit()
                    else:
                        hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                        query = "UPDATE mydb.user SET nickname = %s, fullname = %s, password = %s, mail = %s WHERE idUser = %s"
                        val = (nickname, fullname, hashedPass, mail,str(session["idUser"]))
                        db.cursor.execute(query, val)
                        db.con.commit()
                else:
                    if password2 == '':
                        
                        query = "UPDATE mydb.user SET nickname = %s,mail = %s WHERE idUser = %s"
                        val = (nickname, mail,str(session["idUser"]))
                        db.cursor.execute(query, val)
                        db.con.commit()
                    else:
                        hashedPass = bcrypt.hashpw(password2,bcrypt.gensalt()) 
                        query = "UPDATE mydb.user SET nickname = %s,password = %s, mail = %s WHERE idUser = %s"
                        val = (nickname,hashedPass, mail,str(session["idUser"]))
                        db.cursor.execute(query, val)
                        db.con.commit()
            return redirect(url_for("profile", userNickname = nickname))
        else:
            query = "DELETE FROM mydb.rank WHERE userId = " + str(session["idUser"])
            db.cursor.execute(query)
            db.con.commit()
            db.cursor = db.con.cursor(buffered=True)
            query = "DELETE FROM mydb.user_play_bet WHERE user_id = " + str(session["idUser"])
            db.cursor.execute(query)
            db.con.commit()
            db.cursor = db.con.cursor(buffered=True)
            query = "DELETE FROM mydb.comment WHERE user_id = " + str(session["idUser"])
            db.cursor.execute(query)
            db.con.commit()
            db.cursor = db.con.cursor(buffered=True)
            query = "DELETE FROM mydb.user WHERE idUser = " + str(session["idUser"])
            db.cursor.execute(query)
            db.con.commit()
            return render_template("index.html")

        


@app.route("/bets")
def bets():
    query = "SELECT * FROM mydb.bet ORDER BY time"
    db.cursor.execute(query)
    bets = db.cursor.fetchall()
    query = "SELECT * FROM mydb.category ORDER BY nameCategory"
    db.cursor.execute(query)
    categories = db.cursor.fetchall()
    lenBet = len(bets)
    lenCat = len(categories)
    currentDate = datetime.today()
    return render_template("bets.html", bets = bets, date= currentDate , cats = categories, lenBet = lenBet, lenCat = lenCat)


@app.route("/bets/<categoryName>")
def bets_category(categoryName):
    query = "SELECT * FROM mydb.category WHERE nameCategory = \"" + str(categoryName) + "\""
    db.cursor.execute(query)
    cat = db.cursor.fetchone()
    catId = cat[0]
    query = "SELECT * FROM mydb.bet_has_category WHERE category_id = " + str(catId)
    db.cursor.execute(query)
    betsIds = db.cursor.fetchall()

    betArray = []
    for i in range(len(betsIds)):
        query = "SELECT * FROM mydb.bet WHERE idBets = \"" + str(betsIds[i][0]) + "\" ORDER BY mydb.bet.time"
        db.cursor.execute(query)
        betx = db.cursor.fetchone()
        print(betx)
        betArray.append(betx)
    
    query = "SELECT * FROM mydb.category ORDER BY nameCategory"
    db.cursor.execute(query)
    categories = db.cursor.fetchall()
    lenBet = len(betArray)
    lenCat = len(categories)
    currentDate = datetime.today()
    return render_template("bets.html", bets=betArray, date= currentDate ,cats = categories, lenBet = lenBet, lenCat = lenCat)

@app.route("/bets/bet/<betId>", methods=["GET","POST"])
def bets_show(betId):
    if session["logged"] == False and session["admin"] == False:
        return render_template("login.html")
    query = "SELECT * FROM mydb.bet WHERE idBets = \"" + str(betId) + "\""
    db.cursor.execute(query)
    bet = db.cursor.fetchone()
    query = "SELECT * FROM mydb.category ORDER BY nameCategory"
    db.cursor.execute(query)
    categories = db.cursor.fetchall()
    db.cursor = db.con.cursor(buffered=True)
    lenCat = len(categories)
    query = "SELECT * FROM mydb.user_play_bet WHERE user_id = " + str(session["idUser"]) + " AND bet_id = " + str(betId)
    db.cursor.execute(query)
    isPlayed = db.cursor.fetchone() 
    db.cursor = db.con.cursor(buffered=True)
    query = "SELECT comment.idComment, comment.user_id, comment.bet_id, comment.Text, comment.time, user.nickname FROM mydb.comment LEFT JOIN mydb.user ON comment.user_id = user.idUser WHERE bet_id = \"" + str(betId) + "\""
    db.cursor.execute(query)
    comments = db.cursor.fetchall()
    lenCom = len(comments)
    db.cursor = db.con.cursor(buffered=True)
    comDelete = request.form.getlist("delete")
    commentarea = request.form.get("commentArea")
    print(comDelete)
    if request.method == "GET":   
        print("asdsad")   
        return render_template("betAnswer.html", bet = bet,cats = categories, lenCat = lenCat, isPlayed = isPlayed, comments = comments, lenCom = lenCom)
    else:
        if request.form.get("showBet") == "answerBet":
            answer = request.form.get("answer")
            if answer == "yes":
                answer = 0
            else:
                answer = 1
            query = "INSERT INTO mydb.user_play_bet (user_id, bet_id, answer) VALUES (" + str(session["idUser"]) + ", "+ str(betId) +", "+ str(answer) +" )"    
            db.cursor.execute(query)
            db.con.commit()
            flash("ANSWERED SUCCESSFULLY","success")
            return redirect(url_for("bets_show", betId = betId))
        elif request.form.get("showBet") == "addComment":
            print("geldiasdasd")
            
            
            query = "INSERT INTO mydb.comment (user_id, bet_id, Text,time) VALUES (%s, %s, %s, current_timestamp())"
            vals = (session["idUser"], betId, commentarea)   
            db.cursor.execute(query, vals)
            db.con.commit()   
            return redirect(url_for("bets_show", betId = betId))
        else:
            print(comDelete)
            print("asdsa")
            for f in comDelete:
                query = "DELETE FROM mydb.comment WHERE idComment  = " + str(f)
                print(query)
                db.cursor.execute(query)
                db.con.commit()
            return redirect(url_for("bets_show", betId = betId))
            



@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    query = "SELECT * FROM mydb.user ORDER BY coin DESC, fullname"
    db.cursor.execute(query)
    users = db.cursor.fetchall()
    counter = 0
    for user in users:
        userHolder = users[counter]
        userId = userHolder[0] 
        counter += 1 
        query = "UPDATE mydb.rank SET idRank = ("+ str(counter) +") WHERE userId = (" + str(userId) +")"
        db.cursor.execute(query)
        db.con.commit()
    query = "SELECT * FROM mydb.rank ORDER BY idRank"
    db.cursor.execute(query)
    leaderboard = db.cursor.fetchall()
    lenTable = len(leaderboard)
    query = "SELECT  rank.idRank, rank.userId, user.nickname, user.coin FROM mydb.rank LEFT JOIN mydb.user ON rank.userId = user.idUser ORDER BY rank.idRank"
    db.cursor.execute(query)
    mergedTables = db.cursor.fetchall()
    lenTable = len(mergedTables)
    return render_template("leaderboard.html", merged = mergedTables, lenTable = lenTable)

@app.route("/editPanel", methods=["GET"])
def editBets():
    if session["admin"] == False:
        return render_template("error.html")
    if request.method == "GET":
        return render_template("edit_panel.html")
    

@app.route("/editPanel/add", methods=["GET", "POST"])
def addbet():
    if session["admin"] == False:
        return render_template("error.html")
    if request.method == "GET":
        return render_template("add_bet.html")
    else:
        question = request.form.get("question")
        time = request.form.get("time")
        file = request.files['file']
        filename1 = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
        reward = request.form.get("reward")
        categories = request.form.getlist("check")
        query = "INSERT INTO mydb.bet (question, imageUrl, reward, time) VALUES (%s,%s,%s,%s)"
        db.cursor = db.con.cursor(buffered=True)
        vals = (question, filename1, reward, time)
        db.cursor.execute(query, vals)
        db.con.commit()
        query = "SELECT * FROM mydb.bet WHERE question = \"" + question +"\""
        db.cursor.execute(query)
        betChecker = db.cursor.fetchone()
        for i in categories:
            query = "SELECT * FROM mydb.category WHERE nameCategory = \"" + i + "\""
            db.cursor.execute(query)
            catChecker = db.cursor.fetchone()
            if catChecker is not None:
                catId = catChecker[0]
                query = "INSERT INTO mydb.bet_has_category (bet_id, category_id) VALUES ("+ str(betChecker[0]) +", "+ str(catId) +")"
                db.cursor.execute(query)
                db.con.commit()
        return redirect(url_for("edit_bets"))

        
@app.route("/editPanel/edit", methods=["GET"])
def edit_bets():
    if session["admin"] == False:
        return render_template("error.html")
    if request.method == "GET":
        query = "SELECT * FROM mydb.bet"
        db.cursor.execute(query)
        bets = db.cursor.fetchall()
        lenBets = len(bets)
        currentDate = datetime.today()
        return render_template("edit_bets.html", bets=bets, lenBets = lenBets, date = currentDate)

@app.route("/editPanel/edit/<betId>", methods=["GET", "POST"])
def edit_bet(betId):
    if session["admin"] == False:
        return render_template("error.html")
    if request.method == "GET":
        query = "SELECT *FROM mydb.bet WHERE idBets = \"" + betId + "\""
        db.cursor.execute(query)
        bet = db.cursor.fetchone()
        return render_template("edit_bet.html", bet=bet)
    else:
        query = "SELECT *FROM mydb.bet WHERE idBets = \"" + betId + "\""
        db.cursor.execute(query)
        bet = db.cursor.fetchone()
        question = request.form.get("question")
        reward = int(request.form.get("reward"))
        file = request.files['file']
        answer = request.form.get("radio")
        if answer == "dont":
            if file:
                filename1 = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename1))
                query = "UPDATE mydb.bet SET question = %s,imageUrl = %s, reward = %s WHERE idBets = %s"
                val = (question,filename1,reward,bet[0])
                db.cursor.execute(query, val)
                db.con.commit()
            else:
                query = "UPDATE mydb.bet SET question = %s, reward = %s WHERE idBets = %s"
                val = (question,reward,bet[0])
                db.cursor.execute(query, val)
                db.con.commit()
        else:
            query = "SELECT * FROM mydb.user_play_bet WHERE bet_id = \"" + str(bet[0]) + "\""
            db.cursor.execute(query)
            users = db.cursor.fetchall()
            db.cursor = db.con.cursor(buffered=True)
            query = "UPDATE mydb.bet SET answer = %s WHERE idBets = %s"
            vals = (answer, bet[0])
            db.cursor.execute(query,vals)
            db.con.commit()

            if users:
                for i in range(0, len(users)):
                    a = users[i][2]
                    if answer == str(a):
                        query = "SELECT * FROM mydb.user WHERE idUser = \"" + str(users[i][0]) +"\""
                        db.cursor.execute(query)
                        user = db.cursor.fetchone()
                        user = list(user)
                        user[6] = user[6] + reward
                        query = "UPDATE mydb.user SET coin = %s WHERE idUser = %s"
                        val = (user[6], user[0])
                        db.cursor.execute(query,val)
                        db.con.commit() 
        return render_template("edit_panel.html")

@app.route("/editPanel/delete", methods=["GET","POST"])
def delete_bet():
    if session["admin"] == False:
        return render_template("error.html")
    if request.method == "GET":
        query = "SELECT * FROM mydb.bet ORDER BY bet.time"
        db.cursor.execute(query)
        bets = db.cursor.fetchall()
        lenBets = len(bets)
        currentDate = datetime.today()
        return render_template("delete_bet.html",bets = bets,lenBets = lenBets, date=currentDate)
    else:
        deleteBets = request.form.getlist("betDelete")
        if deleteBets:
            for i in range(0, len(deleteBets)):
                query = "DELETE FROM mydb.bet_has_category WHERE bet_id = " + str(deleteBets[i])
                db.cursor.execute(query)
                db.con.commit()
                query = "DELETE FROM mydb.comment WHERE bet_id = " + str(deleteBets[i])
                db.cursor.execute(query)
                db.con.commit()
                query = "DELETE FROM mydb.user_play_bet WHERE bet_id = " + str(deleteBets[i])
                db.cursor.execute(query)
                db.con.commit()
                query = "DELETE FROM mydb.bet WHERE idBets = " + str(deleteBets[i])
                db.cursor.execute(query)
                db.con.commit()
                
        return render_template("edit_panel.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = ''
    if request.method == "GET":
        return render_template("login.html")
    else:
        nickname = request.form.get("nickname")
        password = request.form.get("password").encode('utf-8')
        if nickname is not None:
            print(nickname)
            query = "SELECT * FROM mydb.user WHERE nickname = \"" + nickname + "\""
            db.cursor.execute(query)
            userChecker = db.cursor.fetchone()
            if userChecker:
                if bcrypt.hashpw(password,userChecker[3].encode('utf-8')) == userChecker[3].encode('utf-8'):
                    session["logged"] = True
                    session["idUser"] = userChecker[0]
                    session["nickname"] = userChecker[1]
                    session.permanent = True
                    if(nickname == "admin"):
                        session["admin"] = True 
                    return redirect(url_for("home_page"))
                else:    
                    return render_template("login.html",message = "Your password is wrong!")
            else:
                return render_template("login.html", message = "There is no user with this nickname!")
        else:
            return render_template("login.html", message = "Fill the form!")


@app.route("/register", methods=["POST","GET"])
def register():
    message =''
    if request.method == "GET":
        return render_template("register.html")
    else:
        nickname = request.form.get("nickname")
        password = request.form.get("password").encode('utf-8')
        password2 = request.form.get("password2").encode('utf-8')
        fullname = request.form.get("fullname")
        mail = request.form.get("mail")
        age = request.form.get("age")
        if password2 != password:
            return render_template("register.html", message='ŞİFRELER EŞLEŞMİYOR. TEKRAR DENEYİNİZ..')
        hashedPass = bcrypt.hashpw(password,bcrypt.gensalt())
        query = "SELECT * FROM mydb.user WHERE mail = \"" + mail + "\""
        db.cursor.execute(query)
        checkMail = db.cursor.fetchone()
        if checkMail is not None:
            return render_template("register.html", message='BU MAİLLE BİR KAYIT ZATEN VAR.')
        query = "SELECT * FROM mydb.user WHERE nickname = \"" + nickname+ "\""
        db.cursor.execute(query)
        checkUser = db.cursor.fetchone()
        if checkUser is not None:
            return render_template("register.html", message="BU KULLANICI ADI KULLANIMDA")
        if age != '':
            if fullname != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail, age) VALUES (%s,%s,%s,%s,%s)"
                vals = (nickname, fullname, hashedPass, mail, age)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail, age) VALUES (%s,%s,%s,%s)"
                vals = (nickname, hashedPass, mail , age)
                db.cursor.execute(query, vals)
                db.con.commit()
        else:
            if fullname != '':
                query = "INSERT INTO mydb.user (nickname, fullname, password, mail) VALUES (%s,%s,%s,%s)"
                vals = (nickname, fullname, hashedPass, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
            else:
                query = "INSERT INTO mydb.user (nickname, password, mail) VALUES (%s,%s,%s)"
                vals = (nickname, hashedPass, mail)
                db.cursor.execute(query, vals)
                db.con.commit()
        query = "SELECT idUser FROM mydb.user WHERE nickname = \"" + nickname+ "\""
        db.cursor.execute(query)
        checkUser = db.cursor.fetchone()
        idHolder = checkUser[0]
        query = "INSERT INTO mydb.rank (userId) VALUES ("+ str(idHolder) +")"
        db.cursor.execute(query)
        db.con.commit()
        return render_template("register.html", message = "BAŞARIYLA KAYIT OLDUNUZ")


@app.route("/faq", methods=["GET", "POST"])
def faq():
    if request.method == "GET":
        return render_template("faq.html")
    else:
        if session["logged"] == False:
            return render_template("login.html")
        else:
            text = request.form.get("text")
            query = "INSERT INTO mydb.ticket (user_id, text, time) VALUES (%s, %s, current_timestamp())"
            vals = (session["idUser"], text)
            db.cursor.execute(query, vals)
            db.con.commit()
            msg = "Your ticket has been sent. We will send our respond to your mail. Don't forget to check your mail. See you!"
            return render_template("faq.html", message = msg)





@app.route("/logout")
def logout():
    session["logged"] = False
    session["nickname"] = False
    session["IdUser"] = False
    session["admin"] = False
    return redirect(url_for("index"))

@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == '__main__':
    app.run(debug=True)

