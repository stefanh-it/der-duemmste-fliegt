"""Not used in this project, but necessary for deployment."""
from . import create_app, socketio

app = create_app()

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8000, debug=False)
