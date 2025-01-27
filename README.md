# Bitspenser
A service which allows sharing files without setting up accounts.
<br>
Usage:
<br>
```$ git clone https://github.com/maholmlund/bitspenser.git ```
<br>
```$ python3 -m pip install Django```
<br>
```$ python3 manage.py runserver```

### How to use:

Uploading a file requires you to give two passwords. The first password is the one you can share. 
It can only be used to download the file. The other password can be used to delete the file from the server. 
The service gives you a link from which you can access the file. 
If you input the pubic password you can only download the file. If you use the other password, 
you will also be able to delete the file.

![](https://github.com/maholmlund/bitspenser/blob/main/upload.gif)
![](https://github.com/maholmlund/bitspenser/blob/main/deletion.gif)

Not production ready. Please do not use.
