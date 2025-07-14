function sayHello() {
    console.log("Hello");
}

// Create a function that takes another function as an argument and calls it after 3 seconds (HOF + Callback).

function delayedCall(fn , i) {
    setTimeout(fn , (i * 1000));
}

delayedCall(sayHello, 3);


// Implement your own version of `.map()` as a higher-order function.

array = [1, 2, 3, 4, 5];
function cube(x) {
    return x * x * x;
}

function myMap(arr , fn) {
    let result = [];
    for(let i = 0; i < arr.length; i++) {
        result.push(fn(arr[i], i, arr));
    }
    return result;
}

let a = myMap(array , cube);
console.log(a);


// Write a function that uses closures to create a counter.

function createCounter() {
    let count = 0;
    return function() {
        count++;
        console.log(count);
    }
}

let b = createCounter();
b();
b();
b();
b();




// Create a function that limits the number of times a function can be called.

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