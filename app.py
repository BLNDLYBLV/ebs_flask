from flask import Flask, redirect,render_template, request, abort
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('./index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if(request.method=='GET'):
        return render_template('./login.html')
    elif(request.method=='POST'):
        # print(request.form['email'])
        email=request.form['email']
        password=request.form['password']
        if( (not (email) or email=='') or (not (password) or password=='') ):
            return render_template('./login.html', error=True, error_msg='Credentials invalid')
        return redirect('/')

if __name__ == "__main__":
    from waitress import serve
    # serve(app,host="0.0.0.0",port="8000")
    app.run(debug=True)