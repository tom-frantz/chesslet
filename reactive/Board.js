import React from 'react';
import {ChessPiece} from './ChessPiece.js';
import './App.css';


const SIZE = 6;

// {name, onClick, value} === props and const {name, onClick, value} = this.props;
function Square({name, divName, onClick, value, subPieces}) {
    return (
        <div className={divName}>
            <button
                className={name}
                onClick={onClick}
            >
                {value}
            </button>
            {subPieces}
        </div>
    );
}

export class Board extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            subPiece: null,
            pieceSelected: null,
            pieceCombination: null,
        };
    }

    // Squares
    handleClick(i, squares) {
        const {pieceSelected, subPiece} = this.state;
        const {ourTurn, weAre, gameUUID, api} = this.props;


        if(pieceSelected){
            if(subPiece){
                if(subPiece.props.rookMoveset.includes(i) ||
                    subPiece.props.bishopMoveset.includes(i) ||
                    subPiece.props.knightMoveset.includes(i)){
                        const pos = pieceSelected.key;
                        const from_pos = {x: pos % 6, y: Math.floor(pos / 6)};
                        const to_pos = {x: i % 6, y: Math.floor(i / 6)};
                        const combination_state = {
                            combination_state: subPiece.props.piece
                        };

                        console.log("SPLIT");
                        api.move_piece(gameUUID, from_pos, to_pos, combination_state, (res) => {
                            if (res.success) {
                                this.setState({
                                    subPiece: null,
                                    pieceSelected: null,
                                    pieceCombination: null,
                                });
                            }
                        });
                        return;
                    }
            }else{
                if(pieceSelected.props.rookMoveset.includes(i) ||
                    pieceSelected.props.bishopMoveset.includes(i) ||
                    pieceSelected.props.knightMoveset.includes(i)){
                    const pos = pieceSelected.key;
                    const from_pos = {x: pos % 6, y: Math.floor(pos / 6)};
                    const to_pos = {x: i % 6, y: Math.floor(i / 6)};
                    const combination_state = {
                        combination_state: pieceSelected.props.piece
                    };

                    console.log("MOVE");
                    api.move_piece(gameUUID, from_pos, to_pos, combination_state, (res) => {
                        if (res.success) {
                            this.setState({
                                subPiece: null,
                                pieceSelected: null,
                                pieceCombination: null,
                            });
                        }
                    });
                    return;
                }
            }
        }

        if (squares[i] == null) {
            this.setState({
                subPiece: null,
                pieceSelected: null,
                pieceCombination: null,
            });
            return;
        }

        if(squares[i].props.color === 'white' || ourTurn && weAre === "White"){
            if(i >= 100){
                this.setState({
                    subPiece: squares[i],
                });
            }else{
                this.setState({
                    pieceSelected: squares[i],
                    pieceCombination: squares[i].props.piece,
                    subPiece: null,
                });
            }
            return;
        }else if(squares[i].props.color === 'black' || ourTurn && weAre === "Black"){
            if(i >= 100){
                this.setState({
                    subPiece: squares[i],
                });
            }else{
                this.setState({
                    pieceSelected: squares[i],
                    pieceCombination: squares[i].props.piece,
                    subPiece: null,
                });
            }
            return;
        }
    }

    // Squares
    renderGrid(size, squares) {
        const {pieceSelected, subPiece} = this.state;

        const table = [];
        let squareNo = 0;

        for (let i = 0; i < size; i++) {
            let squareArr = [];
            for (let j = 0; j < size; j++) {
                let counter = squareNo;
                let className = 'square';
                let subPiecesArr = ['', '', ''];
                if(pieceSelected != null){
                    if(subPiece != null){
                        if(subPiece.props.rookMoveset.includes(counter) ||
                            subPiece.props.bishopMoveset.includes(counter) ||
                            subPiece.props.knightMoveset.includes(counter)){
                            className += ' selected';
                        }
                    }else{
                        if(pieceSelected.props.rookMoveset.includes(counter) ||
                            pieceSelected.props.bishopMoveset.includes(counter) ||
                            pieceSelected.props.knightMoveset.includes(counter)){
                            className += ' selected';
                        }
                    }
                    if(squares[squareNo] != null &&
                        squares[squareNo].key == pieceSelected.key){
                        className += ' piece-selected';
                        if(pieceSelected.props.piece.length > 1){
                            for(let k = 0; k < pieceSelected.props.piece.length; k++){
                                let color = 'white';
                                if (this.props.weAre === 'Black') {
                                    color = 'black';
                                }
                                let divName = 'position-absolute sub' + k;
                                let pieceClass = 'square sub-piece';
                                let piece = [this.state.pieceCombination[k]]
                                let rookMoves = [];
                                let bishopMoves = [];
                                let knightMoves = [];
                                if(this.state.pieceCombination[k] == "Rook"){
                                    rookMoves = this.state.pieceSelected.props.rookMoveset;
                                }
                                if(this.state.pieceCombination[k] == "Bishop"){
                                    bishopMoves = this.state.pieceSelected.props.bishopMoveset;
                                }
                                if(this.state.pieceCombination[k] == "Knight"){
                                    knightMoves = this.state.pieceSelected.props.knightMoveset;
                                }
                                let newSubPiece = <ChessPiece
                                    color={color}
                                    piece={piece}
                                    rookMoveset={rookMoves}
                                    bishopMoveset={bishopMoves}
                                    knightMoveset={knightMoves}
                                    key={100 + k}
                                    />;
                                if(subPiece != null){
                                    if(newSubPiece.key == subPiece.key){
                                        className = 'square';
                                        pieceClass += ' piece-selected';
                                    }
                                }
                                squares[newSubPiece.key] = newSubPiece;
                                subPiecesArr[k] = <Square
                                    divName={divName}
                                    name={pieceClass}
                                    value={newSubPiece}
                                    onClick={() => this.handleClick(newSubPiece.key, squares)}
                                    subPieces=''
                                    />;
                            }
                        }
                    }
                }
                let square = <Square
                    divName='position-relative square-container'
                    name={className}
                    value={squares[squareNo]}
                    onClick={() => this.handleClick(counter, squares)}
                    subPieces={<>{subPiecesArr[0]}{subPiecesArr[1]}{subPiecesArr[2]}</>}
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
        const {boardState} = this.props;

        let squares = Array(36).fill(null);
        for(const piece of boardState.player_1){
            let position = piece.position.x + (piece.position.y * 6);
            let rookMoves = [];
            let bishopMoves = [];
            let knightMoves = [];

            let validMovePositions = piece.valid_move_positions;

            for (let j = 0; j < validMovePositions.Rook.length; j++){
                rookMoves.push(validMovePositions.Rook[j].x +
                    (validMovePositions.Rook[j].y * 6));
            }

            for (let j = 0; j < validMovePositions.Bishop.length; j++){
                bishopMoves.push(validMovePositions.Bishop[j].x +
                    (validMovePositions.Bishop[j].y * 6));
            }

            for (let j = 0; j < validMovePositions.Knight.length; j++){
                knightMoves.push(validMovePositions.Knight[j].x +
                    (validMovePositions.Knight[j].y * 6));
            }

            squares[position] = <ChessPiece
                color={'black'}
                piece={piece.combination_state}
                rookMoveset={rookMoves}
                bishopMoveset={bishopMoves}
                knightMoveset={knightMoves}
                key={position}
            />;
        }

        for(const piece of boardState.player_2){
            let position = piece.position.x + (piece.position.y * 6);
            let rookMoves = [];
            let bishopMoves = [];
            let knightMoves = [];

            const validMovePositions1 = piece.valid_move_positions;

            for (let j = 0; j < validMovePositions1.Rook.length; j++){
                rookMoves.push(validMovePositions1.Rook[j].x +
                    (validMovePositions1.Rook[j].y * 6));
            }

            for (let j = 0; j < validMovePositions1.Bishop.length; j++){
                bishopMoves.push(validMovePositions1.Bishop[j].x +
                    (validMovePositions1.Bishop[j].y * 6));
            }

            for (let j = 0; j < validMovePositions1.Knight.length; j++){
                knightMoves.push(validMovePositions1.Knight[j].x +
                    (validMovePositions1.Knight[j].y * 6));
            }

            squares[position] = <ChessPiece
                color={'white'}
                piece={piece.combination_state}
                rookMoveset={rookMoves}
                bishopMoveset={bishopMoves}
                knightMoveset={knightMoves}
                key={position}
            />;
        }
        return squares;
    }

    render() {
        const squares = this.placePieces();
        let status = 'Next player: ' + (this.state.whiteIsNext ? 'White' : 'Black');

        return (
            <div>
                <div className="status">{status}</div>
                <div className="status">we are: {this.props.weAre}</div>
                <div className="status">Game UUID: {this.props.gameUUID}</div>
                {this.renderGrid(SIZE, squares)}
                <br/>
            </div>
        );
    }
}
