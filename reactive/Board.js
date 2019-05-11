import React from 'react';
import {ChessPiece} from './ChessPiece.js';
import './App.css';

function Square(props) {
    return (
        <button
            className="square"
            onClick={props.onClick}
        >
            {props.value}
        </button>
    );
}

export class Board extends React.Component {
    constructor(props) {
        super(props);
        let squares = this.placePieces();
        this.state = {
            size: 6,
            squares: squares,
            whiteIsNext: true,
        };
    }

    handleClick(i) {
        const squares = this.state.squares.slice();
        if (squares[i]) {
            return;
        }
        squares[i] = this.state.whiteIsNext ? 'White' : 'Black';
        this.setState({
            squares: squares,
            whiteIsNext: !this.state.whiteIsNext,
        });
    }

    renderSquare(i) {
        return <Square
            value={this.state.squares[i]}
            onClick={() => this.handleClick(i)}
            key={i}
        />
    };

    renderGrid(size) {
        const table = [];
        let squares = this.placePieces();
        let squareNo = 0;
        for (let i = 0; i < size; i++) {
            let squareArr = [];
            for (let j = 0; j < size; j++) {
                let square = <Square
                    value={squares[squareNo]}
                    onClick={() => this.handleClick(i)}
                    key={squareNo}
                />;
                squareArr.push(square);
                squareNo++;
            }
            table.push(<div className="board-row" key={i}>{squareArr}</div>)
        }
        return table;
    }

    resetBoard() {
        let squares = this.placePieces();
        this.setState({
            size: 6,
            squares: squares,
            whiteIsNext: true,
        });
    }

    placePieces() {
        let squares = Array(36).fill(null);
        let pieces = this.props.boardState.player_1;
        for(let i = 0; i < pieces.length; i++){
            let position = pieces[i].position.x + (pieces[i].position.y * 6);
            squares[position] = <ChessPiece
                color={'black'}
                piece={pieces[i].combination_state}
                moveset={pieces[i].valid_move_positions}
            />;
        }
        pieces = this.props.boardState.player_2;
        for(let i = 0; i < pieces.length; i++){
            let position = pieces[i].position.x + (pieces[i].position.y * 6);
            squares[position] = <ChessPiece
                color={'white'}
                piece={pieces[i].combination_state}
                moveset={pieces[i].valid_move_positions}
            />;
        }
        return squares;
    }

    render() {
        let status = 'Next player: ' + (this.state.whiteIsNext ? 'White' : 'Black');

        return (
            <div>
                <div className="status">{status}</div>
                {this.renderGrid(this.state.size)}
                <br/>
                <button
                    onClick={() => this.resetBoard()}
                >
                    reset
                </button>
            </div>
        );
    }
}
