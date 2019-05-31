// reactive/containers/Login.js

import React from "react";

export default class Login extends React.Component {
    render () {
        const {
            username,
            password,

            onUsernameChange,
            onPasswordChange,
            login
        } = this.props;

        return (
            <div className="game-info row justify-content-center">
                <div className="col-6">
                    <div>
                        <form onSubmit={(e) => {
                            e.preventDefault();
                            login()
                        }}>
                            <span className="input-header">Username</span>
                            <input
                                className="form-input"
                                value={username}
                                onChange={onUsernameChange}
                            />
                            <span className="input-header">Password</span>
                            <input
                                className="form-input"
                                type='password'
                                value={password}
                                onChange={onPasswordChange}
                            />
                            <button
                                type="submit"
                                className="form-input form-button"
                            >
                                Login
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        )
    }
}
