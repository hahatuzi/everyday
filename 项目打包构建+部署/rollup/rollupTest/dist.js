(function () {
  'use strict';

  const fnA = () => {
    console.log('a');
  };

  fnA();
  console.log('hello rollup');
  // rollup -i index.js --file dist.js --format iife
  // rollup -i index.js

})();
