import datetime
from flask import Flask, flash, jsonify, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import time, date
import random
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import re


app=Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    rcno = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)

class Dchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Change_Date= db.Column(db.Date, nullable=False)
    Username_From = db.Column(db.String(200), nullable=False)
    RCNo_From = db.Column(db.String(50), nullable=False)
    email_From = db.Column(db.String(100), nullable=False)
    Duty_time_From = db.Column(db.Time, nullable=False)
    OTP_From = db.Column(db.String(100), nullable=False)
    Username_To = db.Column(db.String(200), nullable=False)
    RCNo_To = db.Column(db.String(50), nullable=False)
    email_To = db.Column(db.String(100), nullable=False)
    Duty_time_To = db.Column(db.Time, nullable=False)
    D_Status = db.Column(db.String(100), nullable=True)

class receiptnumber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receiptNo= db.Column(db.Integer, nullable=False)

class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float) 

class dailyUtilization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    today_Date= db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(200), nullable=False)
    airline_Name = db.Column(db.String(50), nullable=True)
    travelAgent = db.Column(db.String(50), nullable=True)
    flightNum = db.Column(db.String(50), nullable=True)
    Business_Pax = db.Column(db.Integer, nullable=True)
    walkin_Pax = db.Column(db.Integer, nullable=True)
    Other_Pax = db.Column(db.Integer, nullable=True)
    Total_pax = db.Column(db.Integer, nullable=True)    

class rates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    adultRateUSD= db.Column(db.Integer, nullable=False)
    KidRateUSD= db.Column(db.Integer, nullable=False)
    adultRateMVR= db.Column(db.Integer, nullable=False)
    KidRateMVR= db.Column(db.Integer, nullable=False)
    GSTRate= db.Column(db.Float, nullable=False)
    
    

class dailyUtilization1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    today_Date= db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(200), nullable=False)
    airline_Name = db.Column(db.String(50), nullable=True)
    travelAgent = db.Column(db.String(50), nullable=True)
    flightNumber = db.Column(db.String(50), nullable=True)
    business_Pax = db.Column(db.Integer, nullable=True)
    walkin_Pax = db.Column(db.Integer, nullable=True)
    other_Pax = db.Column(db.Integer, nullable=True)
    total_Pax = db.Column(db.Integer, nullable=True)  

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    today_Date= db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(200), nullable=False)
    paxName = db.Column(db.String(50), nullable=True)
    airlineName = db.Column(db.String(50), nullable=True)
    flightNumber = db.Column(db.String(50), nullable=True)
    seatNumber = db.Column(db.String(50), nullable=True)
    adultPax = db.Column(db.Integer, nullable=True)
    kidPax = db.Column(db.Integer, nullable=True)
    paymentType = db.Column(db.String(50), nullable=True)
    currencyType = db.Column(db.String(50), nullable=True)
    adultAmount = db.Column(db.Float, nullable=True)
    kidAmount = db.Column(db.Float, nullable=True)
    adultGST= db.Column(db.Float, nullable=True)
    kidGST= db.Column(db.Float, nullable=True)
    totalAmount= db.Column(db.Float, nullable=True)
    givenAmount= db.Column(db.Float, nullable=True)
    balanceAmount= db.Column(db.Float, nullable=True)
    approvalCode= db.Column(db.String(50), nullable=True)
    batchNumber= db.Column(db.String(50), nullable=True)
    receiptNumber =  db.Column(db.Integer, autoincrement=True)


class Shift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Shift_Date= db.Column(db.Date, nullable=False)
    Shift_Name = db.Column(db.String(200), nullable=False)
    Shift_Status = db.Column(db.String(50), nullable=False)
    
class Airlines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Airlines = db.Column(db.String(200), nullable=False)
    TravelAgents = db.Column(db.String(50), nullable=False)    
    FlightNum = db.Column(db.String(50), nullable=False)  


#Create String
    def __repr__(self):
          return '<Name %r>' % self.name
# Create the database tables     
with app.app_context():
    db.create_all()    



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    rcno = StringField('RCNo', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Length(min=6, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Sign Up') 

class ReceiptNoForm(FlaskForm):
    id = StringField('Id')
    receiptNumber= IntegerField('ReceiptNumber')

class NumberForm(FlaskForm):
    value = DecimalField('Number')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')   

class ShiftForm(FlaskForm):
    id = StringField('Id')
    Shift_Date = DateField('Shift Date', default=date.today, format='%Y-%m-%d')
    Shift_Name = SelectField('Shift Type', choices=[('Shift1', 'Shift1'), ('Shift2', 'Shift2')])
    Shift_Status = StringField('Shift_Status', validators=[DataRequired()])
    Shift_Status1 = StringField('Shift_Status1', validators=[DataRequired()])
    todayDate= DateField('Shift Date')
    shift1close = StringField('S1 Close')
    shift2close = StringField('S2 Close')
    shift1open = StringField('S2 Open')
    shift2open = StringField('S2 Open')
    


class paymentForm(FlaskForm):    
    id = StringField('Id') 
    todayDate = DateField('Date')
    shift= StringField('shift')
    code = StringField('Code')
    paxName= StringField('Name')
    airlineName= StringField('Airline')
    flightNumber= StringField('FlightNumber')
    seatNumber= StringField('Seat')
    adultPax= IntegerField('adultpax')
    kidPax= IntegerField('FlightNumber')
    paymentType= StringField('Paymenttype')
    currencyType= StringField('Currency')
    adultAmount= IntegerField('AdultAmount')
    kidAmount= IntegerField('KidAmount')
    adultGST= IntegerField('AdultGST')
    kidGST= IntegerField('KidGST')
    totalAmount= IntegerField('Total')
    givenAmount= IntegerField('GivenAmount')
    balanceAmount= IntegerField('Balance')
    approvalCode= StringField('Approval')
    batchNumber= StringField('Batch')
    receiptNumber= IntegerField('Receipt')    

class dailyUtilize(FlaskForm):
    id = StringField('Id')
    todayDate = DateField('Date')
    shift = StringField('Shift')
    airlineName = StringField('Airline')
    travelAgent = StringField('TravelAgent')
    flightNumber= StringField('FlightNumber')
    businessPax = IntegerField('Business Pax')
    walkinPax =  IntegerField('Walk-in')
    others = IntegerField('Others')
    totalPax = IntegerField('Total')

class dailyUtilize1(FlaskForm):
    id = StringField('Id')
    todayDate = DateField('Date')
    shift = StringField('Shift')
    airlineName = StringField('Airline')
    travelAgent = StringField('TravelAgent')
    flightNumber= StringField('FlightNumber')
    businessPax = IntegerField('Business Pax')
    walkinPax =  IntegerField('Walk-in')
    others = IntegerField('Others')
    totalPax = IntegerField('Total')

class DChangeForm(FlaskForm):
    id = StringField('Id')
    Username = StringField('Username')
    RCNo = StringField('RC Number')
    Change_Date = DateField('Date')
    email = StringField('email')   
    OTP_From =StringField('OTP_From')
    OTP_To =StringField('OTP_To')
    Status = StringField('Duty Status')

class EditForm(FlaskForm):
    RCNo_From = StringField('Login User')
    D_Status = StringField('Status')
    submit = SubmitField('Accept')

class ChangeForm(FlaskForm):
    id = StringField('Id')
    Change_Date= DateField('Date')
    Username = StringField('Username')
    RCNo = StringField('RC Number')
    email = StringField('email')
    Duty_time_From = TimeField('Time')    
    Username_To = SelectField('Select Username', coerce=int)
    RCNo_To = StringField('RC Number')
    email_To = StringField('email')
    Duty_time_To = TimeField('Time')    
    D_Status = StringField('Status')
    submit = SubmitField('Save to DChange') 
#Mail setup
def send_email(to_email, subject, body):
    # Your Gmail credentials
    sender_email = "inkl0509@gmail.com"
    password = "mdjy xsyh hgth vhrz"

    # Create a message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the body to the email
    message.attach(MIMEText(body, "plain"))

    # Establish a secure connection with the SMTP server
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Log in to the Gmail account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, rcno=form.rcno.data, email=form.email.data, password=hashed_password, is_approved=False)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please wait for approval.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

def get_open_shift_names():
    open_shift_names = Shift.query.filter_by(Shift_Status='Open').with_entities(Shift.Shift_Name).all()
    return open_shift_names

# Make open_shift_names available in the template context
@app.context_processor
def inject_open_shift_names():
    open_shift_names = get_open_shift_names()
    return dict(open_shift_names=open_shift_names)


@app.route('/num', methods=['GET', 'POST'])
def num():
    form = NumberForm()
    if form.validate_on_submit():
        new_number = Number(value=form.value.data)
        db.session.add(new_number)
        db.session.commit()
        return redirect(url_for('dashboard'))
    numbers = Number.query.all()
    return render_template('num.html', form=form, numbers=numbers)

@app.route('/get_airlines_and_agents')
def get_airlines_and_agents():
    airlines = [row.Airlines for row in Airlines.query.all()]
    travel_agents = [row.TravelAgents for row in Airlines.query.all()]
    flight_numbers = [row.FlightNum for row in Airlines.query.all()]

    response_data = {
        'airlineName': airlines,
        'travel_agents': travel_agents,
        'flight_numbers': flight_numbers
    }

    return jsonify(response_data)

@app.route('/get_usernames')
def get_usernames():
    usernames = [user.username for user in User.query.all()]
    return jsonify({'usernames': usernames})

@app.route('/draw', methods=['GET', 'POST'])
def draw():
    

    return render_template('participants.html')

@app.route('/slide')
def slide():
    return render_template('slide.html')



    return render_template('slide.html')

@app.route('/get_user_data/<username>')
def get_user_data(username):
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({'email': user.email, 'rcno': user.rcno})
    else:
        return jsonify({'error': 'User not found'}), 404



@app.route('/get_shift_data')
def get_shift_data():
    shift_name = request.args.get('Shift_Name')
    # Assuming Shift is your model, replace it with the actual model name
    shift_status = Shift.query.filter_by(Shift_Name=shift_name).first().Shift_Status
    return jsonify({"Shift_Status": shift_status})
    
@app.route('/')
def home():
    
    
    return redirect(url_for('dashboard'))

@app.route('/changeduty', methods=['GET', 'POST'])
def changeduty():
    form = ChangeForm()

    if request.method == 'POST' and form.validate_on_submit():

        new_change = Dchange(Change_Date=form.Change_Date.data,
                             Username_From=form.Username.data,
                             RCNo_From=form.RCNo.data,
                             email_From=form.email.data,
                             Duty_time_From=form.Duty_time_From.data,
                             Username_To=form.Username_To.data,
                             RCNo_To=form.RCNo_To.data,
                             email_To=form.email_To.data,
                             Duty_time_To=form.Duty_time_To.data,
                             D_Status=form.D_Status.data,
                             )
        db.session.add(new_change)
        db.session.commit()
        # Access form data using form.data
        # Perform actions with the form data (e.g., save to database)
        # Redirect to a new page or render a success message
        return redirect(url_for('dashboard'))

    return render_template('Dchange.html', form=form)
      
@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form=paymentForm()
    data = rates.query.filter_by().all()
    RNo = receiptnumber.query.filter_by().first().receiptNo
    receipt_entry = receiptnumber.query.first()
    if request.method == 'POST':
        
        Todate=form.todayDate.data
        shift=form.shift.data
        receiptNumber = RNo + 1
        code = form.code.data
        paxName = form.paxName.data
        airlineName = form.airlineName.data
        flightNumber = form.flightNumber.data
        seatNumber = form.seatNumber.data
        adultPax = form.adultPax.data
        kidPax = form.kidPax.data
        paymentType = form.paymentType.data
        currencyType = form.currencyType.data
        totalAmount = form.totalAmount.data
        givenAmount = form.givenAmount.data
        balanceAmount = form.balanceAmount.data
        adultAmount = form.adultAmount.data
        kidAmount = form.kidAmount.data
        adultGST = form.adultGST.data
        kidGST = form.kidGST.data
        kidGST = form.kidGST.data

        receipt_entry.receiptNo = receiptNumber
        
        paymententry=Payment(today_Date=Todate, shift=shift, receiptNumber=receiptNumber,
                                   paxName=paxName, airlineName=airlineName, flightNumber=flightNumber,
                                   seatNumber=seatNumber, adultPax=adultPax, kidPax=kidPax,
                                   paymentType=paymentType, currencyType=currencyType, totalAmount=totalAmount,
                                   givenAmount=givenAmount, balanceAmount=balanceAmount, adultAmount=adultAmount,
                                   kidAmount=kidAmount, adultGST=adultGST, kidGST=kidGST, code=code)
        
                                   
        db.session.add(receipt_entry)
        db.session.add(paymententry)
        db.session.commit()
        
        return redirect (url_for('payment'))  


    return render_template('payment.html', form=form, data=data, RNo=RNo)



@app.route('/shift', methods=['GET', 'POST'])
@login_required
def shift():
    form = ShiftForm()
    current_date = date.today()
    shift_to_update = Shift.query.filter_by(Shift_Name='Shift1').all()
    if request.method == 'POST':
        status=form.Shift_Status.data
   
        

    return render_template('shiftmanagement.html', form=form, current_date=current_date )


@app.route ('/entry', methods=['GET', 'POST'])
@login_required
def entry():
    form=dailyUtilize1()
    current_date = date.today()
    data = dailyUtilization1.query.filter_by(today_Date=current_date).all()
    
    if request.method == 'POST' and form.validate_on_submit():
        
        Todate=form.todayDate.data
        shift=form.shift.data
        airline_Name=form.airlineName.data
        travelAgent=form.travelAgent.data
        flightNumber=form.flightNumber.data
        businessPax=form.businessPax.data
        walkin_Pax=form.walkinPax.data
        other_Pax=form.others.data
        total_Pax = businessPax + walkin_Pax + other_Pax
        
        newentry=dailyUtilization1(today_Date=Todate, shift=shift, airline_Name = airline_Name,
                                   travelAgent = travelAgent, flightNumber=flightNumber, business_Pax=businessPax,
                                   walkin_Pax=walkin_Pax, other_Pax=other_Pax,total_Pax=total_Pax)
        db.session.add(newentry)
        db.session.commit()
        
        return redirect (url_for('entry'))  

    return render_template('entry.html', form=form, current_date=current_date, data=data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        rcno = current_user.rcno

        current_date = date.today()
        open_shift_names = request.args.get('Shift_Name')

        data = Dchange.query.filter_by(RCNo_To=rcno, D_Status="requested").all()
        shift = Shift.query.filter_by(Shift_Name=open_shift_names, Shift_Date=current_date).first()

        
        return render_template('dashboard.html', user=current_user, data=data, shift=shift)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


def generate_otp():
    return str(random.randint(100000, 999999))
  

@app.route('/DutyChange' , methods = ['GET', 'POST'])
@login_required
def DutyChange():
    form = ChangeForm()
    generated_otp = generate_otp()
    
    if request.method == 'POST' and form.validate_on_submit():
        User_to_check = form.RCNo.data
        Date_to_check = form.Change_Date.data
        existing_user = Dchange.query.filter_by(RCNo_From=User_to_check, Change_Date=Date_to_check ).first()
        
        if existing_user:
            flash('User has a request for the same date.')
        else:
        #get data from Form
            User_id = form.id.data
            ChangeDate = form.Change_Date.data
            Username = form.Username.data
            RCNo = form.RCNo.data
            D_From_email = form.email.data
            DT_F = form.Duty_time_From.data
            OTP_F = form.OTP_From.data
            Username_To = form.Username_To.data
            RCNo_To = form.RCNo_To.data
            email_To = form.email_To.data
            DT_T = form.Duty_time_To.data
            D_Status = 'requested'

            #email
                       
            new_user2 = Dchange(Change_Date= ChangeDate, Username_From= Username, RCNo_From= RCNo,
                                email_From= D_From_email, Duty_time_From= DT_F, OTP_From= OTP_F,
                                Username_To= Username_To, RCNo_To= RCNo_To, email_To= email_To,
                                Duty_time_To= DT_T, D_Status= D_Status )
            db.session.add(new_user2)
            db.session.commit()
            
            flash('User registered successfully.')
        return redirect(url_for('DutyChange')) #redirect to same page after submission
            
    return render_template('DutyChange.html', form=form, generated_otp=generated_otp )
   


@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_data(item_id):
   
    item = Dchange.query.get_or_404(item_id)
    form = EditForm(obj=item)

    if form.validate_on_submit():
        # Collect data from the form and update the item attributes
        item.RCNo_From = form.RCNo_From.data
       # item.Username_From = form.Username_From.data
        item.D_Status = 'Approved'
        to_email =  'iirufan@gmail.com'
        body =   item.Username_From +' ('+ item.RCNo_From + ') ' + ' --> ' + str(item.Duty_time_To) + ' and ' + item.Username_To + ' (' + item.RCNo_To + ') ' +  ' --> ' + str(item.Duty_time_From) + ' on ' + str(item.Change_Date)
        subject = 'Duty Change'
        
        db.session.commit()
        send_email(to_email, subject, body)
        flash('Duty change updated successfully')
        return redirect(url_for('dashboard'))

    return render_template('edit_data.html', form=form, item=item)
    
@app.route('/shiftchange/<int:item_id>', methods=['GET', 'POST'])
@login_required
def shiftchange(item_id):
   
    item = Shift.query.get_or_404(item_id)
    form = ShiftForm(obj=item)
    current_date = date.today() 
    shift1="Shift1"
    Open1="Open"
    
    dataforshift1 = Shift.query.filter_by(Shift_Name=shift1).all()
    dataforopenshift = Shift.query.filter_by(Shift_Status=Open1).all()
    if form.validate_on_submit():
        # Collect data from the form and update the item attributes
        item.Shift_Date = form.todayDate.data
        item.Shift_Status = form.Shift_Status1.data
       # item.Username_From = form.Username_From.data

        db.session.commit()
        
        flash('updated successfully')
        return redirect(url_for('shift'))

    return render_template('shiftchange.html', form=form, item=item, dataforshift1=dataforshift1, dataforopenshift=dataforopenshift)



if __name__ == '__main__':
      
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))



