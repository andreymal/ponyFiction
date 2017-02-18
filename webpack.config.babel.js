import {ProvidePlugin, DefinePlugin, optimize} from 'webpack';
import ExtractTextPlugin from 'extract-text-webpack-plugin';
import path from 'path';
import fs from 'fs';


const isLocal = process.env.NODE_ENV === 'local';

function getOutputPath() {
    const chunks = [__dirname, "static"];
    if (!isLocal) {
        chunks.push('[hash]');
    }
    return path.resolve(...chunks);
}

function getNaming() {
    if (!isLocal) {
        return '[hash:4].[ext]';
    }
    return '[name].[ext]';
}

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

const configuration = {
    entry: {
        bootstrap: 'bootstrap-loader',
        styles: './assets/styles/main.scss',
        app: './assets/app/',
        vendor: ['jquery', 'jquery-ui']
    },
    output: {
        path: getOutputPath(),
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
                test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: 'url-loader',
                options: {
                    name: getNaming()
                }
            },
            {
                test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
                loader: 'file-loader',
                options: {
                    name: getNaming()
                }
            },
            {
                test: /\.(gif|png|jpg|jpeg)$/,
                loader: 'url-loader',
                options: {
                    limit: 10000,
                    name: `img/${getNaming()}`
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
        new optimize.CommonsChunkPlugin({
            name: 'vendor',
            minChunks: Infinity
        }),
    ]
};

if (!isLocal) {
    configuration.plugins.push(new VersionPlugin())
}

export default configuration;
