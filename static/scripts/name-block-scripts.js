// Email verification function
function validateEmail(email) {
  const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}

// Show preference modal
function showPrefModal() {
  const modal = document.getElementById("prefModal");
  const btn = document.getElementById("prefBtn");
  const span = document.getElementsByClassName("close")[0];

  btn.onclick = function() {
    modal.style.display = "block";
  };

  span.onclick = function() {
    modal.style.display = "none";
  };

  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  };
}

function closeModal() {
  const modal = document.getElementById("prefModal");
  modal.style.display = "none";
}

// Save data and close modal
function saveAndCloseModal() {
  const modal = document.getElementById("prefModal");
  modal.style.display = "none";
  // Collect and submit form data here if needed
}

// Submit user info (Updated)
async function submitUserInfo(formData) {
  try {
    const response = await fetch("/submit_user_details", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formData)
    });
    if (response.ok) {
      alert("User info submitted successfully!");
    } else {
      alert("Failed to submit user info.");
    }
  } catch (error) {
    console.error("Error submitting user info:", error);
    alert("An error occurred while submitting user info.");
  }
}

// Update preferences (Uncommented and updated)
async function change_pref(data) {
  const new_preferences = {
    initialized: "yes",
    name: "",
    email_id: "",
    email_notifications: ""
  };

  // Prompt for name until a valid input is given
  let new_name = "";
  while (!new_name) {
    new_name = prompt("Please enter your name (required)", data.name_block.name || "");
  }
  new_preferences.name = new_name;

  // Prompt for email and validate
  let new_email_id = "";
  while (!validateEmail(new_email_id) && new_email_id !== "") {
    new_email_id = prompt("Please enter your e-mail (leave empty if you do not wish to share)", data.name_block.email_id || "");
    if (new_email_id === "") break;
  }
  new_preferences.email_id = new_email_id;

  // Ask for email notifications preference if email is provided
  if (new_email_id) {
    const new_email_notifications = prompt("Do you want critical email notifications for your tasks? (yes/no)", data.name_block.email_notifications || "no");
    new_preferences.email_notifications = new_email_notifications.toLowerCase() === "yes" ? "yes" : "no";
  } else {
    new_preferences.email_notifications = "no";
  }

  // Send updated preferences to the server
  try {
    const response = await fetch("/update_user_info", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(new_preferences)
    });
    if (response.ok) {
      alert("Preferences updated successfully!");
    } else {
      alert("Failed to update preferences.");
    }
  } catch (error) {
    console.error("Error updating preferences:", error);
    alert("An error occurred while updating preferences.");
  }
}

// Forced initialization to set preferences if not yet done
function force_initialization(data) {
  if (data.name_block.initialized !== "yes") {
    alert("Welcome to Simpli! Please enter some information to get started.");
    change_pref(data);
  }
}
