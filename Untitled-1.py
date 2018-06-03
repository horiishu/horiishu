#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import matplotlib.pyplot as plt
import numpy as np

today = str(datetime.date.today())
testtest = "こんにちはいぬさん"

date_list = ["5/1", "5/2", "5/3", "5/4", "5/5", "5/6"]
follower_list = ["10", "35", "59", "87", "125", "191"]

plt.plot(date_list, follower_list, marker="o")
plt.title("follower value")
plt.xlabel("date")
plt.ylabel("value")
plt.grid(True)
plt.savefig("account_value.png")

test = "aiai"
test1 = "baka"

print('Content-type: text/html\n')
html = ("""
<!DOCTYPE html>
<html>
<head><title>CGIスクリプト</title></head>
<body>Today's result\n
<img src='./account_value.png'>
/n%sねこねこ%s
</body></html>
"""%(test, test1))
with open('doc.html', 'wb') as file:
    file.write(html.encode('utf-8'))