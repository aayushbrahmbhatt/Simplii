
# Export to CSV Functionality

This document explains the implementation of the **Export to CSV** feature in your application. It includes the design and functionality of the "Export to CSV" button, JavaScript code that enables data export, and how it is integrated into the `dashboard.html` template.

---

## Table of Contents

1. [Introduction](#introduction)
2. [File Breakdown](#file-breakdown)
    - [dashboard.html](#dashboardhtml)
3. [Export to CSV Button Design](#export-to-csv-button-design)
4. [JavaScript Code for CSV Export](#javascript-code-for-csv-export)
5. [Steps to Use the Export Feature](#steps-to-use-the-export-feature)
6. [Conclusion](#conclusion)

---

## Introduction

The **Export to CSV** feature allows users to export visible tasks into a CSV file. This functionality ensures users can easily download and share their task data in a widely compatible format. The exported file includes the following task attributes:
- Task Name
- Status
- Category
- Start Date
- Due Date

---

## File Breakdown

### dashboard.html

The **dashboard.html** template includes the Export to CSV button, task table, and JavaScript code required for the export functionality. Below are the key components:

1. **Export Button**  
   The Export to CSV button is designed using Bootstrap and Font Awesome:
   ```html
   <button id="exportCSV" class="btn btn-primary me-2">
       <i class="fas fa-download"></i> Export to CSV
   </button>
   ```

2. **Task Table**  
   The task table displays task details in a structured format. Only visible rows are exported to the CSV file. Example structure:
   ```html
   <table id="myTable" class="table table-striped table-hover">
       <thead>
           <tr>
               <th>Task</th>
               <th>Status</th>
               <th>Category</th>
               <th>Start Date</th>
               <th>Due Date</th>
               <th>Actions</th>
           </tr>
       </thead>
       <tbody>
           <!-- Rows dynamically generated -->
           <tr>
               <td>Example Task</td>
               <td>To-Do</td>
               <td>Physical</td>
               <td>2024-11-01</td>
               <td>2024-11-10</td>
               <td>
                   <!-- Action buttons -->
               </td>
           </tr>
       </tbody>
   </table>
   ```

---

## Export to CSV Button Design

The button is styled using Bootstrap classes:
- `btn btn-primary`: Provides the primary color scheme.
- Font Awesome icon (`fas fa-download`): Displays a download icon alongside the button label.

Code snippet:
```html
<button id="exportCSV" class="btn btn-primary me-2">
    <i class="fas fa-download"></i> Export to CSV
</button>
```

The button is placed within a button group for alignment with other actions (e.g., Send Schedule).

---

## JavaScript Code for CSV Export

The JavaScript code implements the functionality for exporting tasks to a CSV file.

### Steps in the Script:

1. **Collect Table Headers**  
   The script extracts column headers from the task table:
   ```javascript
   $('#myTable thead th').slice(0, -1).each(function() {
       headers.push($(this).text().trim());
   });
   rows.push(headers.join(','));
   ```

2. **Collect Visible Row Data**  
   Only visible rows are included in the export. Data is sanitized for special characters (e.g., commas):
   ```javascript
   $('#myTable tbody tr:visible').each(function() {
       const rowData = [];
       $(this).find('td').slice(0, -1).each(function() {
           let data = $(this).text().trim();
           data = data.replace(/"/g, '""'); // Escape double quotes
           if (data.includes(',')) {
               data = `"${data}"`; // Add quotes for commas
           }
           rowData.push(data);
       });
       rows.push(rowData.join(','));
   });
   ```

3. **Generate CSV File**  
   A Blob object is created, and the CSV file is made available for download:
   ```javascript
   const csvContent = rows.join('\n');
   const blob = new Blob([csvContent], { type: 'text/csv' });
   const url = window.URL.createObjectURL(blob);
   const a = document.createElement('a');
   a.href = url;
   a.download = 'tasks.csv';
   document.body.appendChild(a);
   a.click();
   document.body.removeChild(a);
   window.URL.revokeObjectURL(url);
   ```

### Complete JavaScript Code:
```javascript
$('#exportCSV').click(function() {
    const rows = [];
    const headers = [];
    
    // Get headers (excluding Actions column)
    $('#myTable thead th').slice(0, -1).each(function() {
        headers.push($(this).text().trim());
    });
    rows.push(headers.join(','));

    // Get visible row data
    $('#myTable tbody tr:visible').each(function() {
        const rowData = [];
        $(this).find('td').slice(0, -1).each(function() {
            let data = $(this).text().trim();
            data = data.replace(/"/g, '""'); // Escape quotes
            if (data.includes(',')) {
                data = `"${data}"`; // Wrap with quotes if needed
            }
            rowData.push(data);
        });
        rows.push(rowData.join(','));
    });

    // Create and trigger download
    const csvContent = rows.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'tasks.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
});
```

---

## Steps to Use the Export Feature

1. Navigate to the dashboard page where tasks are displayed in a table.
2. Apply filters if needed to limit the visible rows in the table.
3. Click the **Export to CSV** button.
4. The browser will download a file named `tasks.csv` containing the visible task data.

---

## Conclusion

The Export to CSV functionality enhances productivity by allowing users to download task data in a structured format. The implementation is simple yet flexible, enabling compatibility with various applications that support CSV files. The integration within the dashboard ensures seamless user interaction.

![image](https://github.com/user-attachments/assets/dbab7bc2-6281-428c-8cb3-33e21c215d5f)



# How to Export Tasks to CSV?

* Open the "All Tasks" dashboard page in the application.

* Review the tasks displayed in the table. Use the filtering options (status, category, display limit) to narrow down the tasks you want to export.

* Click the Export to CSV button located in the top-right corner of the task table.

* The system will generate a CSV file containing the visible tasks and prompt you to save or download it.

* Save the file to your desired location on your computer.

Example interaction:

* User Action: Clicks on the "Export to CSV" button after applying filters.

* Result: A file named tasks.csv is downloaded, containing the selected tasks' data.


---
