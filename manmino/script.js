var csv;

$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "table.csv",
        dataType: "text",
        success: function(data) {processData(data);}
     });
});

function processData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var lines = [];

    for (var i=0; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data[0] == '' || data[1] == '')
            continue;
        var tarr = [];
        tarr.push(data[0]);
        tarr.push(data[1]);
        lines.push(tarr);
    }
    csv = lines;
}

var inputField = document.getElementById('search');
inputField.addEventListener('input', update);
var output = document.getElementById('output');

function update(){
    let inCurrent = inputField.value;
    let outNew = [];
    let outString = '';
    for(let character in inCurrent){
        outString += '(';
        for(let row in csv){
            for(let index in csv[row][1]){
                if(csv[row][1][index] == inCurrent[character]){
                    if(outNew[character] === undefined){
                        outNew[character] = [];
                        outNew[character].push(csv[row][0]);
                        outString += csv[row][0];
                    }else if(!outNew[character].includes(csv[row][0])){
                        outNew[character].push(csv[row][0]);
                        outString += ', ' + csv[row][0];
                    }
                }
            }
        }
        outString += ')';
    }
    console.log(inputField, outNew);
    output.innerText = outString;
}
