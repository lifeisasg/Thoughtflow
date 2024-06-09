# importing libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
 
# creating a flask app instance
app = Flask(__name__)
 
'''Database handling'''
# creating a new account
def insert_creds(name, phone, email, userid, password):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT User_ID FROM Login_Creds WHERE User_ID = ?", (userid,))
    row = cursor.fetchone()
    if row:
        conn.close()
        return -1
    else:
        cursor.execute("""
            INSERT INTO Login_Creds (User_ID, Name, Phone_Number, Email_ID, Password)
            VALUES (?, ?, ?, ?, ?)
        """, (userid, name, phone, email, password))
        conn.commit()
        conn.close()
        return 0
 
# logging in
def chk_creds(userid, password):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Password FROM Login_Creds WHERE User_ID=?", (userid,))
    result = cursor.fetchone()
    if result:
        if result[0] == password:
            conn.close()
            return "access"
        else:
            conn.close()
            return "wrong password"
    else:
        conn.close()
        return "no user"
 
# creating a new blog
def createblog(title, content):
    global uid
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID FROM Login_Creds WHERE User_ID = ?", (uid,))
    owner_uid = cursor.fetchone()[0]
    cursor.execute("INSERT INTO Blog (Owner_UID, Blog_Title, Blog_contents) VALUES (?, ?, ?)", (owner_uid, title, content))
    conn.commit()
    blog_uid = cursor.lastrowid
    conn.close()
    return blog_uid
 
# fetching a blog
def fetchblog(blog_uid):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID, Blog_Title, Blog_contents FROM Blog WHERE Blog_UID=?", (blog_uid,))
    result = cursor.fetchone()
    if result:
        owner_uid, blog_title, blog_content = result
        cursor.execute("SELECT Name FROM Login_Creds WHERE Owner_UID=?", (owner_uid,))
        result1 = cursor.fetchone()
        name = result1[0]
        conn.close()
        return [blog_title, name, blog_content]
    else:
        conn.close()
        return [-1]
 
# deleting a blog
def deleteblog(blogid):
    # delete the comments first
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Comments WHERE Blog_UID = ?", (blogid,))
    cursor.execute("DELETE FROM Blog WHERE Blog_UID = ?", (blogid,))
    conn.commit()

# fetch comments
def fetchcomments(blog_uid):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("""
            SELECT Owner_UID, Comment_contents 
            FROM Comments 
            WHERE Blog_UID = ?
    """, (blog_uid,))
    comments = cursor.fetchall()
    cursor.execute("""
            SELECT Owner_UID, User_ID
            FROM Login_Creds
    """)
    usernames = dict(cursor.fetchall())
    conn.close()
    comments_list = []
    for owner_id, contents in comments:
        if owner_id in usernames:
            username = usernames[owner_id]
            comments_list.append([username, contents])
    return comments_list
 
# add a new comment
def addcomment(blogid, comment):
    global uid
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID FROM Login_Creds WHERE User_ID = ?", (uid,))
    owner_uid = cursor.fetchone()[0]
    cursor.execute("INSERT INTO Comments (Owner_UID, Blog_UID, Comment_contents) VALUES (?, ?, ?)",
                                    (owner_uid, blogid, comment))
    conn.commit()
    conn.close()
 
# fetch all the blogs
def fetchallblogs():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Blog_UID, Owner_UID, Blog_Title, Blog_contents FROM Blog")
    all_blogs = cursor.fetchall()
    blog_list = []
    # [blog_id, title, contents, author]
    for blog in all_blogs:
        list = [blog[0], blog[2], blog[3]]
        cursor.execute("SELECT Name FROM Login_Creds WHERE Owner_UID = ?", (blog[1],))
        list.append(cursor.fetchone()[0])
        blog_list.append(list)
    conn.close()
    return blog_list
 
# fetch my blogs
def fetchmyblogs():
    global uid
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID FROM Login_Creds WHERE User_ID = ?", (uid,))
    owner_uid = cursor.fetchone()[0]
    cursor.execute("SELECT Blog_UID, Blog_Title, Blog_contents FROM Blog WHERE Owner_UID = ?", (owner_uid,))
    all_blogs = cursor.fetchall()
    blog_list = []
    # [blog_id, title, content]
    for blog in all_blogs:
        blog_list.append([blog[0], blog[1], blog[2]])
    conn.close()
    return blog_list
 
# fetching my commented blogs
def fetchmycommentedblogs():
    # [blog_id, title, content]
    global uid
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID FROM Login_Creds WHERE User_ID = ?", (uid,))
    owner_uid = cursor.fetchone()[0]
    cursor.execute("SELECT Blog_UID, Comment_contents FROM Comments WHERE Owner_UID = ?", (owner_uid,))
    result = cursor.fetchall()
    commentdict = {} # {blogid: [blog title, [comment1, comment2, ...]]}
    for iterable in result:
        if iterable[0] in commentdict:
            commentdict[iterable[0]].append(iterable[1])
        else:
            commentdict[iterable[0]] = [iterable[1]]
    for key, value in commentdict.items():
        commentdict[key] = [fetchblog(key)[0], value]
    return commentdict
 
# check edit access:
def chkedit(blogid):
    global uid
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Owner_UID FROM Login_Creds WHERE User_ID = ?", (uid,))
    owner_uid = cursor.fetchone()[0]
    cursor.execute("SELECT Owner_UID FROM Blog WHERE Blog_UID = ?;", (blogid,))
    if owner_uid == cursor.fetchone()[0]:
        conn.close()
        return 1
    else:
        conn.close()
        return -1

# user-info
def user_info():
    global uid
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Name, User_ID, Phone_Number, Email_ID FROM Login_Creds WHERE User_ID = ?", (uid,))
    row = cursor.fetchone()
    conn.close()
    info = {'Name': row[0], 'Username': row[1], 'Email': row[3], 'Phone': row[2]}
    return info

# update a blog
def updateblog(blogid, title, content):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Blog SET Blog_Title=?, Blog_contents=? WHERE Blog_UID=?", (title, content, blogid))
    conn.commit()
    conn.close()


# global user ID and password
uid = None
pwd = None
 
 
'''App Handling'''
# default page
@app.route('/', methods=['GET'])
def landing():
    return redirect(url_for('home'))
 
# home page
@app.route('/home', methods=['GET'])
def home():
    blogs = fetchallblogs()
    status = None
    if uid:
        status = "True"
    return render_template("homepage.html", blog_posts = blogs, status = status)
 
# signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    global uid, pwd
    if uid:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        # getting details from form
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        userid = request.form['userid']
        password = request.form['password']
        # checking the database and updating details
        if insert_creds(name, phone, email, userid, password) == 0:
        # updating the global variables
            uid = userid
            pwd = password
            return redirect(url_for('dashboard'))
        else:
            return render_template('signup.html', error_message = "This user ID has been taken")
 
# login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    global uid, pwd
    if uid:
        return redirect(url_for('dashboard'))
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['userid']
        password = request.form['password']
        result = chk_creds(userid, password)
        if result == "access":
            uid = userid
            pwd = password
            return redirect(url_for('dashboard'))
        elif result == "no user":
            return render_template("login.html", error_message = "User ID not found")
        else:
            return render_template("login.html", error_message = "Wrong Password Entered")
 
# signout page
@app.route('/signout', methods = ['GET'])
def signout():
    global uid, pwd
    uid = pwd = None
    return redirect(url_for('home'))
 
# new blog
@app.route('/new-blog', methods = ['GET', 'POST'])
def newblog():
    global uid, pwd
    if uid == None:
        return redirect(url_for('login'))
    if uid and request.method == 'GET':
        return render_template('newblog.html')
    else:
        blog_title = request.form["blogTitle"]
        blog_content = request.form["blogContent"]
        blog_id = createblog(blog_title, blog_content)
        return redirect(url_for('blog', blogid = blog_id))
 
# display blog and add comment
@app.route('/blog-<blogid>', methods = ['GET', 'POST'])
def blog(blogid):
    global uid, pwd
    if request.method == 'GET':
            result = fetchblog(blogid)
            if result[0] == -1:
                return redirect(url_for('home'))
            comm = fetchcomments(blogid)
            if comm:
                pass
            else:
                comm = [["No Comments yet", "Be the first one to comment!"]]
            status = None
            if uid:
                status = "True"
            return render_template("blog.html", title = result[0], author = result[1], content = result[2], comments = comm, blogid = blogid, status = status)
    else:
        if uid:
            new_comment = request.form['new-comment']
            blog_id = request.form['blog-id']
            addcomment(blog_id, new_comment)
            return redirect(url_for('blog', blogid = blog_id))
        else:
            return redirect(url_for('login'))

# dashboard
@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    if uid:
        if request.method == "GET":
            return render_template("dashboard.html", myblogs = fetchmyblogs(), commentedblogs = fetchmycommentedblogs())
        else:
            blogid = request.form['blogid']
            deleteblog(blogid)
            return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
 
# edit blog page
@app.route('/edit-blog-<blogid>', methods = ['GET', 'POST'])
def edit_blog(blogid):
    blog = fetchblog(blogid)
    if (blog == [-1]):
        return redirect(url_for('home'))
    elif uid:
        if chkedit(blogid) == -1:
            return redirect(url_for('blog', blogid = blogid))
        elif request.method == "GET":
            return render_template('editblog.html', title = blog[0], content = blog[-1], blogid = blogid)
        else:
            blog_id = request.form['blog-id']
            title = request.form['blogTitle']
            content = request.form['blogContent']
            updateblog(blog_id, title, content)
            return redirect(url_for('blog', blogid = blog_id))
    else:
        return redirect(url_for('login'))

# user-info
@app.route('/myinfo', methods = ['GET'])
def userinfo():
    if uid:
        return render_template('myinfo.html', userinfo = user_info())
    else:
        return redirect(url_for('login'))
    

if __name__ == '__main__':
    app.run(debug=True)
