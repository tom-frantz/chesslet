import io from "socket.io-client";


class API {
    constructor(connection, gameStartCallback, movePieceCallback) {
        this.token = null;
        this.current_game = null;

        this.serverIO = io(connection);

        this.serverIO.on("connect", () => {console.log("Connected!")});
        this.serverIO.on("game start", gameStartCallback);
        this.serverIO.on("move piece", movePieceCallback)

    }

    __check_token() {
        if (this.token === null) {
            console.warn("THERE WAS NO TOKEN SET. PLEASE LOG IN FIRST");
            return false;
        } else {
            return true;
        }
    }

    login (username, password, callback) {
        this.serverIO.emit("login", {username, password}, (res) => {
            if (res.success) {
                this.token = res.token;
            }
            callback(res)
        });
    }

    create_game (callback) {
        // For all these, need to pass token to the server to check if logged in.
        this.__check_token();

        this.serverIO.emit("create_game", {token: this.token}, (res) => {
            if (res.success) {
                this.current_game = res.game_uuid
            }
            callback(res)
        })
    }

    join_game(game_uuid, callback) {
        this.__check_token();

        this.serverIO.emit(
            "join_game",
            {
                token: this.token,
                game_uuid
            },
            (res) => {
                if (res.success) {
                    this.current_game = game_uuid
                }
                callback(res);
            }
        )
    }

    leave_game(callback) {
        this.serverIO.emit("leave_game", {game_uuid: this.current_game}, callback);
        this.serverIO.current_game = null;
    }

    move_piece(from_piece, to_piece, combination_state, callback) {

        this.serverIO.emit(
            "move_piece",
            {token: this.token, from_piece, to_piece, combination_state},
            callback
        )
    };
}

export function configureAPI(connection, gameStartCallback, movePieceCallback) {
    return new API(connection, gameStartCallback, movePieceCallback)
}

export default configureAPI;
