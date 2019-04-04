const path = require('path');
const HtmlWebPackPlugin = require('html-webpack-plugin');

module.exports = {
    mode: "development",
    devtool: "heap-module-inline-source-map",
    target: 'electron-main',
    entry: {
        index: path.resolve(__dirname, "./reactive/index.js")
    },
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "bundle.js"
    },
    watch: false,
    watchOptions: {
        aggregateTimeout: 1000,
        poll: 1000,
        ignored: /node_modules/
    },
    module: {
        rules: [
            {
                test: /\.js?$/,
                exclude: "/node_modules/",
                use: {
                    loader: "babel-loader",
                }
            }, {
                test: /\.html$/,
                use: {
                    loader: "html-loader"
                }
            }, {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            }, {
                test: /\.png?$/,
                use: {
                    loader: "file-loader",
                    options: {
                        name: './resources/[name].[ext]'
                    }
                }
            }, {
                test: /\.(eot|svg|ttf|woff|woff2)$/,
                use: {
                    loader: "file-loader",
                    options: {
                        name: './assets/[name].[ext]'
                    }
                }
            }
        ]
    },
    node: {
        fs: 'empty'
    },
    plugins: [
        new HtmlWebPackPlugin({
            template: path.resolve(__dirname, "./reactive/index.html"),
            filename: path.resolve(__dirname, "./dist/index.html"),
            chunks: ["index"]
        })
    ]
};
