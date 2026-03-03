const listeners = {};

export const evntBus = {
  $on(event, handler) {
    if (!listeners[event]) listeners[event] = [];
    listeners[event].push(handler);
  },
  $off(event, handler) {
    if (!listeners[event]) return;
    if (handler) {
      listeners[event] = listeners[event].filter(h => h !== handler);
    } else {
      listeners[event] = [];
    }
  },
  $emit(event, ...args) {
    if (!listeners[event]) return;
    listeners[event].forEach(handler => handler(...args));
  },
};