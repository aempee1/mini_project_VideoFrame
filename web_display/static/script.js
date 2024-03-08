document.addEventListener('DOMContentLoaded', function() {
    function updateTimeAndDate() {
        var currentTimeElement = document.getElementById('current-time');
        var currentDateElement = document.getElementById('current-date');

        var now = new Date();

        // Update time
        var currentTime = now.toLocaleTimeString();
        currentTimeElement.innerText = ;

        // Update date
        var currentDate = now.toDateString();
        currentDateElement.innerText = currentDate;
    }

    // Update time and date every second
    setInterval(updateTimeAndDate, 1000);

    // Initial update
    updateTimeAndDate();
});
