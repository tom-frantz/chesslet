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
