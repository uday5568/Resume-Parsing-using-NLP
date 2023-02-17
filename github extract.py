import re
def extract_github_addresses(string):
    # r = re.compile(r'[\w\.-]+@[\w\.-]+')
    r = re.compile('(?:http[s]?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]{3,100}\/?')
    return r.findall(string)
print("Github :",extract_github_addresses(input()))