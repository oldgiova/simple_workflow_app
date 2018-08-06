from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)
from commands import commands

# index page: ask for first info
@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        install = request.form['choose1']
        return redirect(url_for('step2', install = install))

# step2 - first option
@app.route('/step2', methods=['GET', 'POST'])
def step2():
    if request.method == 'GET':
        install = request.args.get('install')
        return render_template('step2.html',install = install)
    elif request.method == 'POST':
        hostname = request.form['hostname']
        hostname2 = request.form['hostname2']
        # now put some logic here
        return redirect(url_for('step3',hostname = hostname))

@app.route('/step3', methods=['GET', 'POST'])
def step3():
    hostname = request.args.get('hostname')
    bashCommand = commands['who']
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return render_template('step3.html',hostname = hostname, output = repr(output), error = repr(error))

if __name__ == '__main__':
    app.run()
