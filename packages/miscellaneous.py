_ENCRYPT_TABLE = {'a':'å','b':'∫','c':'ç','d':'∂','e':'´','f':'ƒ','g':'©','h':'˙','i':'ˆ','j':'∆','k':'˚','l':'¬','m':'µ','n':'˜','o':'ø','p':'π','q':'œ','r':'®','s':'ß','t':'†','u':'¨','v':'√','w':'∑','x':'≈','y':'¥','z':'Ω',
               'A':'Å','B':'ı','C':'Ç','D':'Î','E':'´','F':'Ï','G':'©','H':'Ó','I':'ˆ','J':'Ô','K':'˚','L':'Ò','M':'Â','N':'˜','O':'Ø','P':'∏','Q':'Œ','R':'®','S':'Í','T':'†','U':'¨','V':'√','W':'∑','X':'≈','Y':'Á','Z':'Ω'}

_DECRYPT_TABLE = {encrypted: original for original, encrypted in _ENCRYPT_TABLE.items()}

def encrypt(string):
    result = ''
    for char in string:
        result += _ENCRYPT_TABLE.get(char, char)
    return result

def decrypt(string):
    result = ''
    for char in string:
        result += _DECRYPT_TABLE.get(char, char)
    return result
