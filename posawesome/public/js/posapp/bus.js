// Vue 2: new Vue() como event bus → NO existe en Vue 3
// Vue 3: se usa mitt (o similar)
import mitt from 'mitt';

const emitter = mitt();

export const evntBus = {
  $on: (event, handler) => emitter.on(event, handler),
  $off: (event, handler) => emitter.off(event, handler),
  $emit: (event, ...args) => emitter.emit(event, ...args),
};