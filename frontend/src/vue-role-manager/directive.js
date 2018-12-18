export default manager => ({
  inserted (el, binding) {
    let hasAccess
    if (typeof binding.value === 'function') {
      hasAccess = binding.value()
    } else {
      hasAccess = manager.hasAccess(binding.value)
    }

    if (hasAccess) {
      return
    }

    /*
      arg: action, class

      modifiers:
      action => remove, hidden, disable
      class => any string
      */
    const arg = binding.arg

    // modifiers: remove hidden disable
    let modifiers = binding.modifiers
      ? binding.modifiers
      : {
        remove: true
      }

    if (arg === 'action') {
      if (modifiers.remove) {
        el.parentElement && el.parentElement.removeChild(el)
      } else if (modifiers.hidden) {
        el.style.display = 'none'
      } else if (modifiers.disable) {
        el.disabled = true
      }
    } else if (arg === 'class') {
      Object.keys(binding.modifiers).map(cls => (el.className += ' ' + cls))
    } else {
      el.parentElement && el.parentElement.removeChild(el)
    }
  }
})
