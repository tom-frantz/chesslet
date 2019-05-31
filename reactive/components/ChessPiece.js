// reactive/components/ChessPiece.js

import React from 'react';
import '../css/App.css';

export class ChessPiece extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        let element;
        let color = "#aaaaaa";
        if (this.props.color === 'black') {
            color = '#000000';
        }

        if (this.props.piece.length == 1){
            if (this.props.piece[0] === 'Rook') {
                element = <i style={{color: color}} className='fas fa-chess-rook'/>;
            } else if (this.props.piece[0] === 'Bishop') {
                element = <i style={{color: color}} className='fas fa-chess-bishop'/>;
            } else if (this.props.piece[0] === 'Knight') {
                element = <i style={{color: color}} className='fas fa-chess-knight'/>;
            }
        }else{
            var pieceIcon1, pieceIcon2, pieceIcon3;
            for (let i = 0; i < this.props.piece.length; i++){
                if (this.props.piece[i] === 'Rook') {
                    pieceIcon1 = <i style={{color: color}} className='fas fa-chess-rook'/>;
                } else if (this.props.piece[i] === 'Bishop') {
                    pieceIcon2 = <i style={{color: color}} className='fas fa-chess-bishop'/>;
                } else if (this.props.piece[i] === 'Knight') {
                    pieceIcon3 = <i style={{color: color}} className='fas fa-chess-knight'/>;
                }
            }
            element = <>{pieceIcon1}{pieceIcon2}{pieceIcon3}</>
        }

        return (
            element
        )
    }
}
