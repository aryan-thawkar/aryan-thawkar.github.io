function sayHello() {
    console.log("Hello");
}

// Create a function that takes another function as an argument and calls it after 3 seconds (HOF + Callback).

function delayedCall(fn , i) {
    setTimeout(fn , (i * 1000));
}

delayedCall(sayHello, 10);








function limit(fn , limit){
    let calltimes = 0;
    return function(){
        if(calltimes < limit){
            calltimes++;
            fn();
        }
        else {
            console.log("Function call limit reached");
        }
    }
}



let fn = limit( sayHello, 3);
fn();
fn();
fn();
fn();