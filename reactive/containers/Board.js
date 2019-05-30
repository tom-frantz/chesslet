import React from 'react';
import {ChessPiece} from '../components/ChessPiece.js';

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


        if (pieceSelected) {
            const pos = pieceSelected.key;
            const from_pos = {x: pos % 6, y: Math.floor(pos / 6)};
            const to_pos = {x: i % 6, y: Math.floor(i / 6)};

            if (
                Board.hasAMoveset(subPiece, i) ||
                Board.hasAMoveset(pieceSelected, i)
            ) {
                const combination_state = subPiece ?
                    subPiece.props.piece :
                    pieceSelected.props.piece;

                console.log("SPLIT");
                api.move_piece(gameUUID, from_pos, to_pos, combination_state, (res) => {
                    if (res.success) {
                        this.cleanState();
                    }
                });
                return;
            }
        }

        const square = squares[i];
        if (square == null) {
            this.cleanState();
            return;
        }

        if (
            square.props.color === 'white' && ourTurn && weAre === "White" ||
            square.props.color === 'black' && ourTurn && weAre === "Black"
        ) {
            if (i >= 100) {
                this.setState({
                    subPiece: square,
                });
            } else {
                this.setState({
                    pieceSelected: square,
                    pieceCombination: square.props.piece,
                    subPiece: null,
                });
            }
        }
    }

    cleanState() {
        this.setState({
            subPiece: null,
            pieceSelected: null,
            pieceCombination: null,
        });
    }

    static hasAMoveset = (piece, i) => {
        if (piece === null) {
            return false
        }

        return piece.props.rookMoveset.includes(i) ||
            piece.props.bishopMoveset.includes(i) ||
            piece.props.knightMoveset.includes(i);
    };

// Squares
    renderGrid(size, squares) {
        const {pieceSelected, subPiece} = this.state;
        const {weAre} = this.props;

        const table = [];
        let squareNo = 0;

        for (let i = 0; i < size; i++) {
            let squareArr = [];
            for (let j = 0; j < size; j++) {
                let counter = squareNo;
                let className = 'square';
                let subPiecesArr = ['', '', ''];
                if (pieceSelected != null) {

                    if (subPiece != null) {
                        if (Board.hasAMoveset(subPiece, counter)) {
                            className += ' selected';
                        }
                    } else if (Board.hasAMoveset(pieceSelected, counter)) {
                        className += ' selected';
                    }


                    if (
                        squares[squareNo] != null &&
                        squares[squareNo].key == pieceSelected.key
                    ) {
                        className += ' piece-selected';
                        if (pieceSelected.props.piece.length > 1) {
                            for (let k = 0; k < pieceSelected.props.piece.length; k++) {
                                let color = weAre.toLowerCase();

                                let divName = 'position-absolute sub' + k;
                                let pieceClass = 'square sub-piece';

                                let piece = [this.state.pieceCombination[k]];
                                let rookMoves = [];
                                let bishopMoves = [];
                                let knightMoves = [];

                                if (this.state.pieceCombination[k] === "Rook") {
                                    rookMoves = this.state.pieceSelected.props.rookMoveset;
                                }
                                if (this.state.pieceCombination[k] === "Bishop") {
                                    bishopMoves = this.state.pieceSelected.props.bishopMoveset;
                                }
                                if (this.state.pieceCombination[k] === "Knight") {
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

                                if (subPiece != null) {
                                    if (newSubPiece.key == subPiece.key) {
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

        const allPieces = [].concat(boardState.player_1, boardState.player_2);

        for (const piece of allPieces) {
            let position = piece.position.x + (piece.position.y * 6);
            let rookMoves = [];
            let bishopMoves = [];
            let knightMoves = [];

            let validMovePositions = piece.valid_move_positions;

            for (let j = 0; j < validMovePositions.Rook.length; j++) {
                rookMoves.push(validMovePositions.Rook[j].x +
                    (validMovePositions.Rook[j].y * 6));
            }

            for (let j = 0; j < validMovePositions.Bishop.length; j++) {
                bishopMoves.push(validMovePositions.Bishop[j].x +
                    (validMovePositions.Bishop[j].y * 6));
            }

            for (let j = 0; j < validMovePositions.Knight.length; j++) {
                knightMoves.push(validMovePositions.Knight[j].x +
                    (validMovePositions.Knight[j].y * 6));
            }

            squares[position] = <ChessPiece
                color={boardState.player_1.includes(piece) ? 'black' : 'white'}
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
        const {weAre, ourTurn, boardState} = this.props;
        let status;
        boardState.winner != null ?
            status = boardState.winner + " has Won!" :
            status = 'Next player: ' + (weAre === "White" && ourTurn || weAre === "Black" && !ourTurn ? 'White' : 'Black');

        return (
            <div className="game">
                <div className="game-board">
                    <div>
                        <div className="status">
                            <div className="row status">
                                <div className="col-4">
                                    <div className="font-italic">Game UUID: {this.props.gameUUID}</div>
                                </div>
                                <div className="col-4">
                                    <div className="font-italic">You are: {this.props.weAre}</div>
                                </div>
                            </div>
                            <div>{status}</div>
                            <div className="font-weight-bold">Score for player 1: {boardState.player_1_score}</div>
                            <div className="font-weight-bold">Score for player 2: {boardState.player_2_score}</div>
                        </div>
                        {this.renderGrid(SIZE, squares)}
                        <br/>
                    </div>
                </div>
            </div>
        );
    }
}
