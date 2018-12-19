from src.app import app
DEBUG = False
PORT = 8000

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
