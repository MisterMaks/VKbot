from flask import Flask
from flask import request
from flask import abort
import MySQLdb
from secret import passSQL
#from flask import jsonify

app = Flask(__name__)

print('start')

def execute(command):
    passdb = passSQL()
    conn = MySQLdb.connect('danr0.mysql.pythonanywhere-services.com', 'danr0', passdb, 'danr0$default')
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    row = str(cursor.fetchall())
    conn.close()
    return str(row)



@app.route('/')
def mainpage():
    return 'PLS use /api'

@app.route('/api/', methods=['GET'])
def apipage():
    return "Choose the table: \n 'errors' = /api/err \n 'users' = /api/users"

@app.route('/api/', methods=['POST'])
def postapi():
    abort(400)


@app.route('/api/err/', methods=['GET'])
def errorsget():
    try:
        row = execute("SELECT * FROM errors")
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
        s = execute("SELECT count(*) FROM errors")
        s = s.replace("((",'').replace(",),)",'')
        return s
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/<int:id>', methods=['GET'])
def get_error(id):
    try:
        row = execute("SELECT * FROM errors WHERE id ="+str(id))
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
        execute("INSERT INTO errors VALUES (NULL, '"+str(l[0])+"', '"+str(l[1])+"', '"+str(l[2])+"'); ")
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/err/<int:id>', methods=['DELETE'])
def del_err(id):
    try:
        execute("DELETE FROM errors WHERE id ="+str(id))
        abort(200)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/err/<int:id>', methods=['PATCH'])
def patch_err(id):
    try:
        data = (request.data).decode("utf-8")
        if data == '':
            abort(400)
        execute("UPDATE errors SET err = '"+str(data)+"' WHERE id ="+str(id))
        abort(200)
    except Exception as e:
        return '500 '+str(e)

'''
@app.route('/api/req/', methods=['GET'])
def reqget():
    try:
        row = execute("SELECT * FROM requests")
        #row = str(cursor.fetchall())
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
        s = execute("SELECT count(*) FROM requests")
        #s = str(cursor.fetchall())
        s = s.replace("((",'').replace(",),)",'')
        return s
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/req/<int:id>', methods=['GET'])
def get_req(id):
    try:
        row = execute("SELECT * FROM requests WHERE id ="+str(id))
        #row = str(cursor.fetchall())
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
        execute("INSERT INTO requests VALUES (NULL, '"+str(l[0])+"', '"+str(l[1])+"', '"+str(l[2])+"') ")
        #conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/req/<int:id>', methods=['DELETE'])
def del_req(id):
    try:
        execute("DELETE FROM requests WHERE id ="+str(id))
        #conn.commit()
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
        execute("UPDATE requests SET text = '"+str(data)+"' WHERE id ="+str(id))
        #conn.commit()
        abort(200)
    except Exception as e:
        return '500 '+str(e)



#print(errorsget(cursor))
#conn.close
'''
@app.route('/api/users/', methods=['GET'])
def userget():
    try:
        row = execute("SELECT * FROM users")
        t = row.split('), (')
        t[0] = t[0].replace('((','')
        t[-1] = t[-1].replace('))','')
        row = ''
        for el in t:
            row = row + str(el)+'\n'
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/users/count', methods=['GET'])
def usergetall():
    try:
        s = execute("SELECT count(*) FROM users")
        s = s.replace("((",'').replace(",),)",'')
        return s
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        row = execute("SELECT * FROM users WHERE id ="+str(id))
        return str(row)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/users/', methods=['POST'])
def userpost():
    try:
        data = (request.data).decode("utf-8")
        l = data.split('$')
        if len(l) != 2:
            abort(400)
        execute("INSERT INTO users VALUES ('"+str(l[0])+"', '"+str(l[1])+"') ")
        abort(200)
    except Exception as e:
        return '500 '+str(e)


@app.route('/api/users/<int:id>', methods=['DELETE'])
def del_user(id):
    try:
        execute("DELETE FROM users WHERE id ="+str(id))
        abort(200)
    except Exception as e:
        return '500 '+str(e)

@app.route('/api/users/<int:id>', methods=['PATCH'])
def patch_user(id):
    try:
        data = (request.data).decode("utf-8")
        if data == '':
            abort(400)
        execute("UPDATE users SET status = '"+str(data)+"' WHERE id ="+str(id))
        abort(200)
    except Exception as e:
        return '500 '+str(e)
