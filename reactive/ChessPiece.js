import React from 'react';
import './App.css';

export class ChessPiece extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);
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
            let pieceTitles = '';
            for (let i = 0; i < this.props.piece.length; i++){
                pieceTitles += this.props.piece[i] + '\n';
            }
            element = <span className='piece-text'>{pieceTitles}</span>;
        }

        return (
            element
        )
    }
}
