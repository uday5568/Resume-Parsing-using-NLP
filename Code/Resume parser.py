import win32com.client as win32
from win32com.client import constants
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import docx2txt
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



def doctotext(m):
    temp = docx2txt.process(m)
    resume_text = [line.replace('\t', ' ') for line in temp.split('\n') if line]
    text = ' '.join(resume_text)
    return (text)

def pdftotext(m):
    # pdf file object
    # you can find find the pdf file with complete code in below
    # pdfFileObj = open(m, 'rb')

    # # pdf reader object
    # pdfFileReader = PdfReader(pdfFileObj)

    # # number of pages in pdf
    # num_pages = len(pdfFileReader.pages)

    # currentPageNumber = 0
    # text = ''

    # # Loop in all the pdf pages.
    # while(currentPageNumber < num_pages ):

    #     # Get the specified pdf page object.
    #     pdfPage = pdfFileReader.pages[currentPageNumber]

    #     # Get pdf page text.
    #     text = text + pdfPage.extract_text()

    #     # Process next page.
    #     currentPageNumber += 1
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
  


# load pre-trained model
nlp = en_core_web_sm.load()

# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)


def extract_name(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', None, pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text





# Grad all general stop words
STOPWORDS = set(stopwords.words('english'))

# Education Degrees
EDUCATION = [
            'BE','B.E.', 'B.E','(B.E)', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'M.B.A', 'MBA', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH','B-TECH','HIGHER SECONDARY SCHOOL','SECONDARY SCHOOL',
            'SSLC', 'SSC' 'HSC', 'CBSE', 'ICSE', 'X', 'XII','BACHELOR','ENGINEERING','12TH','10TH','INTERMEDIATE','SSC'
        ]

def extract_education(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,|)|(]', r'', tex)
            if index+1< len(nlp_text) and tex.upper() in EDUCATION and tex not in STOPWORDS:
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
BRANCH=[
    'CHEMICAL','MINING','AERONAUTICAL','TEXTILE','MECHATRONICS','CIVIL',
    'ELECTRONICS','COMMUNICATION','ROBOTICS','POWER','AEROSPACE','MECHANICAL',
    'STRUCTURAL','INDUSTRIAL','MARINE','PETROLEUM','AUTOMOBILE','PRODUCTION',
    'METALLURGICAL','CERAMIC','BIOMEDICAL','CONSTRUCTION','ELECTRONICS','TOOL'
    ,'TELECOMMUNICATION','ENVIRONMENTAL','TRANSPORTATION','ELECTRONICS AND COMMUNICATION'
    ,'BIOTECHNOLOGY','ELECTRICAL','COMPUTER','COMPUTER SCIENCE','CSE','ECE','EEE','ARC']

def extract_branch(resume_text):
    nlp_text = nlp(resume_text)

    # Sentence Tokenizer
    nlp_text = [sent.string.strip() for sent in nlp_text.sents]

    edu = {}
    # Extract education degree
    for index, text in enumerate(nlp_text):
        for tex in text.split():
            # Replace all special symbols
            tex = re.sub(r'[?|$|.|!|,|)|(]', r'', tex)
            if index+1< len(nlp_text) and tex.upper() in BRANCH and tex not in STOPWORDS:
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
noun_chunks=None
def extract_skills(resume_text):
    global noun_chunks,skill_set
    nlp_text = nlp(resume_text)
    noun_chunks=nlp_text.noun_chunks
    # removing stop words and implementing word tokenization
    tokens = [token.text for token in nlp_text if not token.is_stop]
    # reading the csv file
    data = pd.read_csv(f'{skill_set}.csv') 
    
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
    # phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), resume_text)
    phone = re.findall(re.compile(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'), resume_text)
    if phone:
        number = ''.join(phone[0])
        if len(number) > 10:
            return number
        else:
            return number



def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)[0] if r.findall(string) else ''


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
    doc.Activate ()

    # Rename path with .docx
    new_file_abs = os.path.abspath(path)
    new_file_abs = re.sub(r'\.\w+$', '.docx', new_file_abs)

    # Save and Close
    word.ActiveDocument.SaveAs(
        new_file_abs, FileFormat=constants.wdFormatXMLDocument
    )
    doc.Close(False)

def sendMails(email_sender='pinnantiuday@gmail.com',email_pass="mzfypoqkatxnqbdc",email_recevier=['pinnantiuday@gmail.com'],skill_set='python'):
    subject="You have been Shortlisted"
    body=f'''
    Hi, congratulations your resume has been shortlisted for {skill_set} role.

    This is a Testing message for Resume parsing for HR analytics project done by Uday from BE-CSE-SIST
    Kindly Ignore This Mail...
    '''
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_recevier
    em['Subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_pass)
        for mailadd in email_recevier:
            if(re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',mailadd)):
                smtp.sendmail(email_sender,mailadd,em.as_string())
            else:
                print('Error sending mail to :',mailadd)
    print("Mails Successfully Sent")
                

def data_display():
    out_data={'Name':extract_name(textinput),
    'Qualification':extract_education(textinput),
    'Specialization':extract_branch(textinput),
    'Skills':extract_skills(textinput),
    'Mobile Number':extract_mobile_number(textinput),
    'Email':extract_email_addresses(textinput),
    'LinkedIn':extract_linkedin_addresses(textinput),
    'Github':extract_github_addresses(textinput)
    }
    json_object = json.dumps(out_data, indent=4)
    
    with open(f"output/{re.sub('[^A-Za-z]','',out_data['Name'])}_{skill_set}_result.json", "w") as outfile:
        outfile.write(json_object)
        outfile.close()
    print(json_object)
    df=pd.read_csv(f"{skill_set}.csv")
    _score=0
    _df ={i:j for i,j in zip(df['skill'],df['Score'])}
    for skill in out_data['Skills']:
        _score+=_df[skill.lower()]
    return _score,out_data['Email']
if __name__ == '__main__': 
    scores={}
    skill_set=input("Enter Domain : ")
    for file in os.listdir(r'../Resume-Parsing-using-NLP/Resumes'):
        try:
            # FilePath = input().replace("\'",'').replace('\"','')
            # FilePath=r"C:\Users\pinna\Downloads\SIST-BE-CSE-39110202-ChakaliGangadhar.pdf"
            FilePath='../Resume-Parsing-using-NLP/Resumes/'+file
            if FilePath.endswith('.docx'):
                textinput = doctotext(FilePath)
                score,mail=data_display()
                scores[file]=[score,mail]
            elif FilePath.endswith('.doc'):
                save_as_docx(FilePath)
                textinput = doctotext(FilePath+'x')
                score,mail=data_display()
                scores[file]=[score,mail]
            elif FilePath.endswith('.pdf'):
                textinput = pdftotext(FilePath)
                score,mail=data_display()
                scores[file]=[score,mail]
            else:
                print("File not support")
        except Exception as e:
            print(e)
    
    df = pd.DataFrame(columns=["File",'Email','scores'])
 
    for fname in sorted(scores,key=lambda x:scores[x][0],reverse=True):
        df.loc[len(df.index)] = [fname,scores[fname][1],int(scores[fname][0])]
    df.to_csv('Ranks.csv',index=False)
    rank_lim=int(input(f'Rank Limit (max : {max(scores.values(),key=lambda x:x[0])[0]}): '))
    mails=[]
    scs=[]
    for fname in sorted(scores,key=lambda x:scores[x][0],reverse=True):
        if(int(scores[fname][0])>=rank_lim):
            mails.append(scores[fname][1])
            scs.append(scores[fname][0])
    print("\n".join(mails))
    xpoints = np.array(mails)
    ypoints = np.array(scs)

    

    plt.bar(xpoints, ypoints)
    plt.xticks(rotation = 45)
    plt.show()
    #sendMails(email_recevier=mails,skill_set=skill_set)
