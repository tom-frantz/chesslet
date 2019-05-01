import React from 'react';
import './App.css';

export class ChessPiece extends React.Component {
    constructor(props) {
        super(props);
        console.log(props);

        // TODO
        this.state = {
            piece: this.props.piece
        };

        if (this.state.piece === 'rook') {
            this.state = {
                icon: 'fas fa-chess-rook',
                moveset: null,
            };
        } else if (this.state.piece === 'bishop') {
            this.state = {
                icon: 'fas fa-chess-bishop',
                moveset: null,
            };
        } else if (this.state.piece === 'knight') {
            this.state = {
                icon: 'fas fa-chess-knight',
                moveset: null,
            };
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
