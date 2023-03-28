import os
from tkinter.ttk import Treeview

import mysql.connector
from tkinter import *
import hashlib
from tkinter import filedialog,messagebox
from tkinter.messagebox import askyesno, askquestion

import win32com.client as win32
from win32com.client import constants
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import docx2txt
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger, PdfReader
import io
import os
from email.message import EmailMessage
import ssl
import smtplib
import pandas as pd
import spacy
import json

nlp = spacy.load('en_core_web_sm')

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords

stop = stopwords.words('english')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
import spacy
import en_core_web_sm
from nltk.tag.stanford import StanfordNERTagger
from spacy.matcher import Matcher
from nameparser.parser import HumanName
from nltk.corpus import wordnet
import matplotlib.pyplot as plt
import numpy as np

# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
STOPWORDS = set(stopwords.words('english'))
# Education Degrees
EDUCATION = [
    'BE', 'B.E.', 'B.E', '(B.E)', 'BS', 'B.S',
    'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S',
    'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 'B-TECH', 'HIGHER SECONDARY SCHOOL', 'SECONDARY SCHOOL',
    'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII', 'BACHELOR', 'ENGINEERING', '12TH', '10TH', 'INTERMEDIATE', 'SSC'
]

BRANCH = [
    'CHEMICAL', 'MINING', 'AERONAUTICAL', 'TEXTILE', 'MECHATRONICS', 'CIVIL',
    'ELECTRONICS', 'COMMUNICATION', 'ROBOTICS', 'POWER', 'AEROSPACE', 'MECHANICAL',
    'STRUCTURAL', 'INDUSTRIAL', 'MARINE', 'PETROLEUM', 'AUTOMOBILE', 'PRODUCTION',
    'METALLURGICAL', 'CERAMIC', 'BIOMEDICAL', 'CONSTRUCTION', 'ELECTRONICS', 'TOOL'
    , 'TELECOMMUNICATION', 'ENVIRONMENTAL', 'TRANSPORTATION', 'ELECTRONICS AND COMMUNICATION'
    , 'BIOTECHNOLOGY', 'ELECTRICAL', 'COMPUTER', 'COMPUTER SCIENCE', 'CSE', 'ECE', 'EEE', 'ARC']

def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)

def pdftotext(m):
    def extract_text_from_pdf(pdf_path):
        with open(pdf_path, 'rb') as fh:
            # iterate over all pages of PDF document
            for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
                # creating a resoure manager
                resource_manager = PDFResourceManager()

                # create a file handle
                fake_file_handle = io.StringIO()

                # creating a text converter object
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,
                    # codec='utf-8',
                    laparams=LAParams()
                )

                # creating a page interpreter
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )

                # process current page
                page_interpreter.process_page(page)

                # extract text
                text = fake_file_handle.getvalue()
                yield text

                # close open handles
                converter.close()
                fake_file_handle.close()

    # text = ''
    # for page in extract_text_from_pdf(r"C:\Users\pinna\Downloads\Profile.pdf"):
    #     text += ' ' + page
    text = ''
    for page in extract_text_from_pdf(m):
        text += ' ' + page
    return (text)

def extract_name(resume_text):
    nlp_text = nlp(resume_text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add(key='NAME', patterns=[pattern])

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,|)|(]', r'', tex)
            if index + 1 < len(nlp_text) and tex.upper() in EDUCATION and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

def extract_branch(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.text.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,|)|(]', r'', tex)
            if index + 1 < len(nlp_text) and tex.upper() in BRANCH and tex not in STOPWORDS:
                edu[tex] = text + nlp_text[index + 1]

    # Extract year
    education = []
    for key in edu.keys():
        year = re.search(re.compile(r'(((20|19)(\d{})))'), edu[key])
        if year:
            education.append((key, ''.join(year[0])))
        else:
            education.append(key)
    return education

# noun_chunks = nlp.noun_chunks
noun_chunks = None

def extract_skills(resume_text):
    global noun_chunks, skill_set
    nlp_text = nlp(resume_text)
    noun_chunks = nlp_text.noun_chunks
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # reading the csv file
    data = pd.read_csv(skill_set)

    # extract values
    skills = data['skill'].tolist()
    skillset = []

    # check for one-grams (example: python)
    for token in tokens:
        if token.lower() in skills:
            skillset.append(token)

    for token in noun_chunks:
        token = token.text.lower().strip()
        if token in skills:
            skillset.append(token)
    return [i.capitalize() for i in set([i.lower() for i in skillset])]


def extract_mobile_number(resume_text):
    phone = re.findall(re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'), resume_text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return number
        else:
            return number


def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)[0].replace(".com", ".co").replace(".co", ".com") if r.findall(string) else ''


def extract_linkedin_addresses(string):
    r = re.compile(r'(?:http[s]?:\/\/)?(?:www\.)?linkedin\.com\/[a-z]{2}\/[a-zA-Z0-9_-]{3,100}\/?')
    return r.findall(string)[0] if r.findall(string) else ''


def extract_github_addresses(string):
    r = re.compile('(?:http[s]?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]{3,100}\/?')
    return r.findall(string)[0] if r.findall(string) else ''


def save_as_docx(path):
    # Opening MS Word
    word = win32.Dispatch("SAPI.SpVoice")
    doc = word.Documents.Open(path)
    doc.Activate()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)


def sendMails(email_sender='pinnintiuday.3344@gmail.com', email_pass="fppdnxddjocusnfb",
              email_recevier=['pinnantiuday@gmail.com'], skill_set="python"):
    subject = "[Testing]You have been Shortlisted"
    body = f'''
    Hi, congratulations your resume has been shortlisted for {skill_set} role.

    This is a Testing message for Resume parsing for HR analytics project done by Uday from BE-CSE-SIST
    Kindly Ignore This Mail...
    '''
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_recevier
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_pass)
        for mailadd in email_recevier:
            if (re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', mailadd)):
                smtp.sendmail(email_sender, mailadd, em.as_string())
            else:
                print('Error sending mail to :', mailadd)
    print("Mails Successfully Sent")


def data_display(textinput):
    out_data = {'Name': extract_name(textinput),
                'Qualification': extract_education(textinput),
                'Specialization': extract_branch(textinput),
                'Skills': extract_skills(textinput),
                'Mobile Number': extract_mobile_number(textinput),
                'Email': extract_email_addresses(textinput),
                'LinkedIn': extract_linkedin_addresses(textinput),
                'Github': extract_github_addresses(textinput)
                }
    json_object = json.dumps(out_data, indent=4)

    with open(
            f"../output/{re.sub('[^A-Za-z]', '', out_data['Name'])}_{skill_set.split('/')[-1].replace('.csv','')}_result.json",
            "w") as outfile:
        outfile.write(json_object)
        outfile.close()
    print(json_object)
    df = pd.read_csv(skill_set)
    _score = 0
    _df = {i: j for i, j in zip(df['skill'], df['Score'])}
    for skill in out_data['Skills']:
        _score += _df[skill.lower()]
    return _score, out_data['Email']




class MainWindow:

    def __init__(self, mainWidget):
        self.root = mainWidget
        self.root.state('zoomed')
        self.gui_elements = []
        self.root['bg'] = '#012'
        self.ResumesFolder=None

        try:
            mydb = mysql.connector.connect(host="localhost", user="root")
            db = mydb.cursor()
            sql = "CREATE DATABASE IF NOT EXISTS resumesparser"
            db.execute(sql)
            mydb.commit()
            mydb.close()
        except Exception as e:
            self.message("*Database Creation Failed", x=620, y=550)
        finally:
            self.login_gui()

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
                print(list_db, hashlib.md5(username_l.get().encode()).hexdigest())
                if list_db.get(hashlib.md5(username_l.get().encode()).hexdigest(), '') == hashlib.md5(
                        password_l.get().encode()).hexdigest():
                    self.resumeprocesssing()
                else:
                    self.message("*Incorrect Username or Password", x=650, y=430)
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
        self.gui_elements.append(Entry(self.root, width=25, show="*",font=('Arial 16'), textvariable=password_l))
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
                if (
                        username_s.get() and email_s.get() and password_s.get() and password_s.get() == re_password_s.get()):
                    sql = "SELECT username FROM users"
                    db.execute(sql)
                    if str(hashlib.md5(username_s.get().encode()).hexdigest()) in [i[0] for i in db]:
                        self.message('*Username Taken', x=signup_x + 150, y=signup_y + 28)
                    else:
                        sql = "INSERT INTO users VALUES(MD5(%s),%s,MD5(%s))"
                        val = (username_s.get(), email_s.get(), password_s.get())
                        if re.search('[A-Z]', val[2]) and re.search('[a-z]', val[2]) and re.search('[0-9]', val[
                            2]) and re.search(
                                '[@_!#$%^&*()<>?/|}{~:]', val[2]) and len(val[2]) >= 8:
                            db.execute(sql, val)
                            self.message("*Registration Successful", x=signup_x + 150, y=signup_y + 177,
                                         color='#00ff00')


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
        self.gui_elements.append(Entry(self.root, width=25,show="*", font=('Arial 16'), textvariable=password_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y + 100)

        self.gui_elements.append(
            Label(self.root, text="Re-type Password", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=14))
        self.gui_elements[-1].place(x=signup_x - 70, y=signup_y + 150)
        self.gui_elements.append(Entry(self.root, width=25, show="*",font=('Arial 16'), textvariable=re_password_s))
        self.gui_elements[-1].place(x=signup_x + 150, y=signup_y + 150)

        self.gui_elements.append(
            Label(self.root, text="Account Already Exist?", font=('Arial', 13), fg="#fff", bg="#012", width=20))
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
        global skill_set
        skill_set_tk=StringVar()
        resumes_folders=StringVar()
        rank=IntVar()
        self.root.title('Resume Parser')
        self.gui_elements_remove(self.gui_elements)
        self.gui_elements.append(
            Entry(self.root, font=('Arial', 13), width=70))
        self.gui_elements[-1].place(x=100,
                                    y=193)
        self.gui_elements[-1].focus_set()
        self.gui_elements.append(
            Label(self.root, text="Enter Resumes Location", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=30))
        self.gui_elements[-1].place(x=220, y=150)

        def fun():

            try:
                self.ResumesFolder = filedialog.askdirectory(
                    title="Select Folder for Resumes",
                )
                self.gui_elements[0].insert(END,  self.ResumesFolder)
                for file in os.listdir(self.ResumesFolder):
                    self.gui_elements[-1].insert(END, file+"\n\n")
            except Exception as e:
                self.message("No Folder selected.", x=300, y=270)

        def fun1():
            global skill_set
            try:
                skill_set = filedialog.askopenfile(
                    title="Select Folder for Resumes",
                    filetypes=[('Comma Seperated Files', "*.csv")]
                ).name
                self.gui_elements[3].insert(END, skill_set)
            except Exception as e:
                self.message("No File selected.", x=820, y=270)
        def fun4(mails,skill_set):
            answer = askyesno(title='Confirmation',
                              message='Are you sure that you want to Send Mails?')
            if(answer):
                try:
                    sendMails(email_recevier=mails,skill_set=skill_set)
                    messagebox.showinfo("Resume Parsing Using NLP", "Mails have been Sent Successfully")
                except Exception as e:
                    messagebox.showinfo("Resume Parsing Using NLP", "!!!Mails Sending Failed!!!")

        def fun3(rm,scores):
            rank_lim =rm
            mails = []
            scs = []
            self.gui_elements[-6].place(x=750, y=350)
            self.gui_elements[-5].place(x=730, y=350)
            for fname in sorted(scores, key=lambda x: scores[x][0], reverse=True):
                if (int(scores[fname][0]) >= rank_lim):
                    mails.append(scores[fname][1])
                    scs.append(scores[fname][0])
                    self.gui_elements[-6].insert('', 'end', text="1", values=(fname, scores[fname][0], scores[fname][1]))

            print("\n".join(mails))
            self.gui_elements.append(
                Button(self.root, text="Send\nMails", font=("Arial",12,"bold"), fg="#fff", bg="#a00",
                       command=lambda: fun4(mails, skill_set.split('/')[-1].replace('.csv', '')),
                       width=10, height=2))
            self.gui_elements[-1].place(x=1400, y=700)

            xpoints = np.array([i.replace("@gmail.com", '') for i in mails])
            ypoints = np.array(scs)

            plt.barh(xpoints, ypoints, )
            plt.show()


        def parser():
            global skill_set
            scores = {}
            skill_set = skill_set_tk.get() if skill_set_tk.get() else skill_set
            self.ResumesFolder = resumes_folders.get() if resumes_folders.get() else self.ResumesFolder
            for file in os.listdir(self.ResumesFolder+'/'):
                try:
                    FilePath = self.ResumesFolder+'/'+ file
                    if FilePath.endswith('.docx'):
                        textinput = doctotext(FilePath)
                        score, mail = data_display(textinput)
                        scores[file] = [score, mail]
                    elif FilePath.endswith('.doc'):
                        save_as_docx(FilePath)
                        textinput = doctotext(FilePath + 'x')
                        score, mail = data_display(textinput)
                        scores[file] = [score, mail]
                    elif FilePath.endswith('.pdf'):
                        textinput = pdftotext(FilePath)
                        score, mail = data_display(textinput)
                        scores[file] = [score, mail]
                    else:
                        print("File not support")
                except Exception as e:
                    print(e)

            df = pd.DataFrame(columns=["File", 'Email', 'scores'])

            for fname in sorted(scores, key=lambda x: scores[x][0], reverse=True):
                df.loc[len(df.index)] = [fname, scores[fname][1], int(scores[fname][0])]
            df.to_csv('Ranks.csv', index=False)
            messagebox.showinfo("Resume Parsing Using NLP","Resume Parsing Completed")
            self.gui_elements.append(
                Label(self.root, text=f'Score Limit (max : {max(scores.values(),key=lambda x:x[0])[0]}): ', font=('Arial',12,'bold'), fg="#fff", bg="#012", bd="0",
                       width=18, height=1))
            self.gui_elements[-1].place(x=710, y=320)
            self.gui_elements.append(
                Button(self.root, text="Shortlist", font=('Arial 12'), fg="#fff", bg="#00f",
                       command=lambda : fun3(rank.get(),scores),
                       width=15, height=1))
            self.gui_elements[-1].place(x=1170, y=310)

            self.gui_elements.append(
                Entry(self.root, font=('Arial', 12),bg='#aaa', width=30, textvariable=rank))
            self.gui_elements[-1].place(x=890,
                                        y=320)



        self.gui_elements.append(
            Button(self.root, text="Select Folder", font=('Arial 12'), fg="#fff", bg="#00f", bd="0",
                   command=fun,
                   width=15, height=1))
        self.gui_elements[-1].place(x=350, y=230)

        self.gui_elements.append(
            Entry(self.root, font=('Arial', 13), width=30,textvariable=skill_set_tk))
        self.gui_elements[-1].place(x=800,
                                    y=193)
        self.gui_elements.append(
            Label(self.root, text="Enter Skill Set", fg="#fff", bg="#012", font=('Arial', 16, "bold"), width=20))
        self.gui_elements[-1].place(x=800, y=150)
        self.gui_elements.append(
            Button(self.root, text="Select Skill set(.csv)", font=('Arial 12'), fg="#fff", bg="#00f", bd="0",
                   command=fun1,
                   width=15, height=1))
        self.gui_elements[-1].place(x=870, y=230)
        self.gui_elements.append(
            Button(self.root, text="Start \nParser", font=("Arial",15,"bold"), fg="#fff", bg="#0a0",
                   command=parser,
                   width=13, height=2))
        self.gui_elements[-1].place(x=1100, y=193)

        self.gui_elements.append(
            Button(self.root, text="Logout", font=('Arial 12'),
                   command=self.login_gui,
                   width=9, height=1))
        self.gui_elements[-1].place(x=1300, y=50)
        self.gui_elements.append(
            Label(self.root, text="Resume Files",fg="#012",bg="#aaa",font=('Arial', 18, "bold"),
                   width=10, height=1))
        self.gui_elements[-1].place(x=100, y=320)

        self.gui_elements.append(Treeview(self.root, column=("c1", "c2","c3"), show='headings', height=20, selectmode="browse"))
        self.gui_elements[-1].column("#1", anchor=CENTER, stretch=NO)
        self.gui_elements[-1].heading("#1", text="FILENAME")
        self.gui_elements[-1].column("#2", anchor=CENTER, stretch=NO)
        self.gui_elements[-1].heading("#2", text="SCORE")
        self.gui_elements[-1].column("#3", anchor=CENTER, stretch=NO)
        self.gui_elements[-1].heading("#3", text="EMAIL")

        self.gui_elements.append(Scrollbar(self.root))
        self.gui_elements[-1].configure(command=self.gui_elements[-2].yview)
        self.gui_elements[-2].configure(yscrollcommand=self.gui_elements[-1].set)
        self.gui_elements[-1].pack(side=RIGHT, fill=BOTH)

        self.gui_elements.append(
            Text(self.root, font=('Arial 12'),
                   width=60, height=23))
        self.gui_elements[-1].place(x=100, y=350)
        self.root.mainloop()

    def message(self, msg, x=0, y=0, color='#ff0000'):
        errmsg = Label(self.root, text=msg, font=('Arial', 10), fg=color,
                       bg='#012', width=30)
        errmsg.place(x=x, y=y)
        self.root.after(3000, errmsg.destroy)

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()
        self.gui_elements = []


def main():
    root = Tk()
    root.geometry("1080x1080")
    window = MainWindow(root)

    root.mainloop()

if __name__ == '__main__':
    main()
