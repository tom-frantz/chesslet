import React from 'react';
import {ChessPiece} from './ChessPiece.js';
import './App.css';

function Square(props) {
    return (
        <button
            className={props.name}
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
            pieceSelected: null,
        };
    }

    // Squares
    handleClick(i, squares) {
        const {pieceSelected} = this.state;

        if(pieceSelected){
            if(pieceSelected.props.moveset.includes(i)){
                console.log("MOVE");
                const pos = this.state.pieceSelected.key;
                const from_pos = {x: pos % 6, y: Math.floor(pos / 6)};
                const to_pos = {x: i % 6, y: Math.floor(i / 6)};
                const combination_state = {
                    combination_state: this.state.pieceSelected.combination_state
                };

                this.props.api.move_piece(this.props.gameUUID, from_pos, to_pos, combination_state, (res) => {
                    console.log(res);
                });
                return;
            }
        }

        console.log(squares[i]);

        if (squares[i] == null) {
            this.setState({
                pieceSelected: null,
            });
            return;
        }
        // TODO
        if(squares[i].props.color === 'white' && this.props.ourTurn && this.props.weAre === "white"){
            this.setState({
                pieceSelected: squares[i],
            });
            return;
        }else if(squares[i].props.color === 'black' && this.props.ourTurn && this.props.weAre === "black"){
            this.setState({
                pieceSelected: squares[i],
            });
            return;
        }
    }

    // Squares
    renderGrid(size, squares) {
        const table = [];
        let squareNo = 0;
        for (let i = 0; i < size; i++) {
            let squareArr = [];
            for (let j = 0; j < size; j++) {
                let counter = squareNo;
                let className = 'square';
                if(this.state.pieceSelected != null){
                    if(this.state.pieceSelected.props.moveset.includes(counter)){
                        className += ' selected';
                    }
                    if(squares[squareNo] != null &&
                        squares[squareNo].key == this.state.pieceSelected.key){
                        className += ' piece-selected';
                    }
                }
                let square = <Square
                    name={className}
                    value={squares[squareNo]}
                    onClick={() => this.handleClick(counter, squares)}
                    key={squareNo}
                />;
                squareArr.push(square);
                squareNo++;
            }
            table.push(<div className="board-row" key={i}>{squareArr}</div>)
        }
        return table;
    }

    // WHERE WE GET SQUARES FROM
    placePieces() {
        let squares = Array(36).fill(null);
        let pieces = this.props.boardState.player_1;
        for(let i = 0; i < pieces.length; i++){
            let position = pieces[i].position.x + (pieces[i].position.y * 6);
            let moves = [];
            let validMovePositions = pieces[i].valid_move_positions;
            for (let j = 0; j < validMovePositions.Rook.length; j++){
                moves.push(validMovePositions.Rook[j].x +
                    (validMovePositions.Rook[j].y * 6));
            }
            for (let j = 0; j < validMovePositions.Bishop.length; j++){
                moves.push(validMovePositions.Bishop[j].x +
                    (validMovePositions.Bishop[j].y * 6));
            }
            for (let j = 0; j < validMovePositions.Knight.length; j++){
                moves.push(validMovePositions.Knight[j].x +
                    (validMovePositions.Knight[j].y * 6));
            }
            squares[position] = <ChessPiece
                color={'black'}
                piece={pieces[i].combination_state}
                moveset={moves}
                key={position}
            />;
        }
        pieces = this.props.boardState.player_2;
        for(let i = 0; i < pieces.length; i++){
            let position = pieces[i].position.x + (pieces[i].position.y * 6);
            let moves = [];
            for (let j = 0; j < pieces[i].valid_move_positions.Rook.length; j++){
                moves.push(pieces[i].valid_move_positions.Rook[j].x +
                    (pieces[i].valid_move_positions.Rook[j].y * 6));
            }
            for (let j = 0; j < pieces[i].valid_move_positions.Bishop.length; j++){
                moves.push(pieces[i].valid_move_positions.Bishop[j].x +
                    (pieces[i].valid_move_positions.Bishop[j].y * 6));
            }
            for (let j = 0; j < pieces[i].valid_move_positions.Knight.length; j++){
                moves.push(pieces[i].valid_move_positions.Knight[j].x +
                    (pieces[i].valid_move_positions.Knight[j].y * 6));
            }
            squares[position] = <ChessPiece
                color={'white'}
                piece={pieces[i].combination_state}
                moveset={moves}
                key={position}
            />;
        }
        return squares;
    }

    render() {
        const API = this.props.api;
        const squares = this.placePieces();
        let status = 'Next player: ' + (this.state.whiteIsNext ? 'White' : 'Black');

        return (
            <div>
                <div className="status">{status}</div>
                <div className="status">Game UUID: {this.props.gameUUID}</div>
                {this.renderGrid(this.state.size, squares)}
                <br/>
            </div>
        );
    }
}
