import os
from der_duemmste import create_app, socketio


def main():
    # Create the Flask app using factory
    app = create_app()

    # Optionally pull host/port/debug settings from environment variables
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 42069))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() in ("true", "1")

    # Run the app using SocketIO. Eventlet should already be monkey-patched in your __init__.py.
    socketio.run(app, host=host, port=port, debug=debug, use_reloader=True)


if __name__ == '__main__':
    main()
