from flask import Flask,render_template,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import datetime
# from flask_mail import Mail



with open("config.json","r") as c:
    params=json.load(c)['params']
local_server=True 


app = Flask(__name__, static_url_path='/static')
app.secret_key = 'super-secret-key'
'''app.config.update(
    MAIL_SERVER ="smtp.gmail.com",
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME =params['gmail_user'],
    MAIL_PASSWORD =params['gmail_password']
)


mail=Mail(app)

'''


if(local_server):
    app.config["SQLALCHEMY_DATABASE_URI"] = params['local_uri']
else:
    app.config["SQLALCHEMY_DATABASE_URI"]=params['prod_uri']
db=SQLAlchemy(app)


class Contacts(db.Model):


    sno=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(12),nullable=False)
    email=db.Column(db.String(30),nullable=False)
    phone_num=db.Column(db.String(12),nullable=False)
    mes=db.Column(db.String(120),nullable=False)
    date=db.Column(db.String(20),nullable=False)



class Posts(db.Model):


    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(12),nullable=False)
    tagline=db.Column(db.String(20),nullable=False)
    slug=db.Column(db.String(30),nullable=False)
    content=db.Column(db.String(120),nullable=False)
    date=db.Column(db.String(20),nullable=False)
    img_file=db.Column(db.String(20),nullable=False)
@app.route("/")
def home():
    posts=Posts.query.filter_by().all()[0:params["no_of_posts"]]
    return render_template("index.html",params=params,posts=posts)

@app.route("/about")
def about():
    return render_template("about.html",params=params)

@app.route("/dashboard",methods=['GET','POST'])

def dashboard():
    if "user" in session and session['user']==params['admin_user']:
        posts = Posts.query.all()
        return render_template("dashboard.html", params=params, posts=posts)

    if request.method=="POST":
        username = request.form.get("uname")
        userpass = request.form.get("pass")
        if username==params['admin_user'] and userpass==params['admin_password']:
            # set the session variable
            session['user']=username
            posts = Posts.query.all()
            return render_template("dashboard.html", params=params, posts=posts)
    else:
        return render_template("login.html", params=params)

@app.route('/post/<string:postslug>', methods=['GET'])
def post_route(postslug):
    slug2 = str(postslug)
    post = db.session.query(Posts).filter_by(slug = slug2).first()
    return render_template('post.html', params=params, post=post)




'''
@app.route("/post/<string:post_slug>",methods=['GET'])
def post_route(post_slug):
    post=Posts.query.filter_by(slug=post_slug).first()
    return render_template("post.html",params=params,post=post)
'''
@app.route("/edit/<string:sno>",methods=['GET','POST'])
def edit(sno):
    if "user" in session and session['user']==params['admin_user']:
        if request.method =='POST':
            box_title =request.form.get("title")
            tline =request.form.get("tline")
            slug =request.form.get("slug")
            content =request.form.get("content")
            img_file =request.form.get("img_file")
            date= datetime.now()


            if sno=="0":
                post=Posts(title=box_title,slug=slug,content=content,tagline=tline,img_file=img_file,date=date)
                db.session.add(post)
                db.session.commit()
            else:

                post=Posts.query.filter_by(sno=sno).first()
                post.title=box_title
                post.slug=slug
                post.content=content
                post.tagline=tline
                post.img_file=img_file
                post.date=date
                db.session.commit()
                return redirect("/edit/"+sno)

        post=Posts.query.filter_by(sno=sno).first()
        return render_template("edit.html",params=params, post=post)

@app.route("/contact",methods=['GET','POST'])
def contact():

    if(request.method=='POST'):
        name=request.form.get('name')
        email=request.form.get('email')
        phone=request.form.get('phone')
        message=request.form.get('message')


        entry=Contacts(name=name,phone_num=phone,email=email,date=datetime.now(),mes=message)
    
        db.session.add(entry)
        db.session.commit()
        '''
        mail.send_message('New message from'+ name,
                          sender=email,
                          recipients=[params['gmail_user']],
                          body=message+"\n"+phone)
    '''
    
    return render_template("contact.html",params=params)

app.run(debug=True)