from flask import Flask, url_for, render_template, request, flash, redirect, session, abort
import subprocess, os, logging 
from commands import commands

import ipdb

logging.basicConfig(
    filename='server.log',
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
    )
app = Flask(__name__)

# index page: ask for first info
@app.route('/', methods=['GET','POST'])
def main():
    if not session.get('logged_in'):
        logging.warn('User not logged in')
        return render_template('login.html')
    else:
        if request.method == 'GET':
            logging.debug('get index page')
            return render_template('index.html')
        elif request.method == 'POST':
            install = request.form['choose1']
#            logging.info('You choosed {}').format(install)
            return redirect(url_for('step2', install = install))

# login step
@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        logging.info('Admin user login')
    else:
        flash('wrong password!')
        logging.warning('Wrong password')
    return redirect(url_for('main'))
#    return main()

# step2 - first option
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if not session.get('logged_in'):
        return render_template('login.html')
        logging.warn('User not logged in')
    else:
        if request.method == 'GET':
#            ipdb.set_trace()
            install = request.args.get('choose1')
            logging.info('You choosed {}'.format(install))
            return render_template('step2.html',install = install)
        elif request.method == 'POST':
            hostname = request.form['hostname']
            hostname2 = request.form['hostname2']
            print(hostname)
            print(hostname2)
            return redirect(url_for('step3',hostname = hostname))

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    if not session.get('logged_in'):
        return render_template('login.html')
        logging.warn('User not logged in')
    else:
        hostname = request.args.get('hostname')
        hostname2 = request.args.get('hostname2')
        logging.info('hostname 1: {}'.format(hostname))
        if hostname2: 
            logging.info('hostname 2: {}'.format(hostname2))
        bashCommand = commands['who']
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        return render_template(
                'step3.html',
                hostname = hostname, 
                output = repr(output), 
                error = repr(error)
                )

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(
            debug=True,
            host='0.0.0.0',
            port=5000
            )
