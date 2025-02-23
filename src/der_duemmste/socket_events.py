from flask_socketio import SocketIO, emit


def register_socket_events(socketio: SocketIO):
    @socketio.on("update_game")
    def handle_update_game(data):
        emit("game_state", data, broadcast=True)
