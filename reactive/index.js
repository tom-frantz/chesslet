import React from "react";
import ReactDOM from "react-dom";
import App from './App';


class App extends React.Component {
    render() {
        return (
            <div>Entry Point</div>
        )
    }
}

ReactDOM.render(
    <App/>,
    document.getElementById("react-entry")
);
