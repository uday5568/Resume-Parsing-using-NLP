import mysql.connector
from tkinter import *
import hashlib
import re
from tkinter import filedialog


class MainWindow:

    def __init__(self, mainWidget):
        self.root = mainWidget
        self.root.state('zoomed')
        self.gui_elements = []
        self.root['bg'] = '#012'

        try:
            mydb = mysql.connector.connect(host="localhost", user="root")
            db = mydb.cursor()
            sql = "CREATE DATABASE IF NOT EXISTS resumesparser"
            db.execute(sql)
            mydb.commit()
            mydb.close()
        except Exception as e:
            self.message("*Database Creation Failed",x=620, y=550)
        finally:
            self.resumeprocesssing()



    def login_gui(self):
        self.root.title('Login Page')
        self.gui_elements_remove(self.gui_elements)
        username_l = StringVar()
        password_l = StringVar()
        def fun():
            mydb = mysql.connector.connect(host="localhost", user="root", database='resumesparser')
            db = mydb.cursor()
            try:
                sql = "SELECT * FROM users"
                db.execute(sql)
                list_db = {}
                for i in db:
                    list_db[i[0]] = i[2]
                print(list_db,hashlib.md5(username_l.get().encode()).hexdigest())
                if list_db.get(hashlib.md5(username_l.get().encode()).hexdigest(), '') == hashlib.md5(
                        password_l.get().encode()).hexdigest():
                    self.resumeprocesssing()
                else:
                    self.message("*Incorrect Username or Password",x=650, y=430)
            except Exception as e:
                self.message("*Error Encountered", x=650, y=430)
            mydb.commit()
            mydb.close()
        login_x = 500
        login_y = 350
        self.gui_elements.append(Label(self.root, text='Resume Parser Using NLP', font=('Arial', 30)))
        self.gui_elements[-1].place(x=login_x, y=login_y - 170)
        # LOGIN
        self.gui_elements.append(Label(self.root, text='Login', width=15, font=('Arial', 18)))
        self.gui_elements[-1].place(x=login_x + 150, y=login_y - 70)

        self.gui_elements.append(
            Label(self.root, text="Username", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=10))
        self.gui_elements[-1].place(x=login_x, y=login_y)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=username_l))
        self.gui_elements[-1].place(x=login_x + 150, y=login_y)
        self.gui_elements.append(
            Label(self.root, text="Password", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=10))
        self.gui_elements[-1].place(x=login_x, y=login_y + 50)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=password_l))
        self.gui_elements[-1].place(x=login_x + 150, y=login_y + 50)

        self.gui_elements.append(Label(self.root, text="New User?", font=('Arial', 13), fg="#fff", bg="#012", width=10))
        self.gui_elements[-1].place(x=login_x + 150,
                                    y=login_y + 150)
        self.gui_elements.append(
            Button(self.root, text="Create Account", font=('Arial 12'), fg="#00f", bg="#012", bd="0",
                   command=self.signup_gui,
                   width=12, height=1))
        self.gui_elements[-1].place(x=login_x + 245, y=login_y + 150)

        self.gui_elements.append(
            Button(self.root, text="Login", font=('Arial 12'), command=fun, width=10, height=1))
        self.gui_elements[-1].place(x=login_x + 200, y=login_y + 110)
    def signup_gui(self):
        self.root.title('SignUp Page')
        self.gui_elements_remove(self.gui_elements)
        username_s = StringVar()
        email_s = StringVar()
        password_s = StringVar()
        re_password_s = StringVar()
        signup_x = 500
        signup_y = 350

        def fun():
            mydb = mysql.connector.connect(host="localhost", user="root", database='resumesparser')
            db = mydb.cursor()
            try:
                sql = '''CREATE TABLE IF NOT EXISTS `users` (
                  `username` varchar(250) NOT NULL ,   
                  `email` varchar(250) NOT NULL ,       
                  `password` varchar(250)  NOT NULL ,     
                   PRIMARY KEY  (`username`)
                );'''
                db.execute(sql)


            except Exception as e:
                self.message("*Table Creation Failed, Error Occured", x=signup_x + 200, y=signup_y + 80)

            try:
                if (username_s.get() and email_s.get() and password_s.get() and password_s.get() == re_password_s.get()):
                    sql = "SELECT username FROM users"
                    db.execute(sql)
                    if str(hashlib.md5(username_s.get().encode()).hexdigest()) in [i[0] for i in db]:
                        self.message('*Username Taken', x=signup_x + 150, y=signup_y+28)
                    else:
                        sql = "INSERT INTO users VALUES(MD5(%s),%s,MD5(%s))"
                        val = (username_s.get(), email_s.get(), password_s.get())
                        if re.search('[A-Z]', val[2]) and re.search('[a-z]', val[2]) and re.search('[0-9]',val[2]) and re.search(
                            '[@_!#$%^&*()<>?/|}{~:]', val[2]) and len(val[2]) >= 8:
                            db.execute(sql, val)
                            self.message("*Registration Successful", x=signup_x + 150, y=signup_y + 177, color='#00ff00')


                        else:
                            self.message('*Weak Password Try Again', x=signup_x + 150, y=signup_y + 130)

                else:
                    if (not username_s.get()):
                        self.message('Username Empty', x=signup_x + 150, y=signup_y + 28)
                    if (not email_s.get()):
                        self.message('Email Empty', x=signup_x + 150, y=signup_y + 78)
                    if (not password_s.get()):
                        self.message('password Empty', x=signup_x + 150, y=signup_y + 128)
                    elif (password_s.get() != re_password_s.get()):
                        self.message('*Password Don\'t match', x=signup_x + 150, y=signup_y + 180)
            except Exception as e:
                self.message(f"*Resgitration Failed,Error Occured", x=signup_x + 150, y=signup_y + 180)

            mydb.commit()
            mydb.close()

        self.gui_elements.append(Label(self.root, text='Resume Parser Using NLP', font=('Arial', 30)))
        self.gui_elements[-1].place(x=signup_x, y=signup_y - 170)
        self.gui_elements.append(Label(self.root, text='SignUp', width=15, font=('Arial', 18)))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y - 70)

        self.gui_elements.append(
            Label(self.root, text="Username", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=10))
        self.gui_elements[-1].place(x=signup_x, y=signup_y)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=username_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y)

        self.gui_elements.append(
            Label(self.root, text="Email", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=10))
        self.gui_elements[-1].place(x=signup_x, y=signup_y + 50)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=email_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y + 50)

        self.gui_elements.append(
            Label(self.root, text="Password", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=10))
        self.gui_elements[-1].place(x=signup_x, y=signup_y + 100)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=password_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y + 100)

        self.gui_elements.append(
            Label(self.root, text="Re-type Password", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=14))
        self.gui_elements[-1].place(x=signup_x - 70, y=signup_y + 150)
        self.gui_elements.append(Entry(self.root, width=25, font=('Arial 16'), textvariable=re_password_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y + 150)

        self.gui_elements.append(Label(self.root, text="Account Already Exist?", font=('Arial', 13), fg="#fff", bg="#012", width=20))
        self.gui_elements[-1].place(x=signup_x + 100,
                                    y=signup_y + 253)

        self.gui_elements.append(
            Button(self.root, text="Login here", font=('Arial 12'), fg="#00f", bg="#012", bd="0",
                   command=self.login_gui,
                   width=9, height=1))
        self.gui_elements[-1].place(x=signup_x + 280, y=signup_y + 250)

        self.gui_elements.append(Button(self.root, text="SignUp", font=('Arial 12'), command=fun, width=10, height=1))
        self.gui_elements[-1].place(x=signup_x + 200, y=signup_y + 210)
        self.root.mainloop()
    def resumeprocesssing(self):
        self.root.title('Resume Parser')
        self.gui_elements_remove(self.gui_elements)
        self.gui_elements.append(
            Entry(self.root, font=('Arial', 13), width=50))
        self.gui_elements[-1].place(x= 100,
                                    y=193)
        self.gui_elements[-1].focus_set()
        self.gui_elements.append(
            Label(self.root, text="Enter Resumes Location", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=30))
        self.gui_elements[-1].place(x=150, y=150 )
        def fun():
            try:
                tf = filedialog.askdirectory(
                    title="Select Folder for Resumes",
                )
                self.gui_elements[0].insert(END, tf)
            except Exception as e:
                self.message("No Folder selected.",x=200,y=200)

        self.gui_elements.append(
            Button(self.root, text="Select Folder", font=('Arial 12'), fg="#fff", bg="#00f", bd="0",
                   command=fun,
                   width=15, height=1))
        self.gui_elements[-1].place(x= 250, y=230)

        self.gui_elements.append(
            Entry(self.root, font=('Arial', 13), width=30))
        self.gui_elements[-1].place(x=650,
                                    y=193)
        self.gui_elements.append(
            Label(self.root, text="Enter Skill Set", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=20))
        self.gui_elements[-1].place(x=650, y=150)
        self.gui_elements.append(
            Button(self.root, text="Start Parser", font=('Arial 12'), fg="#fff", bg="#00f", bd="0",
                   command=fun,
                   width=13, height=1))
        self.gui_elements[-1].place(x=720, y=230)


        self.gui_elements.append(
            Button(self.root, text="Logout", font=('Arial 12'),
                   command=self.login_gui,
                   width=9, height=1))
        self.gui_elements[-1].place(x=1300, y=50)
        self.root.mainloop()

    def message(self, msg, x=0, y=0, color='#ff0000'):
        errmsg = Label(self.root, text=msg, font=('Arial', 10), fg=color,
                       bg='#012', width=30)
        errmsg.place(x=x, y=y)
        self.root.after(3000, errmsg.destroy)

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()
        self.gui_elements=[]


def main():
    root = Tk()
    root.geometry("1080x1080")
    window = MainWindow(root)

    root.mainloop()


if __name__ == '__main__':
    main()
