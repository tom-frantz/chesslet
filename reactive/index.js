// reactive/index.js

import React from "react";
import ReactDOM from "react-dom";
import {configureAPI} from "./utils/api.js";
import 'bootstrap/dist/css/bootstrap.min.css';
import './css/App.css';

import {Board} from "./containers/Board.js";
import Login from "./containers/Login";
import ConnectToGame from "./containers/ConnectToGame";

class App extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            username: "",
            password: "",
            loggedIn: false,
            inGame: false,
            ourTurn: false,
            gameUUID: "",
            gameData: {
                player_1: [],
                player_2: []
            },
            // gameData: data,
            API: configureAPI(
                "http://0.0.0.0:5000/",
                (res, API) => {
                    console.log("GAME STARTED CALLBACK");
                    console.log("WE ARE:", res.b.player_1_uuid === API.token ? "Black" : "White");
                    this.setState({
                        gameData: res.b,
                        ourTurn: res.b.current_player === API.token,
                        weAre: res.b.player_1_uuid === API.token ? "Black" : "White"
                    });
                },
                (res, API) => {
                    console.log("PIECE MOVED CALLBACK!");
                    console.log("OUR TURN AFTER MOVE:", res.b.current_player === API.token);
                    this.setState({
                        gameData: res.b,
                        ourTurn: res.b.current_player === API.token
                    });
                }
            )
        }
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

    login = () => {
        this.state.API.login(
            this.state.username,
            this.state.password,
            (res) => {
                this.setState({loggedIn: res.success})
            }
        )
    };

    joinGame = () => {
        this.state.API.join_game(this.state.gameUUID, (res) => {
            this.setState({inGame: res.success})
        })
    };

    createGame = () => {
        this.state.API.create_game((res) => {
            this.setState({inGame: res.success, gameUUID: res.game_uuid})
        })
    };

    render() {
        const API = this.state.API;

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
                    {
                        this.state.loggedIn &&
                        this.state.inGame &&
                        <Board
                            api={API}
                            gameUUID={this.state.gameUUID}
                            boardState={this.state.gameData}
                            ourTurn={this.state.ourTurn}
                            weAre={this.state.weAre}
                        />
                    } {
                        this.state.loggedIn &&
                        !this.state.inGame &&
                        <ConnectToGame
                            gameUUID={this.state.gameUUID}
                            onGameUUIDChange={this.onGameUUIDChange}
                            joinGame={this.joinGame}
                            createGame={this.createGame}
                        />
                    } {
                        !this.state.loggedIn &&
                        <Login
                            username={this.state.username}
                            password={this.state.password}

                            onUsernameChange={this.onUsernameChange}
                            onPasswordChange={this.onPasswordChange}
                            login={this.login}
                        />
                    }
                </div>
            </div>
        );
    }
}


ReactDOM.render(
    <App/>,
    document.getElementById("react-entry")
);
