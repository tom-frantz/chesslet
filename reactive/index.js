import React from "react";
import ReactDOM from "react-dom";
import {Board} from "./Board.js";
import API, {configureAPI} from "./api.js";
import 'bootstrap/dist/css/bootstrap.min.css';

let data = require('./dummy.json'); //dummy data, delete later

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            loggedIn: true,
            inGame: true,
            gameUUID: "",
            gameData: {
                player_1: [],
                player_2: []
            },
            gameData: data,
            API: configureAPI(
                "http://10.132.36.3:5000/",
                (res) => {
                    console.log("YHEET?");
                    this.setState({gameData: res.b})},
                (res) => {this.setState({gameData: res.b})}
            )
        }
    }

    componentDidMount() {}

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
        const API = this.state.API;

        console.log(this.state.gameData);

        let body;
        // change this "if" to == for board, change to != for login
        if (this.state.loggedIn) {
            if (this.state.inGame) {
                body =
                    <div className="game">
                        <div className="game-board">
                            <Board
                                api = {API}
                                gameUUID={this.state.gameUUID}
                                boardState={this.state.gameData}
                            />
                        </div>
                    </div>;
            }else{
                body =
                    <div style={{marginLeft: "20px"}}>
                        <form onSubmit={(e) => {
                            e.preventDefault();
                            API.join_game(this.state.gameUUID, (res) => {
                                this.setState({inGame: res.success})
                            })
                        }}>
                            <span className="input-header">Game UUID</span>
                            <input
                                className="form-input"
                                value={this.state.gameUUID}
                                onChange={this.onGameUUIDChange}
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
                            API.create_game((res) => {
                                this.setState({inGame: res.success, gameUUID: res.game_uuid})
                            })
                        }}>
                            <button
                                type="submit"
                                className="form-input form-button"
                            >
                                Create new Game
                            </button>
                        </form>
                    </div>;
            }
        } else {
            body =
                <div className="game-info row justify-content-center">
                    <div className="col-6">
                        <div>
                            <form onSubmit={(e) => {
                                e.preventDefault();
                                API.login(
                                    this.state.username,
                                    this.state.password,
                                    (res) => {
                                        this.setState({loggedIn: res.success})
                                    }
                                )
                            }}>
                                <span className="input-header">Username</span>
                                <input
                                    className="form-input"
                                    value={this.state.username}
                                    onChange={this.onUsernameChange}
                                />
                                <span className="input-header">Password</span>
                                <input
                                    className="form-input"
                                    type='password'
                                    value={this.state.password}
                                    onChange={this.onPasswordChange}
                                />
                                <button
                                    type="submit"
                                    className="form-input form-button"
                                >
                                    Login
                                </button>
                            </form>
                        </div>
                        <div>{/* status */}</div>
                        <ol>{/* TODO */}</ol>
                    </div>
                </div>;
        }
        return (
            <div>
                <div className="container-fluid header-top">
                    <div className="row align-items-center justify-content-between">
                        <div className="col">
                            <div className="row">
                                <div className="col project-title">
                                    SEF Chesslet
                                </div>
                            </div>
                            <div className="row">
                                <div className="col">
                                    A Hey Mayne project
                                </div>
                            </div>
                        </div>
                        <div className="col-2 position-relative">
                            <div className="position-absolute vert-line"/>
                            <div className="row">
                                Tom Frantz
                            </div>
                            <div className="row">
                                Jack Belcher
                            </div>
                            <div className="row">
                                Flynn Calcutt
                            </div>
                            <div className="row">
                                Grace Kerr
                            </div>
                        </div>
                    </div>
                </div>
                <div className="container">
                    {body}
                </div>
            </div>
        );
    }
}


ReactDOM.render(
    <App/>,
    document.getElementById("react-entry")
);
