from flask import Flask, render_template, url_for,flash,redirect,request,session
from forms import RegistrationForm, LoginForm
import pandas as pd
import sqlite3
import os
import Question_Maker
import run
import addDisease
app = Flask(__name__)

# Some Definitions
app.config['SECRET_KEY'] = '4f9a5c9c0b0e66722f11b04bbfb4949f'


# Routes

@app.route('/')
@app.route('/home')
def home():
    return render_template('intro.html')

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/symps', methods=['POST','GET'])
def symptoms():
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    cur.execute("SELECT DISTINCT symptom FROM symptoms")
    symptom = cur.fetchall()

    if request.method == 'POST':
        session['visitor'] = 'visitor'
        session['sex'] = request.form.get('gender','udefined')
        if session['sex'] == "udefined":
            flash(f'Please select your gender!','danger')
            return redirect(url_for('home'))
        session['age'] = request.form['age']
        return render_template('symps.html', symptom = symptom)
    if request.method == 'GET' and 'email' in session:
        return render_template('symps.html', symptom = symptom)
    else:
        return redirect(url_for('info'))


Q1=Q2=[]
@app.route('/questions', methods=['POST','GET'])
def questions():
    if request.method == 'GET':
        return redirect(url_for('info'))
    symptoms = request.form.getlist('sym[]')
    if len(symptoms) <= 1:
        flash(f'Please select atleast 2 symptoms!','danger')
        return redirect(url_for('home'))
    myQuestions1,myQuestions2 = Question_Maker.fillter(symptoms)
    if len(myQuestions2) > 0:
        global Q1
        Q1=myQuestions1
        global Q2
        Q2=myQuestions2
        return render_template('choose-one.html',symptoms=symptoms,myQuestions1=myQuestions1,
                                                    myQuestions2=myQuestions2)
    else:
        return render_template('questions.html',symptoms=symptoms,myQuestions=myQuestions1)
    

@app.route('/choose', methods=['POST','GET'])
def chooseOne():
    if request.method == 'GET':
        return redirect(url_for('info'))
    symptoms = request.form.getlist('sym[]')
    choosen = request.form['ans']
    if choosen[0] == '1':
        symptoms.pop(1)
        choosen = choosen.replace('1','')
        symptoms.append(choosen)
    else:
        symptoms.pop(0)
        choosen = choosen.replace('2','')
        symptoms.append(choosen)
    
    myQuestions1,myQuestions2 = Question_Maker.fillter(symptoms)
    if len(myQuestions2) > 0:
        global Q1
        Q1=myQuestions1
        global Q2
        Q2=myQuestions2
        return render_template('choose-one.html',symptoms=symptoms,myQuestions1=myQuestions1,
                                                    myQuestions2=myQuestions2)
    else:
        return render_template('questions.html',symptoms=symptoms,myQuestions=myQuestions1)


@app.route('/diagnosis/<count>', methods=['POST','GET'])
def diagnosis(count):
    if request.method == 'GET':
        return redirect(url_for('info'))
    goodAnswer = []
    badAnswer = []
    ans = []
    for i in range(int(count)):
        ans = ans + request.form.getlist('ans['+str(i)+']')

    for x in range(len(ans)):
        if ans[x][-1] == '3' or ans[x][-1] == '2':
            badAnswer.append(ans[x])
        else:
            goodAnswer.append(ans[x])
    
    symptoms = request.form.getlist('sym[]')
    symptoms = list(set(symptoms+goodAnswer))
    diseases = run.run(symptoms)
    
    percent=[]
    diseasesSyms = []
    for i in range(len(diseases)):
        disSymps = getAllSyms(diseases[i])
        percent.append(getPercent(symptoms,disSymps))
        diseasesSyms.append(disSymps)


    for i in range(len(diseases)-1):
        for j in range(len(diseases)-i-1):
            if percent[j] < percent[j+1]:
                percent[j],percent[j+1] = percent[j+1],percent[j]
                diseases[j],diseases[j+1] = diseases[j+1],diseases[j]
                diseasesSyms[j],diseasesSyms[j+1] = diseasesSyms[j+1],diseasesSyms[j]
    
    if len(diseases) > 0:
        counter = 0
        finalDiseases = []
        finalPercent = []
        diseasesInfo = []
        finalDisSyms = []
        diseasesTips = []
        specialist = []
        for i in range(len(diseases)):
            if percent[i] == 0:
                continue
            finalDiseases.append(diseases[i])
            finalPercent.append(percent[i])
            finalDisSyms.append(diseasesSyms[i])
            diseasesInfo.append(getDiseaseData(diseases[i]))
            specialist.append(getSpecialist(diseasesInfo[i][4]))
            diseasesTips.append(getTips(diseases[i]))
            counter = counter + percent[i]
            if counter > 75.0:
                break
        return render_template('diagnosis.html',diseases=finalDiseases,percent=finalPercent,
                symptoms=symptoms,diseasesInfo=diseasesInfo,diseasesSyms=finalDisSyms,diseasesTips=diseasesTips,specialist=specialist)
    else:
        flash(f'Sorry your symptoms dosn\'t match any disease, try again!','danger')
        return redirect(url_for('home'))


@app.route('/map', methods=['POST','GET'])
def goolge_map():
    address = address_value = "Cairo"
    if request.method == 'POST':
        address = address_value = request.form['map-address']
        address = address.replace(' ','+')
    return render_template('google-map.html',address=address,address_value=address_value)


@app.route('/feedback',methods=['POST'])
def feedback():
    if 'email' not in session:
        return redirect(url_for('login'))
    else:
        msg = request.form['feedback']
        usermail = session['email']
        rate = request.form['rate']
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """INSERT INTO feedback (usermail,message,rate) VALUES (?,?,?)"""
        cur.execute(query_string, (usermail,msg,rate))
        con.commit()
        cur.close()
        flash(f'Feedback sent','success')
        return redirect(url_for('home'))

def getDiseaseData(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT * FROM diseases WHERE disease=?"""
    cur.execute(query_string, (disease,))
    diseases = cur.fetchall()
    cur.close()
    if len(diseases) > 0:
        return diseases[0]
    return []

def getAllSyms(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT symptom FROM symptoms WHERE disease=?"""
    cur.execute(query_string, (disease,))
    symptoms = cur.fetchall()
    cur.close()
    result = []
    if len(symptoms) > 0:
        for s in symptoms:
            result.append(s[0])
        return result
    return []

def getTips(disease):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT tips FROM tips WHERE disease=?"""
    cur.execute(query_string, (disease,))
    tips = cur.fetchall()
    cur.close()
    if len(tips) > 0:
        return tips[0][0]
    return []

def getPercent(mySymptoms,diseaseSymptoms):
    counter = 0
    for ms in mySymptoms:
        for ds in diseaseSymptoms:
            if ms == ds:
                counter +=1
    if len(diseaseSymptoms) == 0:
        return 0
    else :
        return int((counter * 100) / len(diseaseSymptoms))

def getSpecialist(organ):
    con = sqlite3.connect("mydatabase.db")
    cur = con.cursor()
    query_string = """SELECT specialist FROM specialist WHERE organ=?"""
    cur.execute(query_string, (organ,))
    specialist = cur.fetchall()
    cur.close()
    if len(specialist) > 0:
        return specialist[0][0]
    return ""

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        if form.validate_on_submit():
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            query_string = """SELECT * FROM user WHERE email=?"""
            cur.execute(query_string, (form.email.data,))
            users = cur.fetchall()
            if len(users) > 0:
                flash(f'Email used before!','danger')
                return render_template('register.html', form=form)
            query_string = """INSERT INTO user (firstName,lastName,email,sex,age,password,accountType) VALUES(?,?,?,?,?,?,?)"""
            cur.execute(query_string, (form.firstName.data,form.lastName.data,form.email.data,
                                                    form.gender.data,form.age.data,form.password.data,form.acc_type.data))
            con.commit()
            con.close()
            flash(f'Account created for {form.firstName.data}!','success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/edit-profile', methods=['POST','GET'])
def edit_profile():
    form = RegistrationForm()
    if request.method == 'GET' and 'email' in session:
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """SELECT * FROM user WHERE email =?"""
        cur.execute(query_string, (session['email'],))
        user = cur.fetchall()
        con.close()
        return render_template('edit-profile.html',form=form,uFirstname=user[0][1],uLastname=user[0][2],
                        uEmail=user[0][3],uSex=user[0][5],uAge=user[0][6],uAccType=user[0][7])
    if request.method == 'POST':
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """UPDATE user SET firstName=?,lastName=?,age=?,password=? WHERE email=?"""
        cur.execute(query_string, (request.form['firstName'],request.form['lastName'],request.form['age'],request.form['password'],session['email']))
        con.commit()
        flash(f'Account updated!','success')
        return redirect(url_for('home'))
    
    return redirect(url_for('home'))
    


@app.route('/add-disease', methods=['GET','POST'])
def add_disease():
    if request.method == 'GET' and 'email' in session:
        if session['accType'] == 'doctor':
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            cur.execute("SELECT organ FROM specialist")
            organs = cur.fetchall()
            return render_template('add-disease.html',organs=organs)
    elif request.method == 'POST':
        disease = request.form['dName']
        definition = request.form['dDefinition']
        organ = request.form['organ']
        degree = request.form['degree']
        tips = request.form['tips']
        symptoms = request.form.getlist('dSym[]')
        addDisease.add(disease,symptoms)
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """INSERT INTO diseases (disease,difinition,degree,organ) VALUES (?,?,?,?)"""
        cur.execute(query_string, (disease,definition,degree,organ))
        con.commit()
        query_string = """INSERT INTO tips (disease,tips) VALUES (?,?)"""
        cur.execute(query_string, (disease,tips))
        con.commit()
        for sym in symptoms:
            if sym != "":
                query_string = """INSERT INTO symptoms (disease,symptom) VALUES (?,?)"""
                cur.execute(query_string, (disease,sym))
                con.commit()
        con.close()
        flash(f'Disease added successfuy!','success')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'GET' and 'email' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        session.pop('visitor', None)
        if form.validate_on_submit():
            con = sqlite3.connect("mydatabase.db")
            cur = con.cursor()
            query_string = """SELECT * FROM user WHERE email=? AND password=?"""
            cur.execute(query_string, (form.email.data,form.password.data,))
            users = cur.fetchall()
            con.close()
            if len(users) > 0:
                session['email'] = form.email.data
                session['firstname'] = users[0][1]
                session['lastname'] = users[0][2]
                session['sex'] = users[0][5]
                session['age'] = users[0][6]
                session['accType'] = users[0][7]
                flash(f'Welcome back {users[0][1]}!','success')
                return redirect(url_for('home'))
            else :
                flash(f'Login Faild!','danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))

@app.route('/doctor-contacts',methods=['GET'])
def doctor_contacts():
    if 'email' in session:
        con = sqlite3.connect("mydatabase.db")
        cur = con.cursor()
        query_string = """SELECT firstName,lastName,email,specialization FROM user WHERE accountType = 'doctor'"""
        cur.execute(query_string)
        doctors = cur.fetchall()
        con.close()
        if len(doctors) > 0:
            return render_template('doctor-contacts.html',doctors=doctors)
        else:
            flash(f'Sorry no available doctor right now!','danger')        
    return redirect(url_for('home'))

@app.route('/search-disease',methods=['POST'])
def search_disease():
    if  request.method == 'POST' and 'email' in session:
        diseaseName = request.form['diseaseName']
        diseasesInfo = getDiseaseData(diseaseName)
        if len(diseasesInfo) > 0:
            diseasesSyms = getAllSyms(diseaseName)
            specialist = getSpecialist(diseasesInfo[4])
            diseasesTips = getTips(diseaseName)
            return render_template('search-disease.html',diseaseName=diseaseName,diseasesInfo=diseasesInfo,diseasesSyms=diseasesSyms,
                                                    specialist=specialist,diseasesTips=diseasesTips)
        else:
            flash(f'Disease not found, We will consider it soon!','danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    # app.run()
    app.run(debug=True)
