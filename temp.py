from bs4 import BeautifulSoup
from ntlm import HTTPNtlmAuthHandler
import urllib2
import mechanize

url = "http://www.dogus.edu.tr/dusor/"
user = r'ata.dogus.edu.tr\1331005'
password = "216216"

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, user, password)
auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

br = mechanize.Browser()

br.handlers = [handler for handler in br.handlers if not isinstance(handler, (mechanize._http.HTTPRobotRulesProcessor))]
br.add_handler(auth_NTLM)

br.addheaders = [('Cookie', br.open(url).info().dict['set-cookie'].split(';')[0])]

response = br.open(url+'FrmMain.aspx')

response = br.open(url+'FrmNot.aspx')
rows = [row.contents for row in BeautifulSoup(response.read()).find_all('table', id='dgnot')[-1].find_all('tr', align='left')]

dersler = [[i.string.strip() for i in row] for row in rows]

print '\n\n'.join(['=-=-='.join(ders) for ders in dersler])