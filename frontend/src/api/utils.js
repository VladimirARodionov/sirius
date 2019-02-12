let _ = require('lodash')

export function flattenTree (tree) {
  function recurse (nodes, path) {
    return _.map(nodes, function (node) {
      var newPath = _.union(path, [node.name])
      return [
        _.assign({ pathname: newPath.join(' > '), level: path.length }, _.omit(node, 'children')),
        recurse(node.children, newPath)
      ]
    })
  }
  return _.flattenDeep(recurse(tree, []))
}

export function flattenJson (tree) {
  function recurse (nodes, path) {
    return _.map(nodes, function (node) {
      var newPath = _.union(path, [node.name])
      return [
        _.assign({ pathname: newPath.join(' > '), level: path.length }, _.omit(node, 'fields')),
        recurse(node.fields, newPath)
      ]
    })
  }
  return _.flattenDeep(recurse(tree, []))
}
