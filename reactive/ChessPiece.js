import React from 'react';
import './App.css';

export class ChessPiece extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);

        if (this.props.piece.length == 1){
            if (this.props.piece[0] === 'Rook') {
                this.state = {
                    icon: 'fas fa-chess-rook',
                };
            } else if (this.props.piece[0] === 'Bishop') {
                this.state = {
                    icon: 'fas fa-chess-bishop',
                };
            } else if (this.props.piece[0] === 'Knight') {
                this.state = {
                    icon: 'fas fa-chess-knight',
                };
            }
        }
    }

    render() {
        let color = "#aaaaaa";
        if (this.props.color === 'black') {
            color = '#000000';
        }

        return (
            <i style={{color: color}} className={this.state.icon}/>
        )
    }
}
