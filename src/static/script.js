


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
    






function readResponse() {
    console.log("readResponse")
    const curRespo = document.getElementById('curRespo');

        socket.on('readRespo', function(data) {
        
        console.log(JSON.stringify(data))
        
        const response = data["response"]

        curRespo.textContent = response
    }); 
}