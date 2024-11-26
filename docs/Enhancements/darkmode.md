
# Dark Mode Theme Implementation

This document explains the implementation of the Dark Mode Theme feature in your application. It includes the setup of a dynamic theme toggle button, the use of `main.css` for light mode, `maindark.css` for dark mode, and details about how the theme persists across page refreshes. The following sections provide a detailed breakdown.

---

## Table of Contents
1. [Introduction](#introduction)
2. [File Breakdown](#file-breakdown)
    - [layout.html](#layouthtml)
    - [main.css and maindark.css](#maincss-and-maindarkcss)
3. [Theme Toggle Button](#theme-toggle-button)
4. [JavaScript for Theme Switching](#javascript-for-theme-switching)
5. [Theme Persistence After Refresh](#theme-persistence-after-refresh)
6. [Applying Themes Across the Application](#applying-themes-across-the-application)
7. [Conclusion](#conclusion)

---

## Introduction

The Dark Mode feature allows users to switch between light and dark themes seamlessly. It is applied across the entire application using a combination of Bootstrap, Font Awesome icons, CSS stylesheets, and JavaScript. The theme preference persists even after the user refreshes the page, providing a consistent user experience.

---

## File Breakdown

### layout.html

The `layout.html` file contains the foundational HTML structure for the dynamic theme toggle functionality. The following key components are included:

1. **Bootstrap and Font Awesome Links**  
   These libraries provide styling and icons for the application:
   ```html
   <!-- Bootstrap CSS -->
   <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

   <!-- Font Awesome for Icons -->
   <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" rel="stylesheet">
   ```

2. **Dynamic Theme CSS**  
   This link dynamically switches between `main.css` (light theme) and `maindark.css` (dark theme) based on the user’s preference:
   ```html
   <link id="themeStyle" rel="stylesheet" type="text/css" href="{{ url_for('static', filename='main.css') }}">
   ```

3. **Theme Toggle Button**  
   The button to toggle themes is fixed at the bottom-right corner of the page:
   ```html
   <div class="theme-toggle" style="position: fixed; bottom: 20px; right: 20px;">
       <button id="themeToggleButton" class="btn btn-primary">
           <i id="themeIcon" class="fas fa-sun"></i> 
       </button>
   </div>
   ```

### main.css and maindark.css

1. **main.css**  
   Contains styles for the **light theme**, such as light background colors and dark text. Example:
   ```css
   body {
       background-color: #ffffff;
       color: #000000;
   }
   ```

2. **maindark.css**  
   Contains styles for the **dark theme**, such as dark backgrounds and light text. Example:
   ```css
   body {
       background-color: #121212;
       color: #ffffff;
   }
   ```

Both stylesheets are stored in the `static` directory.

---

## Theme Toggle Button

The theme toggle button is implemented in `layout.html` as a floating button styled with Bootstrap and Font Awesome. 

- The button uses a **Font Awesome icon** to represent the current theme (`fa-sun` for light and `fa-moon` for dark).  
- It is designed to be always visible to the user, placed at a fixed position on the screen.

---

## JavaScript for Theme Switching

The logic for toggling themes is implemented using JavaScript. Below are the key features:

1. **Toggle Function**  
   The `toggleTheme` function switches between light and dark themes:
   ```javascript
   function toggleTheme() {
       let currentTheme = localStorage.getItem('theme');
       if (currentTheme === 'dark') {
           document.getElementById('themeStyle').href = "{{ url_for('static', filename='main.css') }}";
           themeIcon.classList.replace('fa-moon', 'fa-sun');
           localStorage.setItem('theme', 'light');
       } else {
           document.getElementById('themeStyle').href = "{{ url_for('static', filename='maindark.css') }}";
           themeIcon.classList.replace('fa-sun', 'fa-moon');
           localStorage.setItem('theme', 'dark');
       }
   }
   ```

2. **Load Theme on Page Load**  
   The saved theme is loaded from `localStorage` and applied when the page loads:
   ```javascript
   window.onload = function () {
       const savedTheme = localStorage.getItem('theme');
       if (savedTheme === 'dark') {
           document.getElementById('themeStyle').href = "{{ url_for('static', filename='maindark.css') }}";
           themeIcon.classList.replace('fa-sun', 'fa-moon');
       } else {
           document.getElementById('themeStyle').href = "{{ url_for('static', filename='main.css') }}";
           themeIcon.classList.replace('fa-moon', 'fa-sun');
       }
   };
   ```

3. **Event Listener**  
   The button listens for user clicks to toggle the theme:
   ```javascript
   themeToggleButton.addEventListener('click', toggleTheme);
   ```

---

## Theme Persistence After Refresh

To ensure the theme persists after a page refresh:
- The theme preference is **saved in `localStorage`** using the `setItem` method.
- On page load, the saved theme is **retrieved from `localStorage`** using the `getItem` method and applied to the `href` attribute of the theme stylesheet.

Example:
```javascript
localStorage.setItem('theme', 'dark');
const savedTheme = localStorage.getItem('theme');
```

This guarantees that the user’s theme choice is maintained across sessions.

---

## Applying Themes Across the Application

Since the theme is dynamically loaded via the `<link>` tag in `layout.html`, it automatically applies to all pages inheriting from the layout template. 

- Any page that extends `layout.html` will reflect the selected theme.
- The theme toggle button is accessible from every page in the application.

---

## Conclusion

The Dark Mode Theme implementation enhances the user experience by allowing theme customization and ensuring theme persistence. The combination of HTML, CSS, and JavaScript makes this feature robust and scalable.

Feel free to modify the styles in `main.css` and `maindark.css` to suit your application's design requirements.

Light Theme Application
![image](https://github.com/user-attachments/assets/95ee34e2-ae62-4074-8be5-3b61c9f6d045)

Dark Theme Application
![image](https://github.com/user-attachments/assets/d5a84f30-4282-42fc-b7c4-9b69b12e27ad)


# How to Enable Dark Mode?
* Launch the application in your web browser (follow the instructions in the main README.md to set up and run the project).

* Locate the dark mode toggle button, typically represented by a moon/sun icon or a switch at the top-right corner of the interface.

* Click on the toggle button to switch between light mode and dark mode.

* The theme will change immediately, and your preference may be saved for future sessions (depending on implementation).

Example interaction:

* User Action: Clicks on the dark mode toggle.
* Result: The UI updates to a dark-themed color palette for better visibility in low-light conditions.


---
