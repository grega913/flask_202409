
var socket = io();

document.addEventListener("DOMContentLoaded", function() {
    const sendButton = document.querySelector(".send-button");
    //const messageInput = document.querySelector("#message-input");

    const messageInput= document.getElementById('message-input');

    const messageList = document.querySelector("#message-list");

    function sendMessage() {
        
        const userMessageText = messageInput.value.trim();
        if (userMessageText !== "") {
            // Add user message
            const userMessage = document.createElement("li");
            userMessage.className = "message_user";
            userMessage.textContent = userMessageText;
            messageList.appendChild(userMessage);

            console.log("we should call api here")

            // Mimic AI response with delay
            /*
                        setTimeout(function() {
                const aiMessage = document.createElement("li");
                aiMessage.className = "message_ai";
                aiMessage.textContent = "this is ai generated message: " + userMessageText;
                messageList.appendChild(aiMessage);
            }, 500);
           */

            


            // request to our api, where heavy handling is made and wait for response
            axios.post('/api/datapoint3', {user_input: userMessageText})
                .then(response => {
                    // Do something with the response data
                    console.log(response.data);

                    // Create a new list item (li) element
                    const newAiMessageElement = document.createElement('li');
                    newAiMessageElement.className = 'message_ai';
                    newAiMessageElement.textContent = response.data; // Set the text content to response data

                    // Append the new list item to the existing list
                    messageList.appendChild(newAiMessageElement);
                })
                .catch(error => {
                    console.error(error);
            });

              // Clear input
            messageInput.value = "";






        }
    }

    sendButton.addEventListener("click", sendMessage);

    messageInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

});




function btnPressed() {

    console.log("btnPressed")

    let isPPressed = false;

        // Create the pPressedElement here
    const pPressedElement = document.createElement('div');
    pPressedElement.className = 'p-pressed';
    document.body.appendChild(pPressedElement);


    document.addEventListener('keydown', (event) => {
        if (event.key === 'p' || event.key==="Pause") {
           if (!isPPressed) {
                console.log("p down")
                isPPressed = true;
                socket.emit("pDown", { event });
                document.querySelector('.p-pressed').style.display = 'block';
            }
        }
    });


    document.addEventListener('keyup', (event) => {
    if (event.key === 'p' || event.key==="Pause") {
       if (isPPressed) {
                console.log("p up")
                isPPressed = false;
                socket.emit("pUp", { event });
                document.querySelector('.p-pressed').style.display = 'none';
            }
        }
    })


}


function helloWorld(name) {
  return `Hello, ${name}!`;
}


function readTranscription() {

    console.log("readTranscription")
    const currentTranscription = document.getElementById('currentTranscription');
    const messageInput= document.getElementById('message-input');

    socket.on('readTrans', function(data) {
        console.log(JSON.stringify(data))

        const transcriptionStr = data["transcription"]
        messageInput.value = transcriptionStr
    });
}