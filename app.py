from website import create_app
from flask import __main__

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
