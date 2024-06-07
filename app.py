from flask import Flask, render_template, request, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from send_sms import send_sms

from oidc import appConf
from db import get_db_connection

#For input sanitization
import bleach

app = Flask(__name__)


#Secret key conf
app.secret_key = appConf.get("FLASK_SECRET")


oauth = OAuth(app)
oauth.register(
    "myApp",
    client_id=appConf.get("OAUTH2_CLIENT_ID"),
    client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email"
    },
    server_metadata_url=f'{appConf.get("OAUTH2_ISSUER")}/.well-known/openid-configuration',

)

#login route
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        return oauth.myApp.authorize_redirect(redirect_uri=url_for("callback", _external=True))
    
    elif "user" in session:
        return redirect(url_for('home'))
    
    else:
        return render_template('login.html')

#OPIDC Callback route
@app.route('/callback')
def callback():

    token = oauth.myApp.authorize_access_token()
    session["user"] = token

    return redirect(url_for('home'))

#Home page
@app.route('/home')
def home():
    if "user" in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


#Add Customers route
@app.route('/add_customer', methods=['GET', 'POST'])
def addCustomer():
    if "user" in session:

        if request.method == 'POST':
            customer_name = request.form['name']
            customer_code = request.form.get('code')
            customer_phone = request.form.get('phone')

            # Sanitize the inputs to prevent XSS using bleach library
            customer_name = bleach.clean(customer_name)
            customer_code = bleach.clean(customer_code)
            customer_phone = bleach.clean(customer_phone)

            #get database connection
            db = get_db_connection()


            try:
                with db.cursor() as cursor:
                    sql = "INSERT INTO Customers (customer_name, customer_code, phone) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (customer_name, customer_code, customer_phone))
                    db.commit()
                    success = f"Customer '{customer_name}' added successfully!"
                return render_template('add_customer.html', success=success)
            except Exception as e:
                error = f"Error adding customer: {e}"
                return render_template('add_customer.html', error=error)
        
        return render_template('add_customer.html')
    
    else:
        return redirect(url_for('login'))

#Add Orders route
@app.route('/add_order', methods=['GET', 'POST'])
def addOrder():
    if "user" in session:

        if request.method == 'POST':
            customer_id = request.form['customer_id']
            item = request.form['item']
            amount = request.form['amount']

            # Sanitize the inputs to prevent XSS
            customer_id = bleach.clean(customer_id)
            item = bleach.clean(item)
            amount = bleach.clean(amount)

            #get database connection
            db = get_db_connection()

            # Insert order data into database
            try:
                with db.cursor() as cursor:
                    sql = "INSERT INTO Orders (customer_id, item, amount) VALUES (%s, %s, %s)"
                    cursor.execute(sql, (customer_id, item, amount))
                    db.commit()
                    success = "Order added successfully"

                    #Send sms Notification
                    send_sms().sending()

                    cursor.execute("SELECT * FROM Customers")
                    customers = cursor.fetchall()
                return render_template('add_order.html', success=success, customers=customers)
            except Exception as e:
                error =f"Error adding order: {e}"
                return render_template('add_order.html', error=error)
        else:
            #get database connection
            db = get_db_connection()

            # Insert order data into database
            try:
                with db.cursor() as cursor:
                    cursor.execute("SELECT * FROM Customers")
                    customers = cursor.fetchall()
                return render_template('add_order.html', customers=customers)
            except Exception as e:
                error =f"Error getting customers: {e}"
                return render_template('add_order.html', error=error)
    
    else:
        return redirect(url_for('login'))


#Logout Route
@app.route('/logout')
def logout():
    id_token = session['user']['id_token']
    session.clear()

    return redirect(
        appConf.get("OAUTH2_ISSUER")
        + "/protocol/openid-connect/logout?"
        + urlencode(
            {
                "post_logout_redirect_uri": url_for("login", _external=True),
                "id_token_hint": id_token
            },
            quote_via=quote_plus,
        )
    )

#Route for static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
