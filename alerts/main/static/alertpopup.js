/*
  Copyright 2016 Google Inc. All Rights Reserved.
  
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  
      http://www.apache.org/licenses/LICENSE-2.0
  
  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. 
*/  
var DEFAULT_ALERT_TIME = 5000;
var seen = {};
var seenUser = {};
var alertStack = [];
var firstLoad = true;
var alertActive = false;
var currentAlert = null;
var initialClear = false;
var allSubs = [];
var clearAlertTimeout;

// Helper Functions
function getQueryParams(qs) {
    qs = qs.split('+').join(' ');

    var params = {},
        tokens,
        re = /[?&]?([^=]+)=([^&]*)/g;

    while (tokens = re.exec(qs)) {
        params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
    }

    return params;
}

var params = getQueryParams(window.location.search);

function setVisible(element, visible) {
  if (visible) {
    $(element).removeClass('hidden');
  } else {
    $(element).addClass('hidden');
  }
}

function loadAlerts() {
  $.getJSON('/alert_api?key='+currentUser, null, handleAlerts ).fail(
    function(jqxhr, textStatus, error) {
      setTimeout(loadAlerts, 60000);
    });
}

function preload(alerts) {
   var fonts = [];
   for (var i = 0; i < alerts.length; i++) {
      var alert = alerts[i];
      if (alert.google_font) {
          fonts.push(alert.font);
      }
   }
   if (fonts) {
   WebFont.load({
       google: {
           families: fonts
       }
   });
   }
}

function handleAlerts(resp) {
  var alerts = resp.alerts;
  if (firstLoad) {
    preload(alerts);
  }
  var subs = [];
  for (var i = 0; i < alerts.length-1; i++) {
      var data = alerts[i];
      if (!seenUser[data['id']]) {
          subs.push(data);
          seenUser[data['id']] = true;
          if (!firstLoad) {
              alertStack.push(data);
          }
          allSubs.push(data['id']);
      }
  }
  firstLoad = false; 
  if (!alertActive && alertStack.length) {
      showAlert();
  }
  setTimeout(loadAlerts, DEFAULT_ALERT_TIME);
}

// Alert handling
function showAlert() {
  alertActive = true;
  currentAlert = alertStack.shift();
  
  // Fill in message text.
  var alertText = currentAlert['text'];
  var alertElem = document.getElementById('alertMessage');
  alertElem.innerHTML = '';
  var splitText = alertText.split("[[br]]");
  for (var i = 0; i < splitText.length; i++) {
    if (i != 0) {
        alertElem.appendChild(document.createElement("br"));
    }
    alertElem.appendChild(document.createTextNode(splitText[i]));
  }
  
  // Load and play sound.
  if (currentAlert.sound) {
      var sound = document.getElementById('sound');
      sound.src = currentAlert.sound;
      sound.play();
  }
  
  // Clear all layout tags and assign correct layout; default to vertical.
  $("#widget").removeClass("layoutSide layoutVertical layoutAbove");
  if (currentAlert['layout']) {
      var layoutName = currentAlert['layout'];
      layoutName = layoutName.charAt(0).toUpperCase() + layoutName.substr(1);
      $("#widget").addClass("layout"+layoutName);
  } else {
      $("#widget").addClass("layoutVertical");
  }    
 
  if (currentAlert['google_font']) {
      WebFont.load({
          google: {
              families: [currentAlert['font']]
          }
      });
  }

  // Assign text style properties.
  var styleProps = {'font': 'font-family', 'font_size': 'fontSize', 'font_color': 'color'};
  for (var key in styleProps) {
      var val = styleProps[key];
      if (currentAlert[key]) {
          $("#alertText").css(val, currentAlert[key]);
      }
  }
  $("#alertText").removeClass()
  var fontEffect = currentAlert['font_effect'] ? currentAlert['font_effect'] : 'shadow';
  $("#alertText").addClass("font-effect-" + fontEffect);
  
  // Manage alert animation.
  $("#alertBox").removeClass();
  setVisible(document.getElementById('widget'), true);
  var animation = currentAlert['animation_in'] ? currentAlert['animation_in'] : 'fadeIn';
  $("#alertBox").addClass("animated " + animation).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', function() {
      $("#alertBox").removeClass();
  });
  
  // Fill in image div.
  $("#imageContainer").css("backgroundImage", '');
  if (currentAlert.image) {
    $("#imageContainer").css("backgroundImage", "url('"+currentAlert.image+"')");
    restartAnimation(currentAlert.image, $("#imageContainer"));
  }


  // Set up timer.
  clearTimeout(clearAlertTimeout);
  initialClear = true;
  clearAlertTimeout = setTimeout(clearAlert, DEFAULT_ALERT_TIME);

}

function nextAlert() {
    setVisible(document.getElementById('widget'), false);
    if (alertStack.length) {
        showAlert();
    } else {
        alertActive = false;
    }
}

function clearAlert() {
  if (initialClear == true) {
      // When we first set our timeout, we haven't loaded the sound,
      // so we basically set an updated timer and bail early here. 
      initialClear = false;
      var soundLength = document.getElementById('sound').duration;
      soundLength = soundLength * 1000;
      if ((soundLength + 1000) > DEFAULT_ALERT_TIME) {
          length = soundLength - DEFAULT_ALERT_TIME;
          clearAlertTimeout = setTimeout(clearAlert, length);
          return;
      }
  }
  var animation = currentAlert['animation_out'] ? currentAlert['animation_out'] : 'fadeOut';
  $("#alertBox").addClass("animated " + animation).one('webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend', nextAlert);
  
}

if (params.key != undefined) {
  currentUser = params.key;
}
if (params.bgColor != undefined) {
    document.body.style.backgroundColor = params.bgColor;
}

resetHelperImages = {};
function restartAnimation(bgImg, elem) {
  elem = $(elem);
  var helper = resetHelperImages[bgImg];
  if (!helper) {
    helper = $('<img>').attr('src', bgImg).css({position: 'absolute', left: '-5000px'}).appendTo('body')[0];
    resetHelperImages[bgImg] = helper;
    setTimeout(function() {
      helper.src = bgImg;
    }, 10);
  } else {
    helper.src = bgImg;
  }
  elem.css("opacity", .99);
  setTimeout(function() {
    elem.css("opacity", 1);
  }, 20);
}
loadAlerts();

