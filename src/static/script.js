
var socket = io();

function helloWorld(name) {
  return `Hello, ${name}!`;
}


function displayCurrentTime() {
        const currentTimeElement = document.getElementById('currentTime');
        const currentTime = moment().unix();
        currentTimeElement.textContent = `Current time: ${currentTime} seconds`;   
}


function readFromPy() {
    
    console.log("readFromPy")

    const currentTimePyElement = document.getElementById('currentTimePy');

    socket.on('emitFromPy', function(data) {
        console.log(JSON.stringify(data))
        currentTimePyElement.textContent = `${JSON.stringify(data)}`;
    });
   
}



function btnTest() {

    console.log("btnTest")

    // Get the button element
    const btnOne = document.getElementById('btnOne');

    // Add an event listener to the button
    btnOne.addEventListener('click', function() {
    // Call the function to log a message to the console
        console.log('Button clicked!');
    });
}

function btnTest2() {
    //var socket = io();


    console.log("btnTestEmit")

    // Get the button element
    const btnTwo = document.getElementById('btnTwo');

    // Add an event listener to the button
    btnTwo.addEventListener('click', function() {
    // Call the function to log a message to the console
        console.log('Button clicked!');
        const currentTime = moment().unix();
        socket.emit('my_event', {'time in js': currentTime});
    });
}
    

function btnPPressed() {

    let isPPressed = false;

    console.log("btnPressed")
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


});


}


function readTranscription() {

    console.log("readTranscription")
    const currentTranscription = document.getElementById('currentTranscription');
        socket.on('readTrans', function(data) {
        console.log(JSON.stringify(data))
        

        const transcriptionStr = data["transcription"]

        currentTranscription.textContent = transcriptionStr
    });
}


