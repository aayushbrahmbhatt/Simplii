function showVal(newVal) {
    document.getElementById("valBox").innerHTML = newVal;
}

function show1Val(newVal) {
    document.getElementById("val1Box").innerHTML = newVal;
}

function show2Val(newVal) {
    document.getElementById("val2Box").innerHTML = newVal;
}

// Code to set up current time on deadline date field.
window.addEventListener('load', () => {
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    document.getElementById('deadline').value = now.toISOString().slice(0, -8);
});

// Show or hide the recurrence end date based on recurrence type
$(document).ready(function() {
    $('input[type="radio"]').click(function() {
        var inputValue = $(this).attr("value");
        $("div.desc").hide();
        $("#" + inputValue + "Split").show();
    });

    $('#recurrence').change(function() {
        if ($(this).val() === 'none') {
            $('#recurrenceEndDate').hide();
            $('#recurrenceEndDateLabel').hide();
        } else {
            $('#recurrenceEndDate').show();
            $('#recurrenceEndDateLabel').show();
        }
    });
});

function submitTask() {
    const formData = {
        title: document.getElementById("title").value,
        deadline: document.getElementById("deadline").value,
        recurrence: document.getElementById("recurrence").value,
        recurrenceEndDate: document.getElementById("recurrenceEndDate").value || null
    };

    let httpReq = new XMLHttpRequest();
    httpReq.open("POST", "/submit_task_details", false);
    httpReq.setRequestHeader("Content-Type", "application/json");
    httpReq.send(JSON.stringify(formData));

    if (httpReq.status === 200) {
        alert("Task submitted successfully!");
    } else {
        alert("Failed to submit task.");
    }
}
