import string

def clean(text):
    lower_txt = text.lower().strip()
    txt_only = lower_txt.translate(str.maketrans('', '', string.punctuation))

    return txt_only

test = "     Testing lang   t  @@@@ @"

print(test)
print(clean(test))