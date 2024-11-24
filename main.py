from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import yaml
from Crypto.PublicKey import RSA

app = Flask(__name__)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='naveenumasankar$26'
app.config['MYSQL_DB']='patient'

mysql=MySQL(app)

def encpy(name,age,gender):
    n=0xdab209ad0b46324b8b5fe88c3684734b6b9b272056cca772150778000adf77b406bc94387bd36f23402596a44f09a294eb9cca53f3bd529420e7cf3b97470ea426f285cdee8863152eab3f0eee616d6eb28c8ad9b58287edb2cb773da7fbe34e00dcceefd0db5985eb4a1afd6d0548522c27f55af66a7a11aa94a528e779b761
    e=0x10001
    d=0x19cc8b7a2bbc8ff5dbff0834b440bb46302f4936162f45e89e24f7a9cf9e8da541ef30b01a2176f8aa5a54d354d49ee6a105e9d36e0b4d48d6b9e9f74e710e3fa4d8e0ea75d2fbbfa93b7d516f8f8c35a58e3cdd7b26e3b993ffab811333687153c0a6ac4f69858a8afd2361d7130537f04e6b227f80937764bb3e756ca416bd
    from hashlib import sha512
    name = bytes(name, 'utf-8')
    hash = int.from_bytes(sha512(name).digest(), byteorder='big')
    signature = pow(hash,d,n)
    age = bytes(age, 'utf-8')
    hash1 = int.from_bytes(sha512(age).digest(), byteorder='big')
    signature1 = pow(hash1, d, n)
    gender = bytes(gender, 'utf-8')
    hash2 = int.from_bytes(sha512(gender).digest(), byteorder='big')
    signature2 = pow(hash2, d, n)
    return signature,signature1,signature2;

@app.route('/' , methods=['GET','POST'])
def index():
    if request.method=='POST':
        a=request.form
        name=a['name']
        age=a['age']
        gender=a['gender']
        symp=a['symp']
        hist = a['hist']
        test = a['test']
        cur=mysql.connection.cursor()
        b,c,d=encpy(name,age,gender)
        print(type(b))
        cur.execute("INSERT INTO patdet(name,age,gender,hist,symp,test) VALUES(%s,%s,%s,%s,%s,%s)",(str(b),str(c),str(d),symp,hist,test))
        mysql.connection.commit()
        cur.close()
    return render_template('entryform.html')

@app.route('/user')
def user():
    cur = mysql.connection.cursor()
    rs=cur.execute("SELECT * FROM patdet")
    if rs>0:
        det=cur.fetchall()
        for i in det:
            res=i[5]
            symp=i[4]
            hist=i[3]
            symp=symp.split()
            hist=hist.split()
            count1 = 0
            count2 = 0
            count3 = 0
            count4 = 0
            count5 = 0
            list = ['genetic', 'sexual contact', 'blood transfusion', 'liver failure']
            list1 = ['drug overdose', 'pregnancy']
            list2 = ['genetic', 'dryness', 'children']
            list3 = ['fatty liver', 'alcohol']
            list4 = ['itching', 'leg enlargement', 'bleeding']
            for j in symp:
                if(j in list):
                    count1 = count1 + 1
            for j in symp:
                if(j in list1):
                    count2 = count2 + 1
            for j in symp:
                if(j in list2):
                    count3 = count3 + 1
            for j in symp:
                if(j in list3):
                    count4 = count4 + 1
            for j in symp:
                if(j in list4):
                    count5 = count5 + 1

            percentage = count1 / len(list)
            percentage1 = count2 / len(list1)
            percentage2 = count3 / len(list2)
            percentage3 = count4 / len(list3)
            percentage4 = count5 / len(list4)
            finallist = [[percentage, "TEST1"], [percentage1, "TEST2"], [percentage2, "TEST3"],
                         [percentage3, "TEST4"], [percentage4, "TEST5"]]
            finallist.sort(reverse=True)
            ans=finallist[0][1]
            print(ans)
            if(ans==res):
                query="SELECT gsymp FROM finaldb WHERE test=\'"+res+"\'"
                fn =cur.execute(query)
                temp=cur.fetchall()

                print('HI1')
                if(fn<=0):
                    str1=i[4]+" "+i[3]
                    cur.execute("INSERT INTO finaldb(gsymp,test) VALUES(%s,%s)",(str1,i[5]))
                    print('HI2')
                else:
                    #print(temp[0][0])
                    str1 = i[4] + " " + i[3]+" "+temp[0][0]
                    cur.execute("UPDATE finaldb set gsymp=\'"+str1+"\' where test=\'"+ans+"\'")
                    print('HI3')
            else:
                query="SELECT gsymp FROM finaldb where test=\'"+res+"\'"
                fn=cur.execute(query)
                temp1=cur.fetchall()
                print('HI4')

                if(fn<=0):
                    str1=i[4]+" "+i[3]
                    cur.execute("INSERT INTO finaldb(gsymp,test) VALUES(%s,%s)",(str1,res))
                    print('HI4')
                else:
                    str1 = i[4] + " " + i[3]+" "+temp1[0][0]
                    cur.execute("UPDATE finaldb set gsymp=\'"+str1+"\' where test=\'"+res+"\'")
                    print('HI5')
            mysql.connection.commit()
        cur.close()
    return 'Successfully Trained'
@app.route('/test' , methods=['GET','POST'])
def samp():
    flist = []
    if request.method=='POST':
        a=request.form
        name=a['name']
        age=a['age']
        gender=a['gender']
        symp=a['symp']
        hist = a['hist']
        # print(name,age,gender,symp,hist)
        str1 = symp + " " + hist
        str1 = str1.split()
        cur=mysql.connection.cursor()
        rs = cur.execute("SELECT * FROM finaldb")
        if(rs > 0):
            det = cur.fetchall()
            finallist=[]
            for i in det:
                llist=[]
                count=0
                gsymp=i[0]
                gsymp=gsymp.split()
                for j in str1:
                    if j in gsymp:
                        count=count+1
                llist.append(count)
                llist.append(i[1])
                finallist.append(llist)
            finallist.sort(reverse=True)

            for x in finallist:
                flist.append(x[1])

        mysql.connection.commit()
        cur.close()
    print(flist)
    return render_template('test.html',flist=flist)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(debug=True)


