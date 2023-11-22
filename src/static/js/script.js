function addToLocalStorage(key,data){
    localStorage.setItem(key) = data;
}

function retrieveFromLocalStorage(key){
    return localStorage.getItem(key)
}

function logout(){
    $.ajax({
        type: "POST",
        url: "/logout",
        success: function(data) {
            console.log(data)
            window.location.href = "login";
        }
    });
}

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','.deleteButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/deleteTask",
            data:{
                "task":col1,
                "status":col2,
                "category":col3
            },
            success: function(response){
                var url = "/dashboard"
                window.location.href = url;
            }
        })
        
    });
});

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','.reminderButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/editTask",
            data:{
                "task":col1,
                "status":col2,
                "category":col3
            },success: function(response){
                resdata = JSON.parse(response)
                var url = "/schedule_reminder?taskname=" + resdata.taskname + "&category=" + resdata.category + "&startdate=" + resdata.startdate + "&duedate="+resdata.duedate+"&status="+resdata.status+"&hours="+resdata.hours;
                window.location.href = url;
            }
        })
        
    });
});

$(document).ready(function(){

    // code to read selected table row cell data (values).
    $("#myTable").on('click','.editButton',function(){
        // get the current row
        var currentRow=$(this).closest("tr"); 
            
        var col1=currentRow.find("td:eq(0)").text(); // get current row 1st TD value
        var col2=currentRow.find("td:eq(1)").text(); // get current row 2nd TD
        var col3=currentRow.find("td:eq(2)").text(); // get current row 3rd TD
        console.log(col1);
        $.ajax({
            type: "POST",
            url: "/editTask",
            data:{
                "task":col1,
                "status":col2,
                "category":col3
            },
            success: function(response){
                resdata = JSON.parse(response)
                var url = "/updateTask?taskname=" + resdata.taskname + "&category=" + resdata.category + "&startdate=" + resdata.startdate + "&duedate="+resdata.duedate+"&status="+resdata.status+"&hours="+resdata.hours;
                window.location.href = url;
            }
        })
        
    });
});

$(document).ready(function(){
    // Initialize Sortable.js for each task list
    new Sortable(document.getElementById('todo-tasks'), {
        group: 'task-list',
        onEnd: function (evt) {
            updateTaskStatus(evt);
        }
    });

    new Sortable(document.getElementById('in-progress-tasks'), {
        group: 'task-list',
        onEnd: function (evt) {
            updateTaskStatus(evt);
        }
    });

    new Sortable(document.getElementById('done-tasks'), {
        group: 'task-list',
        onEnd: function (evt) {
            updateTaskStatus(evt);
        }
    });

    // Function to update task status in the database after drag-and-drop
    function updateTaskStatus(evt) {
        var taskId = evt.item.getAttribute('data-task-id');
        var newListId = evt.to.id;
        console.log(taskId, newListId);
        // Send AJAX request to update task status in the database
        $.ajax({
            url: '/update_task_status',
            type: 'POST',
            data: { task_id: taskId, new_status: newListId },
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error(error);
            }
        });
    }
});
