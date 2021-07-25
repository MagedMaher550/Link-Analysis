from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap

import Vector_Space_Model

app = Flask(__name__)
Bootstrap(app)
 
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/',methods=['POST'])
def getValue():
    query = request.form['VectorQuery']
    mySearchRes = Vector_Space_Model.showAllRes()
    f = open("Q.txt" , 'w')
    f.write(query)
    f.close

    return render_template("index.html" , Res1= mySearchRes[0].replace('\n', '<br>'),Res2= mySearchRes[1].replace('\n', '<br>'),Res3= mySearchRes[2].replace('\n', '<br>'))