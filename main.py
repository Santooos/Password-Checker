import requests
import hashlib
import sys#built in module in python to do the hashing
"""
www.miraclesalad.com/webtools/md5.php
     md5 hash generator 
     hash of a string and convert into some random pattern, for creating password anamoly of the user input
     this technique is used so that other people can never guess the actual password, just take first 4 char of MD5 hash
     """


def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char

    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())
    for h,count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #check password if it exists in API response

    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)

    return get_password_leaks_count(response, tail)

git
def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times>>>> you should change your password')
        else:
            print(f'{password} was Not found. Carry on!')

        return 'done!'

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))