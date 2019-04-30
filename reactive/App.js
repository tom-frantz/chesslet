import React, { Component } from 'react';
import logo from './logo.svg';
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

class Board extends React.Component {
  constructor(props) {
    super(props);
    let squares = this.startingPieces();
    this.state = {
      size: 6,
      squares: squares,
      whiteIsNext: true,
    };
  }

  handleClick(i){
    const squares = this.state.squares.slice();
    if(squares[i]){
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
           />
  };

  renderGrid(size) {
      let table = [];
      let squareNo = 0;
      for(let i = 0; i < size; i++) {
          let square = [];
          for (let j = 0; j < size; j++) {
              square.push(this.renderSquare(squareNo))
              squareNo++;
          }
          table.push(<div className="board-row">{square}</div>)
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

  startingPieces(){
      let squares = Array(36).fill(null);
      squares[0] = "Black\n Rook"
      squares[1] = "Black\n Bishop"
      squares[2] = "Black\n Knight"
      squares[3] = "Black\n Knight"
      squares[4] = "Black\n Bishop"
      squares[5] = "Black\n Rook"
      squares[30] = "White\n Rook"
      squares[31] = "White\n Bishop"
      squares[32] = "White\n Knight"
      squares[33] = "White\n Knight"
      squares[34] = "White\n Bishop"
      squares[35] = "White\n Rook"
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

class App extends React.Component {
  render() {
    return (
      <div className="game">
        <div className="game-board">
          <Board />
        </div>
        <div className="game-info">
          <div>{/* status */}</div>
          <ol>{/* TODO */}</ol>
        </div>
      </div>
    );
  }
}

export default App;
