// reactive/containers/ConnectToGame.js

import React from "react";


export default class ConnectToGame extends React.Component {
    render() {
        const {
            gameUUID,
            onGameUUIDChange,

            joinGame,
            createGame
        } = this.props;

        return (
            <div style={{marginLeft: "20px"}}>
                <form onSubmit={(e) => {
                    e.preventDefault();
                    joinGame();
                }}>
                    <span className="input-header">Game UUID</span>
                    <input
                        className="form-input"
                        value={gameUUID}
                        onChange={onGameUUIDChange}
                    />
                    <button
                        type="submit"
                        className="form-input form-button"
                    >
                        Join Game
                    </button>
                </form>

                <span className="or-text">
                    or
                </span>

                <form onSubmit={(e) => {
                    e.preventDefault();
                    createGame()
                }}>
                    <button
                        type="submit"
                        className="form-input form-button"
                    >
                        Create new Game
                    </button>
                </form>
            </div>
        )
    }
}
