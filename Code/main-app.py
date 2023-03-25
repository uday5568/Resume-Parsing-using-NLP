import mysql.connector
from tkinter import *
import hashlib
import re


# ws = Tk()
# ws.geometry("1080x1080")
# ws.state('zoomed')
# ws.title("Resume Parser")
#
#
# ws['bg'] = '#012'
#
# username_l = StringVar()
# password_l = StringVar()
# username_s = StringVar()
# password_s = StringVar()
#
#
# # img = PhotoImage(file="a40012e.png")
# # label = Label(
# #     ws,
# #     image=img
# # )
# # label.place(x=0, y=0)
#
#
#
# def registration():
#     reg = Toplevel()
#
#     reg.title("Resume Parser")
#     reg.state('zoomed')
#     reg.geometry("1080x1080")
#     reg['bg'] = '#012'
#     def fun():
#         mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
#         db = mydb.cursor()
#         try:
#             sql = "SELECT username FROM users"
#             db.execute(sql)
#             if str(hashlib.md5(username_s.get().encode()).hexdigest()) in [i[0] for i in db]:
#                 errmsg=Label(reg, text="*Username Taken", font=('Arial', 12), fg='#ff0000', bg='#012', width=20)
#                 errmsg.place(x=700, y=350)
#                 reg.after(3000, errmsg.destroy)
#             else:
#                 sql = "INSERT INTO users VALUES(MD5(%s),MD5(%s))"
#                 val = (username_s.get(), password_s.get())
#                 if re.search('[A-Z]', val[1]) and re.search('[a-z]', val[1]) and re.search('[0-9]', val[1]) and re.search(
#                         '[@_!#$%^&*()<>?/\|}{~:]', val[1]) and len(val[1]) >= 8:
#                     db.execute(sql, val)
#                     errmsg=Label(reg, text="*Registration Successful", font=('Arial', 12), fg='#00ff00', bg='#012', width=30)
#                     errmsg.place(x=700, y=350)
#                     reg.after(3000, errmsg.destroy)
#
#                 else:
#                     errmsg=Label(reg, text="*Weak Password Try Again", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
#                     errmsg.place(x=700, y=350)
#                     reg.after(3000, errmsg.destroy)
#
#         except Exception as e:
#             errmsg=Label(reg, text="*Registration Failed, Error Occured", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
#             errmsg.place(x=700, y=430)
#             reg.after(3000, errmsg.destroy)
#
#         mydb.commit()
#         mydb.close()
#
#     signup_x = 500
#     signup_y = 350
#     Label(reg, text='Resume Parser Using NLP', font=('Arial', 30)).place(x=signup_x, y=signup_y - 170)
#     Label(reg, text='SignUp', width=15, font=('Arial', 18)).place(x=signup_x + 150, y=signup_y - 70)
#
#     Label(reg, text="Username", font=('Arial', 16), width=10).place(x=signup_x, y=signup_y)
#     Entry(reg, width=25, font=('Arial 16'), textvariable=username_s).place(x=signup_x + 150, y=signup_y)
#     Label(reg, text="Password", font=('Arial', 16), width=10).place(x=signup_x, y=signup_y + 50)
#     Entry(reg, width=25, font=('Arial 16'), textvariable=password_s).place(x=signup_x + 150, y=signup_y + 50)
#     Button(reg, text="SignUp", font=('Arial 12'), command=fun, width=10, height=1).place(x=signup_x + 200,
#                                                                                                  y=signup_y + 130)
#     reg.mainloop()


# def validate():
#     mydb = mysql.connector.connect(host="localhost", user="root", database='carwash')
#     db = mydb.cursor()
#     try:
#         sql = "SELECT * FROM users"
#         db.execute(sql)
#         list_db = {}
#         for i in db:
#             list_db[i[0]] = i[1]
#         if list_db.get(hashlib.md5(username_l.get().encode()).hexdigest(), '') == hashlib.md5(
#                 password_l.get().encode()).hexdigest():
#             if hashlib.md5(username_l.get().encode()).hexdigest() == "9a7174d1cf08b61c7bf9cafe287f4dce" and hashlib.md5(
#                     password_l.get().encode()).hexdigest() == "b7a84f4452aa9d48aa8c0f43073bbd8d":
#                 admin_home()
#             else:
#                 user_home()
#         else:
#             errmsg=Label(reg, text="*Incorrect Username or Password", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
#             errmsg.place(x=200, y=350)
#             reg.after(3000, errmsg.destroy)
#     except Exception as e:
#         errmsg=Label(reg, text="*Error Encountered", font=('Arial', 12), fg='#ff0000', bg='#012', width=30)
#         errmsg.place(x=350, y=450)
#         reg.after(3000, errmsg.destroy)
#     mydb.commit()
#     mydb.close()
#
#
# login_x = 500
# login_y = 350
# Label(ws, text='Resume Parser Using NLP', font=('Arial', 30)).place(x=login_x,y=login_y-170)
# # LOGIN
# Label(ws, text='Login', width=15, font=('Arial', 18)).place(x=login_x + 150, y=login_y-70)
#
# Label(ws, text="Username", font=('Arial', 16), width=10).place(x=login_x, y=login_y)
# Entry(ws, width=25, font=('Arial 16'), textvariable=username_l).place(x=login_x + 150, y=login_y)
# Label(ws, text="Password", font=('Arial', 16), width=10).place(x=login_x, y=login_y + 50)
# Entry(ws, width=25, font=('Arial 16'), textvariable=password_l).place(x=login_x + 150, y=login_y + 50)
# Label(ws, text="New User?", font=('Arial', 13),fg="#fff",bg="#012", width=10).place(x=login_x+150, y=login_y + 90)
#
# Button(ws, text="Create Account", font=('Arial 12'),fg="#00f",bg="#012",bd="0", command=registration, width=12, height=1).place(x=login_x+245, y=login_y + 87)
#
# Button(ws, text="Login", font=('Arial 12'), command=validate, width=10, height=1).place(x=login_x + 200,y=login_y + 130)
#
#
# ws.mainloop()


class MainWindow():

    def __init__(self, mainWidget):
        self.root = mainWidget
        self.root.state('zoomed')
        self.gui_elements = []
        self.root['bg'] = '#012'
        mydb = mysql.connector.connect(host="localhost", user="root")
        db = mydb.cursor()
        try:
            sql = "CREATE DATABASE IF NOT EXISTS resumesparser"
            db.execute(sql)

        except Exception as e:
            errmsg = Label(self.root, text="*Database Creation Failed", font=('Arial', 12), fg='#ff0000',
                           bg='#012', width=30)
            errmsg.place(x=700, y=430)
        finally:
            self.login_gui()

        mydb.commit()
        mydb.close()

    def login_gui(self):
        self.root.title('Login Page')
        self.gui_elements_remove(self.gui_elements)
        username_l = StringVar()
        password_l = StringVar()
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
                                    y=login_y + 90)

        self.gui_elements.append(
            Button(self.root, text="Create Account", font=('Arial 12'), fg="#00f", bg="#012", bd="0",
                   command=self.signup_gui,
                   width=12, height=1))
        self.gui_elements[-1].place(x=login_x + 245, y=login_y + 87)

        self.gui_elements.append(
            Button(self.root, text="Login", font=('Arial 12'), command=self.login_gui, width=10, height=1))
        self.gui_elements[-1].place(x=login_x + 200, y=login_y + 130)

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
                  `username` varchar(11) NOT NULL ,   
                  `email` varchar(250) NOT NULL ,       
                  `password` varchar(30)  NOT NULL ,     
                   PRIMARY KEY  (`username`)
                );'''
                db.execute(sql)


            except Exception as e:
                self.message("*Table Creation Failed, Error Occured", x=signup_x + 200, y=signup_y + 80)

            try:
                if (
                        username_s.get() and email_s.get() and password_s.get() and password_s.get() == re_password_s.get()):
                    sql = "SELECT username FROM users"
                    db.execute(sql)
                    if str(hashlib.md5(username_s.get().encode()).hexdigest()) in [i[0] for i in db]:
                        raise Exception('*Username Taken')
                    else:
                        sql = "INSERT INTO users VALUES(MD5(%s),%s,MD5(%s))"
                        val = (username_s.get(), email_s.get(), password_s.get())
                        if re.search('[A-Z]', val[1]) and re.search('[a-z]', val[1]) and re.search('[0-9]',
                                                                                                   val[
                                                                                                       1]) and re.search(
                            '[@_!#$%^&*()<>?/\|}{~:]', val[1]) and len(val[1]) >= 8:
                            db.execute(sql, val)
                            self.message("*Registration Successful", x=signup_x + 200, y=signup_y, color='#00ff00')


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
                print(e)
                self.message("*Resgitration Failed,Error Occured", x=signup_x + 150, y=signup_y + 180)

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

        self.gui_elements.append(Button(self.root, text="SignUp", font=('Arial 12'), command=fun, width=10, height=1))
        self.gui_elements[-1].place(x=signup_x + 200, y=signup_y + 230)
        self.root.mainloop()

    def message(self, msg, x=0, y=0, color='#ff0000'):
        errmsg = Label(self.root, text=msg, font=('Arial', 10), fg=color,
                       bg='#012', width=30)
        errmsg.place(x=x, y=y)
        self.root.after(3000, errmsg.destroy)

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()


def main():
    root = Tk()
    root.geometry("1080x1080")
    window = MainWindow(root)

    root.mainloop()


if __name__ == '__main__':
    main()
