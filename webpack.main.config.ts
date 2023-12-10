import type { Configuration } from 'webpack';

import { rules } from './webpack.rules';



rules.push({
  test: /\.jsx$/,
  exclude: /node_modules/, 
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react', '@babel/preset-env'], // These presets ensure compatibility with React and modern browsers
          },
        },
});


export const mainConfig: Configuration = {
  /**
   * This is the main entry point for your application, it's the first file
   * that runs in the main process.
   */
  entry: {
    main:'./src/index.ts',
  },
  // Put your normal webpack config below here
  module: {
    rules,
  },
  resolve: {
    extensions: ['.js', '.ts', '.jsx', '.tsx', '.css', '.json'],
  },
};
