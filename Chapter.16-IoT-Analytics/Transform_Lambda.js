exports.handler = function handler(event) {
    
    console.log("event whole: ", event);
    console.log("event element: ", event[0]);
    
//add timestamp to data and name it "ServersideTimestamp"
        event[0].ServersideTimestamp = Date.now();
        console.log("event whole mod: ", event);
        
       return event;
};
