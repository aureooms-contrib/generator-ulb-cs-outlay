'use strict';
const path = require('path');
const assert = require('yeoman-assert');
const helpers = require('yeoman-test');

describe('generator-ulb-cs-outlay:app', () => {
  beforeAll(() => {
    return helpers.run(path.join(__dirname, '../generators/app')).withPrompts({
      firstname: 'John',
      lastname: 'Doe',
      address: '1 Church Street, 123456 Neverland',
      title: 'Medium-sized Conference',
      location: 'Small-sized City (Big-sized Country)',
      begin: '1974-02-27',
      end: '1974-03-03'
    });
  });

  it('creates files', () => {
    assert.file(['.gitignore', 'Makefile', 'README.md', 'data.yml']);
  });
});
