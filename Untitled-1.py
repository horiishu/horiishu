import re

wao = '2018-05-30amg_Impressions2028'
date_ptn = r"\d{4}-\d{2}-\d{2}"
args = "amg_Impressions"
remove = date_ptn + args
waos = wao.replace(remove, "")
wao3 = wao.replace(date_ptn, "")
wao4 = re.sub(remove, '', wao)

print(waos)
print(wao3)
print(wao4)