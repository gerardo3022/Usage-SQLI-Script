# SQL injection script for the "Usage" HTB machine

The "Usage" HTB machine has a blind SQL injection in the "/forget-password" directory. While this vulnerability can be exploited with tools like sqlmap, I wanted to create a script to demonstrate a manual SQL injection attack.

The idea behind this attack is that the application generates different error messages when a correct e-mail address is entered versus an incorrect one. Since the "forget-password" page is susceptible to SQL injection, we can leverage this to extract information from the underlying SQL database, including stored credentials.
