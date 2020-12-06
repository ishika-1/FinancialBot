//---------------------------------- Main Code Area ----------------------------------//
//  Variables to be used for storing the last message sent and recieved for the database
var lastSentMessage = "";
var lastRecievedMessage = 1;
var ButtonClicked = false;


var DEFAULT_TIME_DELAY = 3000;

// Variable for the chatlogs div
var $chatlogs = $('.chatlogs');


$('document').ready(function(){

	// Hide the switch input type button initially
	$("#switchInputType").toggle();

	// If the switch input type button is pressed
	$("#switchInputType").click(function(event) {


		$('textarea').toggle();
		$('.buttonResponse').toggle();

	});

	//----------------------User Sends Message Methods--------------------------------//
	// Method which executes once the enter key on the keyboard is pressed
	$("textarea").keypress(function(event) {

		// If the enter key is pressed
		if(event.which === 13) {

			// Ignore the default function of the enter key(Dont go to a new line)
			event.preventDefault();

			ButtonClicked = false;

			// Call the method for sending a message, pass in the text from the user
			send(this.value);

			// reset the size of the text area
			$(".input").attr("rows", "1");

			// Clear the text area
			this.value = "";

			if($("#switchInputType").is(":visible")) {
				$("#switchInputType").toggle();
				$('.buttonResponse').remove();
			}

		}
	});


	// If the user presses the button for voice input
	$("#rec").click(function(event) {

		// Call the method to switch recognition to voice input
		switchRecognition();
	});


	// If the user selects one of the dynamic button responses
	$('.chat-form').on("click", '.buttonResponse', function() {

		ButtonClicked = true;

		// Send the text on the button as a user message
		send(this.innerText);

		// Show the record button and text input area
		//$('#rec').toggle();
		$('textarea').toggle();

		// Hide the button responses and the switch input button
		$('.buttonResponse').toggle();
		$('#switchInputType').hide();

		// Remove the button responses from the div
		$('.buttonResponse').remove();

	});

})


// Method which takes the users text and sends an AJAX post request to API.AI
// Creates a new Div with the users text, and recieves a response message from API.AI
function send(text) {

	// Create a div with the text that the user typed in
	$chatlogs.append(
        $('<div/>', {'class': 'chat self'}).append(
            $('<p/>', {'class': 'chat-message', 'text': text})));

	// Find the last message in the chatlogs
	var $sentMessage = $(".chatlogs .chat").last();
	console.log("Last Message")
	console.log( $sentMessage)

	// Check to see if that message is visible
	checkVisibility($sentMessage);

	// update the last message sent variable to be stored in the database and store in database
	lastSentMessage = text;

	// AJAX post request, sends the users text to API.AI and
	// calls the method newReceivedMessage with the response from API.AI
	$.ajax({
		success: function(data) {
			var message= lastSentMessage
			var str
			var url_django = '/save_message?message='+message;
			var xhttp = new XMLHttpRequest();
				xhttp.onreadystatechange = function() {

					if (this.readyState == 4 && this.status == 200) {

						str= xhttp.responseText

						console.log(str)
						newRecievedMessage(str);

						console.log("successful")
					}
				};
				xhttp.open("GET", url_django, true);
				xhttp.send();
		},
		error: function() {
			newRecievedMessage("Internal Server Error");
		}
	});
}


//----------------------User Receives Message Methods--------------------------------//


// Method called whenver there is a new recieved message
// This message comes from the AJAX request sent to API.AI
// This method tells which type of message is to be sent
// Splits between the button messages, multi messages and single message
function newRecievedMessage(messageText) {
	console.log(messageText)

	// Variable storing the message with the "" removed
	var removedQuotes = messageText.replace(/[""]/g,"");

	// update the last message recieved variable for storage in the database
	lastRecievedMessage = removedQuotes;

	// Show the typing indicator
	showLoading();

	// After 3 seconds call the createNewMessage function
	setTimeout(function() {createNewMessage(removedQuotes);}, DEFAULT_TIME_DELAY);
}


// Method to create a new div showing the text from API.AI
function createNewMessage(message) {

	// Hide the typing indicator
	hideLoading();

	// take the message and say it back to the user.
	// speechResponse(message);
	// Append a new div to the chatlogs body, with an image and the text from API.AI
	$chatlogs.append(
		$('<div/>', {'class': 'chat friend'}).append($('<p/>', {'class': 'chat-message', 'text': message}))
	);

	// Find the last message in the chatlogs
	var $newMessage = $(".chatlogs .chat").last();

	// Call the method to see if the message is visible
	checkVisibility($newMessage);
}




//------------------------------------------- Database Write --------------------------------------------------//

// Funtion which shows the typing indicator
// As well as hides the textarea and send button
function showLoading() {

	$chatlogs.append($('#loadingGif'));
	$("#loadingGif").show();
	$('.chat-form').css('visibility', 'hidden');
}



// Function which hides the typing indicator
function hideLoading() {

	$('.chat-form').css('visibility', 'visible');
	$("#loadingGif").hide();

	// Clear the text area of text
	$(".input").val("");

	// reset the size of the text area
	$(".input").attr("rows", "1");
}



// Method which checks to see if a message is in visible
function checkVisibility(message) {

	// Scroll the view down a certain amount
	$chatlogs.stop().animate({scrollTop: $chatlogs[0].scrollHeight});
}





//----------------------Voice Message Methods--------------------------------//
var recognition;

function startRecognition() {

	console.log("Start")
	recognition = new webkitSpeechRecognition();

	recognition.onstart = function(event) {

	console.log("Update");
		updateRec();
	};

	recognition.onresult = function(event) {

		var text = "";

		for (var i = event.resultIndex; i < event.results.length; ++i) {
			text += event.results[i][0].transcript;
		}

		setInput(text);
		stopRecognition();

	};

	recognition.onend = function() {
		stopRecognition();
	};

	recognition.lang = "en-US";
	recognition.start();

}

function stopRecognition() {
	if (recognition) {
        console.log("Stop Recog");
		recognition.stop();
		recognition = null;
	}
	updateRec();
}

function switchRecognition() {
	if (recognition) {
		console.log(" Stop if");
		stopRecognition();
	} else {
		startRecognition();
	}
}

function setInput(text) {
	$(".input").val(text);
	send(text);
	console.log(text)
    $(".input").val("");
}

function updateRec() {
	console.log("Update Recognition")
}

function speechResponse(message) {

	var msg = new SpeechSynthesisUtterance();
	msg.default = false;
	msg.voiceURI = "Fiona";
	msg.name = "Fiona";
	msg.localService = true;
	msg.text = message;
	msg.lang = "en";
	msg.rate = .9;
	msg.volume = 1;
	window.speechSynthesis.speak(msg);
}

//----------------------------------------- Resize the textarea ------------------------------------------//
$(document)
	.one('focus.input', 'textarea.input', function(){
		var savedValue = this.value;
		this.value = '';
		this.baseScrollHeight = this.scrollHeight;
		this.value = savedValue;
	})
	.on('input.input', 'textarea.input', function(){
		var minRows = this.getAttribute('data-min-rows')|0, rows;
		this.rows = minRows;
		rows = Math.ceil((this.scrollHeight - this.baseScrollHeight) / 17);
		this.rows = minRows + rows;
	});
