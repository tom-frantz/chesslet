import React from "react";
import ReactDOM from "react-dom";
import {Board} from "./Board.js";
import API from "./api.js";

class App extends React.Component {
    constructor (props) {
        super(props);

        this.state = {
            API: API
        }
    }


    render() {
        return (
            <div className="game">
                <div className="game-board">
                    <Board api={this.state.API}/>
                </div>
                <div className="game-info">
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
