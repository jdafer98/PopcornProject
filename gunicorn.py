#USO: gunicorn --bind 0.0.0.0:$CV3_PORT restapi:app

from restapi import app

if __name__ == "__main__":
    app.run()
