from flask import Flask
from flask import request
from flask import abort
import MySQLdb
from secret import passSQL
#from flask import jsonify

app = Flask(__name__)

print('start')
passdb = passSQL()
conn = MySQLdb.connect('danr0.mysql.pythonanywhere-services.com', 'danr0', passdb, 'danr0$default')
cursor = conn.cursor()


@app.route('/')
def mainpage():
    return 'PLS use /api'

@app.route('/api/', methods=['GET'])
def apipage():
    return "Choose the database: \n DB 'errors' = /api/err \n requests /api/req"

@app.route('/api/', methods=['POST'])
def postapi():
    abort(400)

@app.route('/api/err/', methods=['GET'])
def errorsget():
    try:
        cursor.execute("SELECT * FROM errors")
        row = str(cursor.fetchall())
        t = row.split('), (')
        t[0] = t[0].replace('((','')
        t[-1] = t[-1].replace('))','')
        row = ''
        for el in t:
            row = row + str(el)+'\n'
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/count', methods=['GET'])
def errgetall():
    try:
        cursor.execute("SELECT count(*) FROM errors")
        s = str(cursor.fetchall())
        s = s.replace("((",'').replace(",),)",'')
        return s
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/<int:id>', methods=['GET'])
def get_error(id):
    try:
        cursor.execute("SELECT * FROM errors WHERE id ="+str(id))
        row = str(cursor.fetchall())
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/', methods=['POST'])
def errorspost():
    try:
        data = (request.data).decode("utf-8")
        l = data.split('$')
        if len(l) != 3:
            abort(400)
        cursor.execute("INSERT INTO errors VALUES (NULL, '"+str(l[0])+"', '"+str(l[1])+"', '"+str(l[2])+"') ")
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/err/<int:id>', methods=['DELETE'])
def del_err(id):
    try:
        cursor.execute("DELETE FROM errors WHERE id ="+str(id))
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/<int:id>', methods=['PATCH'])
def patch_err(id):
    try:
        data = (request.data).decode("utf-8")
        if data == '':
            abort(400)
        cursor.execute("UPDATE errors SET err = '"+str(data)+"' WHERE id ="+str(id))
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/req/', methods=['GET'])
def reqget():
    try:
        cursor.execute("SELECT * FROM requests")
        row = str(cursor.fetchall())
        t = row.split('), (')
        t[0] = t[0].replace('((','')
        t[-1] = t[-1].replace('))','')
        row = ''
        for el in t:
            row = row + str(el)+'\n'
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/req/count', methods=['GET'])
def reqgetall():
    try:
        cursor.execute("SELECT count(*) FROM requests")
        s = str(cursor.fetchall())
        s = s.replace("((",'').replace(",),)",'')
        return s
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/req/<int:id>', methods=['GET'])
def get_req(id):
    try:
        cursor.execute("SELECT * FROM requests WHERE id ="+str(id))
        row = str(cursor.fetchall())
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/req/', methods=['POST'])
def reqpost():
    try:
        data = (request.data).decode("utf-8")
        l = data.split('$')
        if len(l) != 3:
            abort(400)
        cursor.execute("INSERT INTO requests VALUES (NULL, '"+str(l[0])+"', '"+str(l[1])+"', '"+str(l[2])+"') ")
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/req/<int:id>', methods=['DELETE'])
def del_req(id):
    try:
        cursor.execute("DELETE FROM requests WHERE id ="+str(id))
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)

#UPDATE `members` SET `contact_number` = '0759 253 542' WHERE `membership_number` = 1;
@app.route('/api/req/<int:id>', methods=['PATCH'])
def patch_req(id):
    try:
        data = (request.data).decode("utf-8")
        if data == '':
            abort(400)
        cursor.execute("UPDATE requests SET text = '"+str(data)+"' WHERE id ="+str(id))
        conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)



#print(errorsget(cursor))
#conn.close()
