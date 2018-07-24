from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        hostname = request.form['hostname']
        return redirect(url_for('step2',hostname = hostname))

    return render_template('index.html')

@app.route('/step2', methods=['GET', 'POST'])
def step2():
    hostname = request.args.get('hostname')
    bashCommand = "df -h"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return render_template('step2.html',hostname = hostname, output = repr(output), error = repr(error))

if __name__ == '__main__':
    app.run()
