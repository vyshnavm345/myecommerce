// countdown.js
document.addEventListener("DOMContentLoaded", function () {
    let countdown = document.getElementById("countdown");
    let remainingTime = localStorage.getItem("remainingTime"); // Try to retrieve remaining time from localStorage
  
    if (remainingTime) {
      // If remaining time is available, parse it and start countdown from there
      remainingTime = parseInt(remainingTime);
      startCountdown(remainingTime);
    } else {
      // If no remaining time is available, start countdown from 60 seconds
      startCountdown(60);
    }
  
    function startCountdown(seconds) {
      let timer = setInterval(function () {
        countdown.textContent = seconds + " seconds";
        seconds--;
  
        // Store the remaining time in localStorage
        localStorage.setItem("remainingTime", seconds);
  
        if (seconds < 0) {
          clearInterval(timer);
          countdown.textContent = "Time's up!";
          localStorage.removeItem("remainingTime"); // Remove the remaining time when the countdown is finished
        }
      }, 1000);
    }
  });
  With    
   
   