from semdiff.loader import load
from semdiff.service import app

if __name__ == "__main__":
    load("semdiff.differs")
    app.run(debug=True)
