document.getElementById('nextDayButton').addEventListener('click', function() {
    const datePicker = document.getElementById('datePicker');
    const currentDate = new Date(datePicker.value);
    currentDate.setDate(currentDate.getDate() + 1);
    datePicker.value = currentDate.toISOString().split('T')[0];
    datePicker.dispatchEvent(new Event('change'));
});

document.getElementById('datePicker').addEventListener('change', function() {
    window.location.href = '?task_date=' + this.value;
});

