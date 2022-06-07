from webserver import create_app

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
    
