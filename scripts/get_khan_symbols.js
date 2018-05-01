/*
Extracts data on symbols from KaTeX.
*/
import symbols from './modules/KaTeX/src/symbols'
import macros from './modules/KaTeX/src/macros'
import functions from './modules/KaTeX/src/functions'

var fs = require('fs');

fs.writeFile("./data/functions.json", JSON.stringify(Object.keys(functions)), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("functions.json file created");
}); 

fs.writeFile("./data/macros.json", JSON.stringify(Object.keys(macros)), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("macros.json file created");
}); 

fs.writeFile("./data/symbols.json", JSON.stringify([...Object.keys(symbols['text']), ...Object.keys(symbols['math'])]), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("symbols.json file created");
}); 

// writes out the symbols with all the fields of data. Used to create features for split rules.
fs.writeFile("./data/symbols_full.json", JSON.stringify(symbols), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("symbols_full.json file created");
}); 

fs.writeFile("./data/macros_full.json", JSON.stringify(macros), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("macros_full.json file created");
}); 

fs.writeFile("./data/functions_full.json", JSON.stringify(functions), function(err) {
    if(err) {
        return console.log(err);
    }
    console.log("functions_full.json file created");
}); 
