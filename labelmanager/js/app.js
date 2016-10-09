//  Copyright 2016 Google Inc. All Rights Reserved.
//  
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//  
//      http://www.apache.org/licenses/LICENSE-2.0
//  
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License. 

var chosenDirectory = null;
var apiKey = null;
var chooseDirButton = document.querySelector('#choose_dir');
var updateKeyButton = document.querySelector('#update_key');
var apiKeyBox = document.querySelector('#api_key');
var resetSessionButton = document.querySelector('#reset_session');
var directoryBox = document.querySelector('#directory');
var output = document.querySelector('#output');


function loadInitialFile(launchData) {
    chrome.storage.local.get(['selectedDir', 'apiKey'], function(items) {
      if (items.selectedDir) {
        // if an entry was retained earlier, see if it can be restored
        chrome.fileSystem.isRestorable(items.selectedDir, function(bIsRestorable) {
          // the entry is still there, load the content
          console.info("Restoring " + items.selectedDir);
          chrome.fileSystem.restoreEntry(items.selectedDir, function(dir) {
            if (dir) {
              chosenDirectory = dir;
              chrome.fileSystem.getDisplayPath(dir, function(path) {
                directoryBox.value = path;
              });
            }
          });
        });
      } 
      if (items.apiKey) {
        apiKeyBox.value = items.apiKey;
        apiKey = items.apiKey;
      }
    });
    setInterval(run, 30000);
}

/*
 * getJSON is a simple XMLHttpRequest wrapper that parses JSON response.
 */
function getJSON(url, callback){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200){
            callback(JSON.parse(xmlhttp.responseText));
        } else if (xmlhttp.readyState == 4 && xmlhttp.status != 200) {
            output.innerHTML = "Failed. (Response Code: " + xmlhttp.status + ")";
        }
    }
    xmlhttp.open("GET", url, true);
    xmlhttp.send();
        
}

function resetSession(){
    var xmlhttp;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.open("POST", "https://www.livestreamalerts.com/reset_session", true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send("reset=true&key="+apiKey);
}

function handleData(data) {
    var count = 0;
    for (var i in data) {
        writeFile(chosenDirectory, i + ".txt", data[i]);
        count += 1;
    }
    var d = new Date();
    var dateString = "(@" + d.getHours() + ":" + d.getMinutes() + ")";
    output.innerHTML = "Updated " + count + " files. " + dateString;

}

function run() {
    var d = new Date();
    var dateString = "(@" + d.getHours() + ":" + d.getMinutes() + ")";
    if (apiKey && chosenDirectory) {
        output.innerHTML = "Updating... " + dateString;
        getJSON('https://www.livestreamalerts.com/recent_api_all?key='+apiKey, handleData);
    } else {
        output.innerHTML = "Not running. " + dateString;
    }
}


chooseDirButton.addEventListener('click', function(e) {
  chrome.fileSystem.chooseEntry({type: 'openDirectory'}, function(theDirectory) {
    if (!theDirectory) {
      return;
    }
    // use local storage to retain access to this file
    chrome.storage.local.set({'selectedDir': chrome.fileSystem.retainEntry(theDirectory)});
    chosenDirectory = theDirectory;
    chrome.fileSystem.getDisplayPath(chosenDirectory, function(path) {
      directoryBox.value = path;
      run();
    });
  });
});

updateKeyButton.addEventListener('click', function(e) {
  chrome.storage.local.set({'apiKey': apiKeyBox.value});
  apiKey = apiKeyBox.value;
  run();
});

function writeFile(dir, filename, contents) {
    // String conversion
    contents += '';
    contents = contents.replace(/\[\[br\]\]/g, "\n");
    dir.getFile(filename, {create: true}, function(fileDirectory) {
        var blob = new Blob([contents.replace(/\\n/g, "\r\n")], {type: 'text/plain'});
        fileDirectory.createWriter(function(writer) {
            writer.onwriteend = function() {
                if (writer.length != blob.size) {
                    writer.truncate(blob.size);
                    return;
                }
            };
            writer.write(blob);
        });
    }, function(error) {
        console.log(error);
    });
}

resetSessionButton.onclick=resetSession;

loadInitialFile(launchData);

