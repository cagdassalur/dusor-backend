import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
import webapp2
from bs4 import BeautifulSoup
from ntlm import HTTPNtlmAuthHandler
import urllib2
import mechanize
import json

class MainHandler(webapp2.RequestHandler):
    def get(self):
        usr = self.request.get('usr')
        password = self.request.get('pw')
        print usr + ' - ' + password

        url = "http://www.dogus.edu.tr/dusor/"
        user = 'ata.dogus.edu.tr\\' + usr

        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, url, user, password)
        auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)

        br = mechanize.Browser()

        br.handlers = [handler for handler in br.handlers if not isinstance(handler, (mechanize._http.HTTPRobotRulesProcessor))]
        br.add_handler(auth_NTLM)
        
        try:
            br.addheaders = [('Cookie', br.open(url).info().dict['set-cookie'].split(';')[0])]
        except KeyError:
            self.response.write('Hatali Sifre veya kullanici adi.')
            return

        response = br.open(url+'FrmMain.aspx')

        response = br.open(url+'FrmNot.aspx')
        rows = [row.contents for row in BeautifulSoup(response.read()).find_all('table', id='dgnot')[-1].find_all('tr', align='left')]
        
        dersler = [[i.string.strip() for i in row] for row in rows]

        if self.request.get('json') == 'true':
            resp = json.dumps([ders[1:] for ders in dersler])
        else:
            resp = '\n<br><br>\n'.join([' - '.join(ders) for ders in dersler])

        self.response.write(resp)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)

def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    main()