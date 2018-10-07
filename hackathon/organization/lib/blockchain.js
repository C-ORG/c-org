const solc = require('solc');
const fs = require("fs");

module.exports = {

  // Compile solidity code
  compilation: (filename, warningFlag=false, errorFlag=true) => {

    const code = fs.readFileSync(filename).toString()
    const compiledCode = solc.compile(code)

    const errors = [];
    const warnings = [];
    (compiledCode.errors || []).forEach((err) => {
      if (/\:\s*Warning\:/.test(err)) {
        warnings.push(err);
      } else {
        errors.push(err);
      }
    });

    if (errorFlag && errors.length) {
      throw new Error('solc.compile: ' + errors.join('\n'));
    }
    if (warningFlag && warnings.length) {
      console.warn('solc.compile: ' + warnings.join('\n'));
    }

    return compiledCode;
  }

}
