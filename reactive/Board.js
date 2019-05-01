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
        let squares = this.startingPieces();
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
        let squareNo = 0;
        for (let i = 0; i < size; i++) {
            let square = [];
            for (let j = 0; j < size; j++) {
                square.push(this.renderSquare(squareNo));
                squareNo++;
            }
            table.push(<div className="board-row" key={i}>{square}</div>)
        }
        return table;
    }

    resetBoard() {
        let squares = this.startingPieces();
        this.setState({
            size: 6,
            squares: squares,
            whiteIsNext: true,
        });
    }

    startingPieces() {
        let squares = Array(36).fill(null);
        squares[0] = <ChessPiece color={'black'} piece={'rook'}/>;
        squares[1] = <ChessPiece color={'black'} piece={'bishop'}/>;
        squares[2] = <ChessPiece color={'black'} piece={'knight'}/>;
        squares[3] = <ChessPiece color={'black'} piece={'knight'}/>;
        squares[4] = <ChessPiece color={'black'} piece={'bishop'}/>;
        squares[5] = <ChessPiece color={'black'} piece={'rook'}/>;
        squares[30] = <ChessPiece color={'white'} piece={'rook'}/>;
        squares[31] = <ChessPiece color={'white'} piece={'bishop'}/>;
        squares[32] = <ChessPiece color={'white'} piece={'knight'}/>;
        squares[33] = <ChessPiece color={'white'} piece={'knight'}/>;
        squares[34] = <ChessPiece color={'white'} piece={'bishop'}/>;
        squares[35] = <ChessPiece color={'white'} piece={'rook'}/>;
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
