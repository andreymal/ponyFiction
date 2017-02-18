import {ProvidePlugin, DefinePlugin, optimize} from 'webpack';
import ExtractTextPlugin from 'extract-text-webpack-plugin';
import path from 'path';
import fs from 'fs';

class VersionPlugin {
    constructor(options) {
        this.options = options;
    }

    apply(compiler) {
        compiler.plugin('done', (stats) => {
            fs.writeFileSync(
                "frontend.version",
                stats.hash
            )
        })
    }
}

export default {
    entry: {
        bootstrap: 'bootstrap-loader',
        styles: './assets/styles/main.scss',
        app: './assets/app/',
        vendor: ['jquery', 'jquery-ui']
    },
    output: {
        path: path.resolve(__dirname, "static", "[hash]"),
        publicPath: "./",
        filename: '[name].bundle.js'
    },
    module: {
        rules: [
            {
                test: /\.jsx?$/,
                loader: 'babel-loader',
                exclude: /node_modules/,
            },
            {
                test: /\.css$/,
                loader: ExtractTextPlugin.extract({
                    fallbackLoader: 'style-loader',
                    loader: 'css-loader?minimize=true&importLoaders=0'
                }),
            },
            {
                test: /\.scss$/,
                loader: ExtractTextPlugin.extract({
                    fallbackLoader: 'style-loader',
                    loader: 'css-loader?minimize=true&importLoaders=1!sass-loader',
                })
            },
            {
                test: /\.(woff2?|ttf|eot)$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: 'font/[hash:4].[ext]'
                }
            },
            {
                test: /\.(gif|png|jpg|jpeg|svg)$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: 'img/[hash:4].[ext]'
                }
            }
        ]
    },
    resolve: {
        modules: [process.env.NODE_PATH, path.resolve(__dirname)]
    },
    resolveLoader: {
        modules: [process.env.NODE_PATH]
    },
    plugins: [
        new ProvidePlugin({
            jQuery: 'jquery',
            $: 'jquery',
            jquery: 'jquery'
        }),
        new ExtractTextPlugin({
            filename: '[name].css',
            allChunks: true
        }),
        new DefinePlugin({
            'process.env': {
                NODE_ENV: JSON.stringify('production'),
            },
        }),
        new optimize.CommonsChunkPlugin({
            name: 'vendor',
            minChunks: Infinity
        }),
        new VersionPlugin()
    ]
}