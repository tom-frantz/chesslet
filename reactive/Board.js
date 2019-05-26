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
            squares: squares,
            whiteIsNext: true,
            pieceSelected: null,
        };
    }

    handleClick(i) {
        const squares = this.state.squares.slice();
        if(this.state.pieceSelected){
            if(this.state.pieceSelected.props.moveset.includes(i)){
                console.log("MOVE");
                let pos = this.state.pieceSelected.key;
                var from_pos = {x: pos % 6, y: Math.floor(pos / 6)};
                var to_pos = {x: i % 6, y: Math.floor(i / 6)};
                var combination_state = {
                    combination_state: this.state.pieceSelected.combination_state
                }
                var JSONfrom_pos = JSON.stringify(from_pos);
                var JSONto_pos = JSON.stringify(to_pos);
                var JSONcombination_state = JSON.stringify(combination_state);
                this.props.api.move_piece(JSONfrom_pos, JSONto_pos, JSONcombination_state, (res) => {
                    console.log("somehting");
                });
                return;
            }
        }
        if (squares[i] == null) {
            this.setState({
                pieceSelected: null,
            });
            return;
        }
        if(squares[i].props.color === 'white' && this.state.whiteIsNext){
            this.setState({
                pieceSelected: squares[i],
            });
            return;
        }else if(squares[i].props.color === 'black' && !this.state.whiteIsNext){
            this.setState({
                pieceSelected: squares[i],
            });
            return;
        }
    }

    renderGrid(size) {
        const table = [];
        let squares = this.placePieces();
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
                    onClick={() => this.handleClick(counter)}
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

        let status = 'Next player: ' + (this.state.whiteIsNext ? 'White' : 'Black');

        return (
            <div>
                <div className="status">{status}</div>
                <div className="status">Game UUID: {this.props.gameUUID}</div>
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
