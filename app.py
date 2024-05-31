from flask import Flask, render_template

app = Flask(__name__)

#login route
@app.route('/')
def login():
    return render_template('login.html')

#Home page
@app.route('/home')
def home():
    return render_template('home.html')

#Add Customers
@app.route('/add_customer')
def addCustomer():
    return render_template('add_customer.html')

#Add Orders
@app.route('/add_order')
def addOrder():
    return render_template('add_order.html')







#Route for static files
@app.route('/static/<path:filename>')
def static_files(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
