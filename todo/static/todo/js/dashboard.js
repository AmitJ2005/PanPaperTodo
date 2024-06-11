document.addEventListener('DOMContentLoaded', function() {
    var datePicker = document.getElementById('datePicker');
    var nextDayButton = document.getElementById('nextDayButton');
    var prevDayButton = document.getElementById('prevDayButton');
    
    function updateUrl(date) {
        var formattedDate = formatDate(date);
        var url = new URL(window.location.href);
        url.searchParams.set('task_date', formattedDate);
        window.location.href = url.toString();
    }

    function formatDate(date) {
        var year = date.getFullYear();
        var month = (date.getMonth() + 1).toString().padStart(2, '0'); // Months are zero indexed
        var day = date.getDate().toString().padStart(2, '0');
        return year + '-' + month + '-' + day;
    }

    nextDayButton.addEventListener('click', function() {
        var selectedDate = new Date(datePicker.value);
        if (isNaN(selectedDate.getTime())) {
            selectedDate = new Date(); // Fallback to current date if selected date is invalid
        }
        selectedDate.setDate(selectedDate.getDate() + 1); // Increment date by 1 day
        updateUrl(selectedDate);
    });

    prevDayButton.addEventListener('click', function() {
        var selectedDate = new Date(datePicker.value);
        if (isNaN(selectedDate.getTime())) {
            selectedDate = new Date(); // Fallback to current date if selected date is invalid
        }
        selectedDate.setDate(selectedDate.getDate() - 1); // Decrement date by 1 day
        updateUrl(selectedDate);
    });

    datePicker.addEventListener('change', function() {
        var selectedDate = new Date(this.value);
        if (isNaN(selectedDate.getTime())) {
            selectedDate = new Date(); // Fallback to current date if selected date is invalid
        }
        updateUrl(selectedDate);
    });

    var urlParams = new URLSearchParams(window.location.search);
    var taskDate = urlParams.get('task_date');
    if (taskDate) {
        datePicker.value = taskDate;
    }
});

document.getElementById('datePicker').addEventListener('change', function() {
    window.location.href = '?task_date=' + this.value;
});

function toggleTaskInput() {
    var taskInputContainer = document.getElementById("taskInputContainer");
    var taskInput = document.getElementById("taskTitle");

    if (taskInputContainer.style.display === "none") {
        taskInputContainer.style.display = "block";
        taskInput.focus();  // Set focus to the input field
    } else {
        taskInputContainer.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const profileInfo = document.querySelector('.profile-info');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    profileInfo.addEventListener('click', function () {
        dropdownMenu.classList.toggle('show');
    });

    window.addEventListener('click', function (event) {
        if (!profileInfo.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});
