import urllib2
import subprocess

req = urllib2.Request('http://nicolettes1992.pythonanywhere.com/home/')
response = urllib2.urlopen(req)
html = response.read()


c = open("htmlcode.txt", "w")
c.write(html)
c.close()

subprocess.call("python bubble2-all.py", shell=True)
subprocess.call("python bubble2-hashtag.py", shell=True)
subprocess.call("python bubble2-star2.py", shell=True)