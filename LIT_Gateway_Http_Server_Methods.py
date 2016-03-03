from sysconfigx import *
from bottle import get, post, request, Bottle, run, error, static_file, response, template

class LIT_http_server_Functions():

	global app
	global _config
	app = Bottle()

        def __init__(self):
		pass

	@app.post('/login')
	def do_login():
    		username = request.forms.get('username')
    		passwd = request.forms.get('password')
	        _config = Parser_Functions()
                _config.parser_init()
                _config.ConfigSectionMap()
                _section = 'WEB_AUTH'
                _username = _config.getSectionOption(_section, 'username')
                _passwd = _config.getSectionOption(_section, 'passwd')
		if (username == _username) and (passwd == _passwd):
			return static_file("index_loginok.html", root='html/')
    		else:
			return "<p>Login failed, invalid credentials</p>"

	@app.error(404)
	def error404(error):
    		return 'IoT Gateway Http Server ERROR 404 - Invalid URL<br><br>Support Email: devops@linuxiot.org'

	@app.route('/download/<filename:path>')
	def download(filename):
    		return static_file(filename, root='files/', download=filename)

	@app.route('/images/<filename:path>')
	def download(filename):
    		return static_file(filename, root='images/', download=filename)

	@app.route('/css/<filename:path>')
	def download(filename):
    		return static_file(filename, root='css/', download=filename)

	#@app.route('/html/<filename:path>')
	#def download(filename):
		#return static_file(filename, root='html/', download=filename)

	@app.route('/')
	def main_page():
		response.set_header('Content-Language', 'en')
    		return static_file("index.html", root='html/')

	def start_server(self):
			run(app, host='0.0.0.0', port=82, server='paste')
