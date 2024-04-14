// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require('vscode');

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed

/**
 * @param {vscode.ExtensionContext} context
 */
const modelURL = "http://localhost:5000/predict";
function activate(context) {

	// Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "vsc" is now active!');
	
	// The command has been defined in the package.json file
	// Now provide the implementation of the command with  registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('vsc.detectRuntimeError', async function () {
		const activeEditor = vscode.window.activeTextEditor;
		if (activeEditor) {
		  // Get the code from the active editor and send it to the ML model
		  const code = activeEditor.document.getText();
		  const response = await fetch(modelURL, {
			method: "POST",
			body: JSON.stringify({ code }),
			headers: {
			  "Content-Type": "application/json",
			},
		  });
		  const data = await response.json();
		  console.log(data.predictions[0]);
		  vscode.window.showInformationMessage(data.predictions[0]);
		  if(data.predictions[0] === "1"){
			vscode.window.showInformationMessage("Runtime Error", 5000);
		  }
		  else{
			vscode.window.showInformationMessage("No Runtime Error", 5000);
		  }
		}
	});

	context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
function deactivate() {}

module.exports = {
	activate,
	deactivate
}
