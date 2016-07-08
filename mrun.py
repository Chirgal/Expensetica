# -*- coding: utf-8 -*-
"""
Created on Wed May  4 13:15:59 2016

@author: Chirgal.Hansdah
"""

from mongodef import *
from pymongo import errors
from flask import redirect, render_template, request, session,url_for,abort
import os
import datetime
import hashlib

cat=list(sorted(['Groceries', 'Restaurants', 'House Rent', 'Household Repairs', 'Electricity', 'Water', 'Phones', 'Cable', 'Internet', 
'Childrens Clothing', 'Adults Clothing', 'Fuel', 'Medicines', 'Health Insurance', 'Auto Insurance', 
'Life Insurance', 'Gym Memberships', 'Hair Cuts', 'Cosmetics', 'Salon Services', 'Personal Loan', 
'Car Loan', 'House Loan', 'Travel', 'Taxi', 'Tuition', 'Movies', 'Games', 'House Maid', 'Misc']))

######################Custom exception#################


###

### Ajax call handler to create expense item
@app.route('/createitem',methods=['POST'])
def create_item():
    
    if 'logged_in' in session:
       try: 
           post_catagory=str(request.form['catagory'])
           post_details=(request.form['details'])
           post_amount=float(request.form['amount'])
           post_date=datetime.datetime.strptime(request.form['expensedate'],'%m/%d/%Y')
           
           item = Item(catagory=post_catagory, details=post_details,amount=post_amount,)
           expense=Expense(user=session['logged_in'],date=post_date,items=[item])
           
           res=db.session.query(Expense).filter(Expense.date.in_(post_date),
                               Expense.user.in_(session['logged_in'])).first()
           
           if res is None:
               db.session.save(expense)
               return "Success"
           else:
               res=db.session.query(Expense).filter(Expense.date.in_(post_date),
                               Expense.user.in_(session['logged_in']))
               query=res.append('items',item)
               query.execute()
               return "Success"
       except:
            return "Error"
       
    else:
        return "Error"

               ######################Routers########################
@app.route('/')
def index():
    return redirect(url_for('home'))


###
@app.route('/home')
def home():
    global item_entry_info
    item_entry_info=[]
    if 'logged_in' in session:
        
        
        query = db.session.query(User).filter(User.email.in_(session['logged_in'])).first()
        if query:        
               return render_template('dashboard2.html',user=query,catagories=cat)
        else:
               return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

####
@app.route('/login',methods=['GET', 'POST'])    
def login():
 error=None
 if request.method == 'POST':
    POST_EMAIL = str(request.form['email'])
    POST_PASSWORD = str(request.form['password'])
    h = hashlib.md5()
    h.update(POST_PASSWORD.encode("utf-8"))
 
    
    try:
        query = db.session.query(User).filter(User.email.in_(POST_EMAIL),User.password.in_(h.hexdigest()) )
        result = query.first()
    except errors.ServerSelectionTimeoutError:
        abort(500)

    if result:
           session['logged_in'] = result.email
           return redirect(url_for('home'))
    else:
           error="Invalid email or password!"
           return render_template('login.html',error=error)
      
 else:
    return render_template('login.html')  


###
@app.route('/signup',methods=['GET', 'POST'])	
def signup():
    info=None
    if request.method == 'POST':
         POST_FIRSTNAME = str(request.form['firstName']).upper()
         POST_LASTNAME =  str(request.form['lastName']).upper()
         POST_EMAIL = str(request.form['email'])
         POST_PASSWORD = str(request.form['password'])
         POST_CONFIRM_PASSWORD=str(request.form['confirmPassword'])
         h = hashlib.md5()
         h.update(POST_PASSWORD.encode("utf-8"))
         #
         # input validation will go here
         #
         
         #Register user 
         user = User(firstname=POST_FIRSTNAME,lastname=POST_LASTNAME,
                     email=POST_EMAIL,password=h.hexdigest(),catagories=cat)
         #db.session.add(user)
         db.session.save(user)
         info=str("Registered Successfully ! Sign in to acces your account.") 
         return render_template('login.html',info=info)
         
    return render_template('signup.html')

###
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))        

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)