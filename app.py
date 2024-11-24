from flask import Flask,render_template,request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='naveenumasankar$26'
app.config['MYSQL_DB']='patient'
mysql = MySQL(app)


@app.route("/test" , methods=['POST','GET'])
def test():
    if request.method == 'POST':
        a = request.form
        name = a['name']
        age = a['age']
        gender = a['gender']
        symp = a['symp']
        hist = a['hist']
    else:
        print('hello')
    return render_template('test.html',res='Test1')
    # with app.app_context():
    #     cur1 = mysql.connection.cursor()
    #     rs = cur1.execute("SELECT * FROM finaldb")
    #     if(rs>0):
    #             det=cur1.fetchall()
    #             a=request.form
    #             name = a['name']
    #             age = a['age']
    #             gender = a['gender']
    #             symp = a['symp']
    #             hist = a['hist']
    #             str1=symp+" "+hist
    #             str1=str1.split()
    #             finallist=[]
    #             for i in det:
    #                 count=0
    #                 gsymp=i[0]
    #                 gsymp=gsymp.split()
    #                 for j in str1:
    #                     if j in gsymp:
    #                         count=count+1
    #                 list.append(count)
    #                 list.append(i[1])
    #                 finallist.append(list)
    #             finallist.sort(reverse=True)
    #            # sql.connection.commit()
    #             cur1.close()


if __name__ == '__main__':
    app.run(debug=True)