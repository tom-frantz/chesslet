class API {
    // ur api c:

    movePiece() {
        return new Promise(
            (resolve, reject) => {
                setTimeout(() => resolve({"x": 10}), 3000);
                reject("Some error here")
            }
        )
    };
}

export default new API()

// Different File

new API().movePiece()
    .then((data) => this.setState(data))
    .catch((err) => this.handleError(err));
