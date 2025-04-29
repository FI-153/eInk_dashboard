from flask import Flask
from Html.htmlTemplates import HtmlTemplates

app = Flask(__name__)

@app.route('/')
def home():
    return HtmlTemplates().home()

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('assets/icons/favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6123, debug=True)