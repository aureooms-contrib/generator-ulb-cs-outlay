'use strict';
const Generator = require('yeoman-generator');
const chalk = require('chalk');
const yosay = require('yosay');

const isValid = require('date-fns/is_valid');
const format = require('date-fns/format');
const yaml = require('yaml');

module.exports = class extends Generator {
  // Constructor(args, opts) {
  // super(args, opts);
  // }

  initializing() {
    // Check for existing config
  }

  async prompting() {
    // Have Yeoman greet the user.
    this.log(
      yosay(
        `Welcome to the remarkable ${chalk.red('generator-ulb-cs-outlay')} generator!`
      )
    );

    const prompts = [
      {
        name: 'firstname',
        message: 'What is your first name?',
        filter: input => input.trim(),
        store: true
      },
      {
        name: 'lastname',
        message: 'What is your last name?',
        filter: input => input.trim(),
        store: true
      },
      {
        name: 'address',
        message: 'What is your address?',
        filter: input => input.trim(),
        store: true
      },
      {
        name: 'title',
        message: 'What is the name of the event you attended?',
        filter: input => input.trim()
      },
      {
        name: 'location',
        message: 'Where did it happen (<city> (<country>))?',
        filter: input => input.trim()
      },
      {
        name: 'begin',
        message: 'When did it begin (YYYY-MM-DD)?',
        validate: input => isValid(new Date(input)) || 'Invalid date',
        filter: input => format(new Date(input), 'YYYY-MM-DD')
      },
      {
        name: 'end',
        message: 'When did it end (YYYY-MM-DD)?',
        validate: input => isValid(new Date(input)) || 'Invalid date',
        filter: input => format(new Date(input), 'YYYY-MM-DD')
      }
    ];

    this.answers = await this.prompt(prompts);
  }

  writing() {
    this.fs.copy(this.templatePath('generator'), this.destinationPath('generator'));

    const data = yaml.stringify(this.answers);
    this.fs.write(this.destinationPath('data.yml'), data);

    this.fs.copy(this.templatePath('Makefile'), this.destinationPath('Makefile'));

    this.fs.copy(this.templatePath('README.md'), this.destinationPath('README.md'));

    this.fs.copy(this.templatePath('gitignore'), this.destinationPath('.gitignore'));
  }
};
