from . import create_app, socketio


def main():
    app = create_app()
    socketio.run(app, host='localhost', port=42069, debug=True)


if __name__ == '__main__':
    main()
