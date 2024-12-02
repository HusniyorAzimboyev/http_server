import json
from http.server import HTTPServer,BaseHTTPRequestHandler
import sqlite3 as sql

class database:
    def __init__(self):
        self.conn = sql.connect("api.db")
        self.cur = self.conn.cursor()
    def get_all(self):
        self.cur.execute("SELECT * FROM users;")
        data = self.cur.fetchall()
        datam = [i[0] for i in self.cur.description]
        result = []
        for i in data:
            result.append(dict(zip(datam,i)))
        return result
    def delete_by_id(self,id):
        print("delete section")
        self.cur.execute("delete from users where id=?;",(id,))
        self.conn.commit()
    def new_user(self,data):
        self.cur.execute("insert into users(id,name,email) values (?,?,?);",(data['id'],data['name'],data['email']))
        self.conn.commit()
        print("new user section")
    def edit(self,data,id):
        data = data
        name = data["name"]
        email = data["email"]
        self.cur.execute("UPDATE users SET name=?,email=? WHERE id=?;",(name,email,id))
        self.conn.commit()
        print("succesfully updated!")
mydata = database()
data = mydata.get_all()
class myhttpserver(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/data":
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps(mydata.get_all()).encode())
        elif self.path.startswith("/data/"):
            id = int(self.path.split("/")[-1])
            for i in data:
                if i['id']==id:
                    self.send_response(200)
                    self.send_header("Content-Type","application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(i).encode())
                    break
            else:
                    self.send_error(404,"No data")

        else:
            self.send_response(404,"There is no such info")
            self.send_header("Content-type","application/json")
            self.end_headers()
    def do_POST(self):
        if self.path == '/data':
            content_length = int(self.headers['Content-Length'])
            print("content-length", content_length)
            post_data = self.rfile.read(content_length)
            new_item = json.loads(post_data.decode())
            new_item['id'] = mydata.get_all()[-1]['id'] + 1
            mydata.new_user(new_item)
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Location', '/data/{}'.format(new_item['id']))
            self.end_headers()
            self.wfile.write(json.dumps(new_item).encode())
        else:
           self.send_error(404)
    def do_PUT(self):
        if self.path.startswith("/data"):
            id = int(self.path.split('/')[-1])
            for i,item in enumerate(mydata.get_all()):
                if id==item["id"]:
                    print("putting...")
                    content_length = int(self.headers['Content-Length'])
                    newdata = json.loads(self.rfile.read(content_length).decode())
                    mydata.edit(id=id,data=newdata)
                    self.send_response(200)
                    self.send_header("Content-Type","application/json")
                    self.end_headers()
                    break
                else:
                    print("trying")
            else:
                self.send_response(404)
                print("error")
                self.send_header("Content-Type","text/HTML")
                self.wfile.write(bytes("<body><h1>No such column</h1></body>","utf-8"))
    def do_DELETE(self):
        user_id = int(self.path.split('/')[-1])
        for i in mydata.get_all():
            if user_id == i['id']:
                print("checking section")
                mydata.delete_by_id(user_id)
                self.end_headers()
                self.send_response(204)
                break
            else:
                print("no...")
        else:
            self.send_response(404)
SERVER = 'localhost'
HOST = 8000


htps = HTTPServer((SERVER,HOST),myhttpserver)
print("Server host on: 8000")
htps.serve_forever()
htps.server_close()
print('Server is closed..')