import pandas as pd
# import spacy
# nlp = spacy.load('en_core_web_sm')
# noun_chunks = nlp.noun_chunks

# def extract_skills(resume_text):
#     nlp_text = nlp(resume_text)

#     # removing stop words and implementing word tokenization
#     tokens = [token.text for token in nlp_text if not token.is_stop]
#     colnames = ['skill']
#     # reading the csv file
#     data = pd.read_csv('skill.csv', names=colnames) 
    
#     # extract values
#     skills = data.skill.tolist()
#     skillset = []
    
#     # check for one-grams (example: python)
#     for token in tokens:
#         if token.lower() in skills:
#             skillset.append(token)
   
#     for token in noun_chunks:
#         token = token.text.lower().strip()
#         if token in skills:
#             skillset.append(token)
#     return [i.capitalize() for i in set([i.lower() for i in skillset])]
  
# print ('Skills:',extract_skills(textinput))


# df=pd.DataFrame(["assembly", "bash", " c " "c++", "c#", "coffeescript", "emacs lisp",
#          "go!", "groovy", "haskell", "java", "javascript", "matlab", "max MSP", "objective c", 
#          "perl", "php","html", "xml", "css", "processing", "python", "ruby", "sml", "swift", 
#          "latex" "unity", "unix","visual basic", "wolfram language", "xquery", "sql", "node.js",
#          "scala", "kdb", "jquery", "mongodb","r","machine learning","data analysis","data science","artificial intelligence","deep learning"],columns=['skill'])
# df.to_csv('skill.csv',index=False)


df=pd.DataFrame({"skill":[ "java", "javascript","node.js","css","jquery", "sql","xml","json","web","framework"],
                 "Score":[4,3,2,1,2,4,3,4,2,1]})
df.to_csv('java.csv',index=False)
# df=pd.DataFrame({"skill":["deep learning","python","data science","machine learning","artificial intelligence", "flask","html","css"],
#                 "Score":[3,4,5,4,4,2,2,2]})
# df.to_csv('python.csv',index=False)