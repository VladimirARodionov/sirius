'use strict'
module.exports = {
  assetsPublicPath: '/sirius/',
  NODE_ENV: '"production"',
  API_URL: '"/crm"',
  optimization: {
    runtimeChunk: true,
    splitChunks: {
      cacheGroups: {
        commons: {
          chunks: 'initial',
          name: 'commons',
          test: 'commons',
          enforce: true,
          minChunks: 2
        }
      }
    }
  }
}
