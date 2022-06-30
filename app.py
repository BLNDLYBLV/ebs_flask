from flask import Flask, redirect,render_template, request, abort
app = Flask(__name__)
# app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def dashboard():
    return render_template('./dashboard.html')

@app.route('/reporting/ebs')
def reporting_ebs():
    return render_template('./reporting_ebs.html')

@app.route('/reporting/other')
def reporting_other():
    return render_template('./reporting_other.html')

@app.route('/backup')
def backup():
    return render_template('./backup.html')

@app.route('/applineage')
def appLineage():
    return render_template('./applineage.html')

# @app.route('/getVolumeMap')
# def getVolumeMap():
#     return render_template('./.html')

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
    serve(app,host="0.0.0.0",port="8000")
    # app.run(debug=True)