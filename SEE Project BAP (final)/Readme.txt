How to use:
 - static directory has all the CSS files, images, etc...
 - templates directory has all the HTML files
 - in the root directory:
   . create_database.py is for creating the blog database, run it once in the starting
   . if you want to delete all data and start fresh, run caeate_database.py file
   . read_database.py is a debug file to read all the contents of blog.db and print it just to see if things are working.
   . main.py has the actual code of flask, run this file always. (only once for the first time run create_database.py)


Plan:
(Many Changes Will be made)

- Navigator Page
 . Hyperlinks to All the possible pages
 . If Logged in: homepage, dashboard, details page, Signout option
 . If Not Logged in: homepage, Login, Signin

- Home Page (blogs will be shown here)
 . All the Blogs will be shown here
 . For each blog- Like Option
 . On the top- Dashboard Link and Logout, Add new Blog Link

- Login Page (Basic UID and PWD)
 . UID, Pwd, Signin Button, Signup Redirect

- Signup Page
 . Name, UID, Pwd, Phno., Email ID

- Details Page
 . Shows all Details like Name, Email ID, Ph. No., UID
 . Allows to change Password

- Blog Page
 . Shows the entire blog
 . Shows all added comments, option to like the Blog, Number of likes, edit blog option

- Blog edit Page
 . Allows User to edit the entire blog
 . Deletion is allowed

- User Dashboard
 . Signout option
 . My written blogs
 . My liked blogs
 . My commented blogs
 . Details page option
 . Add new blog link


Database:
- Login Creds
 . Owner UID (primary Key, Autogenerate)
 . User ID
 . Name
 . Phone Number
 . Email ID
 . Password

- Blog
 . Blog UID (primary Key, Autogenerate)
 . Owner UID
 . Blog Title
 . Blog contents

- Comments
 . Comment UID (primary key, Autogenerate)
 . Owner UID
 . Blog UID
 . Comment contents

- Like
 . Like UID (primary key, Autogenerate)
 . Owner UID
 . Blog UID
 . (optional) comment UID (counting comment likes)


Later, try adding images as part of blog