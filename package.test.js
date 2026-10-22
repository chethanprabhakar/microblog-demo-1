const test = require('node:test');
const assert = require('node:assert');

test('package.json is a valid private manifest', () => {
  const pkg = require('./package.json');
  assert.strictEqual(pkg.name, 'microblog');
  assert.strictEqual(pkg.private, true);
  assert.strictEqual(pkg.main, undefined);
});
