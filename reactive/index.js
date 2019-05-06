import React from "react";
import ReactDOM from "react-dom";
import {Board} from "./Board.js";
import API from "./api.js";

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            gameUUID: ""
        }
    }

    componentDidMount() {
    }

    onUsernameChange = (event) => {
        this.setState({
            username: event.target.value
        })
    };

    onPasswordChange = (event) => {
        this.setState({
            password: event.target.value
        })
    };

    onGameUUIDChange = (event) => {
        this.setState({
            gameUUID: event.target.value
        })
    };

    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board/>
                </div>
                <div className="game-info">
                    <div>
                        <form onSubmit={(e) => {
                            e.preventDefault();
                            API.login(
                                this.state.username,
                                this.state.password,
                                (res) => {
                                    console.log(res)
                                }
                            )
                        }}>
                            <input
                                value={this.state.username}
                                onChange={this.onUsernameChange}
                            />
                            <input
                                value={this.state.password}
                                onChange={this.onPasswordChange}
                            />
                            <button type="submit">Login</button>
                        </form>

                        <form onSubmit={(e) => {
                            e.preventDefault();
                            API.join_game(this.state.gameUUID, (res) => {
                                console.log(res);
                            })
                        }}>
                            <input
                                value={this.state.gameUUID}
                                onChange={this.onGameUUIDChange}
                            />
                            <button>Join Game</button>
                        </form>

                        <form onSubmit={(e) => {
                            e.preventDefault();
                            API.create_game((res) => {
                                console.log(res)
                            })
                        }}>
                            <button>Create new Game</button>
                        </form>
                    </div>
                    <div>{/* status */}</div>
                    <ol>{/* TODO */}</ol>
                </div>
            </div>
        );
    }
}


ReactDOM.render(
    <App/>,
    document.getElementById("react-entry")
);
