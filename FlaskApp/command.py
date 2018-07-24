from flask import Flask, render_template, request
import subprocess

bashCommand = "df -h"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
output, error = process.communicate()

print(repr(output))
