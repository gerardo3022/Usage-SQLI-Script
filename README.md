# SQL injection script for the "Usage" HTB machine

[Usage Machine Banner](./images/Usage.png)

The "Usage" HTB machine has a bling sql injectino in the "/forget-password" directory. While this can be exploited with sqlmap, I wanted to create a script that show how this injection is performed.

The idea behind this injection is that we get different error messages when we input a correct e-mail address to the reset password box than when we input an incorrect email address. Because the forget password is SQL injectable, we can use this to enumerate the SQL database and extract the stored credentials.




