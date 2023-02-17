import re
def extract_linkedin_addresses(string):
    r = re.compile('(?:http[s]?:\/\/)?(?:www\.)?linkedin\.com\/[a-z]{2}\/[a-zA-Z0-9_-]{3,100}\/?')
    return r.findall(string)

x='''+918919768667
gangadharganga90@gmail.com
linkedin.com/in/ganga-dharr
github.com/gangadharrr'''
print(extract_linkedin_addresses(x))