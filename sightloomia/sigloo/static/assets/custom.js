//document.addEventListener("DOMContentLoaded", function() {
    // Get the current path, ignoring any trailing slash
//    const currentPath = window.location.pathname.replace(/\/$/, "");
//    console.log("Current Path:", currentPath); // Debugging line

    // Select all navigation links in the menu
//    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

//    navLinks.forEach(link => {
        // Get the link's href path, ignoring any trailing slash
//        const linkPath = new URL(link.href).pathname.replace(/\/$/, "");
//        console.log("Link Path:", linkPath); // Debugging line

        // Check if the link's path matches the current path
//        if (linkPath === currentPath) {
//            console.log("Active link found:", link); // Debugging line

            // Remove 'active' from any previously active link to ensure only one is highlighted
//            navLinks.forEach(navLink => navLink.classList.remove("active"));

            // Add 'active' to the matching link
//            link.classList.add("active");
//        }
//    });
//});



// SECTION 1: GLOBALLY ACCESSIBLE FUNCTIONS (These functions need to be explicitly called within other JavaScript code or by HTML elements. )

// Function, can be used directly as: document.getElementById('save-button').addEventListener('click', SaveItem);
function SaveItem() {
    return alert('Do you want save it?'); 
}

// Function
function CloseItem(el) {
    alert('Do you want close it?');
    console.log(el.id);
    console.log(sessionStorage);
    console.log('1: ', sessionStorage.getItem("to_remove"));
    sessionStorage.setItem("to-remove", el.id);
    console.log('2: ', sessionStorage.getItem("to-remove"));  
    return el.id;
}

// F1: Mutation Observer to watch for changes in the element style
// F2: Listener for clicks on for "remove-" buttons to remove loaded inputs and release memory
function observeStyleChanges() {
    console.log("observeStyleChanges() called");

    var buttons = document.querySelectorAll('.dt-buttons');
    var observerCallback = function(mutationsList) {
        for (var mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                var targetElement = mutation.target;
                if (targetElement.style.display === 'none') {
                    window.dash_clientside.clientside.moveDataTableButtons();
                }
            }
        }
    };
    var observerOptions = { attributes: true, attributeFilter: ['style'] };

    buttons.forEach(function(button) {
        var observer = new MutationObserver(observerCallback);
        observer.observe(button, observerOptions);
    });

    // 2) Function to handle 'remove-' button clicks
    function handleButtonClick(event) {
        const button = event.target;
        const buttonId = button.id;
        console.log('Button clicked:', buttonId);                                     // DEBUG

        // Find the parent div with an ID starting with "file-"
        const parentDiv = button.closest('div[id^="file-"]');
        if (parentDiv) {
            // Remove the parent div from the DOM
            parentDiv.remove();

            // Extract and return the part of the parent ID after "file-"
            const fileIdPart = parentDiv.id.substring('file-'.length);
            console.log('Removed file ID:', fileIdPart);
            return fileIdPart;
        } else {
            console.log('No parent div found for button:', buttonId);
        }
        return '';
    }

    let captured_name = '';
    var btns = document.querySelectorAll('.remove-inputs');
        console.log("Found remove buttons:", btns);
    btns.forEach(button => {
        button.addEventListener('click', function(event) {
            captured_name = handleButtonClick(event);
            console.log('Captured file name:', captured_name);
//            if (captured_name) {
//                window.dash_clientside.clientside.setValue('captured-name-store', captured_name);
//            }
        });
    });
}



// SECTION 2: MAIN FUNCTION WITH CALLBACKS

(function(){
    if (!window.dash_clientside) { window.dash_clientside = {}; }
    window.dash_clientside.clientside = {

        // F0: Function to toggle options panel
        toggleOptionsPanel: function(n_clicks) {
            console.log("toggleOptionsPanel: ", n_clicks); // DEBUG
            var x = document.getElementById("optionsDiv");
            var y = document.getElementById("options");
            var z = document.getElementById("left-panelDiv");
            var tabs = document.getElementsByClassName("tab-fixed");
            if (!x || !y || !z) {
                return {display: "none"};
            }

            if (x.style.display === "none") {
                x.style.display = "block";
                y.style.backgroundColor = "#D6F2FA";
                y.style.color = "#90B6C1";
                y.innerText = "✕";
                z.style.minWidth = "198px";
                z.style.width = "25vw";

                var viewportWidth = window.innerWidth;
                var computedStyle = window.getComputedStyle(z);
                var newWidth = ((parseFloat(computedStyle.width) - 36) / 2);
                var newWidthVw = (newWidth / viewportWidth) * 100;
                width = newWidthVw + 'vw'
                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].style.setProperty('width', width, 'important');
                }

            } else {
                console.log("set default width....");
                x.style.display = "none";
                y.style.backgroundColor = "#008CBA";
                y.style.color = "white";
                y.innerText = "≡";
                z.style.minWidth = "37px";
                z.style.width = "37px";

                for (var i = 0; i < tabs.length; i++) {
                    tabs[i].style.setProperty('width', '120px', 'important');
                }
            }
            return {display: x.style.display}; // Return an object for Dash compatibility
        },
        
        // F1: Add DT buttons for each data table: edit datatable (add col/row, toggle, export, etc); 
        // F2: Add Item buttons for each data table: manage datatable (save, cache, close); 
        //     Move buttons to the expected location in DOM
        moveDataTableButtons: function() {
            var y = document.getElementById("edition-items");
            if (y) {
                var items = y.getElementsByClassName('accordion-body');
                if (items.length > 0) {
                    for(var i = 0; i < items.length; i++) {      
                        var item = items[i];
                        var menu = item.getElementsByClassName('dash-spreadsheet-menu')[0];
                        var refElem = item.getElementsByClassName('dash-spreadsheet-menu-item')[0];
                        var buttons = item.getElementsByClassName('dt-buttons')[0];
                        var format = buttons.getElementsByClassName('export-format')[0];
                        console.log("moveDataTableButtons: ", buttons); // DEBUG
                
                        // 1) Check if the buttons have already been moved; if not: style and move "dt-buttons" div above Data Table 
                        if (menu && refElem && buttons && !buttons.classList.contains('moved')) {
                            buttons.setAttribute('style', 'display: inline-flex;');
                            menu.insertBefore(buttons, refElem);
                            menu.classList.add('frame', 'p-1');
                            refElem.classList.add('vertical-line-left', 'vertical-line-right', 'ps-1', 'me-2');
                            var toggle = refElem.getElementsByClassName('show-hide')[0];
                            toggle.textContent = 'unhide cols'; 
                            toggle.setAttribute('title', 'Column Visibility Checklist: \n- Check a column to make it visible. \n- Uncheck to hide a visible column.');
                            toggle.classList.add('d-inline', 'btn', 'btn-outline-secondary', 'btn-sm', 'h28', 'me-2', 'ms-2');
                            var current = menu.getElementsByClassName('export')[0];
                            current.textContent = 'download';
                            current.setAttribute('title', 'Download current visible data from the DataTable.');
                            current.classList.add('d-inline', 'btn', 'btn-outline-secondary', 'btn-sm', 'h28', 'me-2', 'ms-1');
                            var parent = current.closest('div');
                            parent.style.display = 'flex';
                            parent.insertBefore(format, current);

                            // Mark the buttons as moved
                            buttons.classList.add('moved');
                        } else {
                            console.log('Buttons not found or already moved');
                        }
                    }
                }
                // 2) Move "my-buttons" div to inline-flex with "accordion-header"
                var items = y.getElementsByClassName('accordion-item');   
                if (items.length > 0) {
                    for(var i = 0; i < items.length; i++) {      
                        var item = items[i];
                        var btns = items[i].getElementsByClassName("accordion-body")[0].children.item(0);
                        console.log("CreateItemButtons: ", btns); // DEBUG
                        var header = items[i].getElementsByClassName('accordion-header')[0];        
                        var counts = header.getElementsByTagName('button');
                        if (counts.length == 1) {
                            header.getElementsByClassName('accordion-button')[0].setAttribute('style', 'display: inline-flex;');
                            header.appendChild(btns);
                        }
                    }
                }
            } else {
                console.log('Element with ID "edition-items" not found');
            }
            observeStyleChanges(); // Ensure this is called to observe changes
            return '';
        },

        // Helper function to update the Dash Store
/*        setValue: function(storeId, value) {
            console.log("store var: ", storeId, value);
            const storeElement = document.getElementById(storeId);
            var storeElement = sessionStorage.getItem(storeId);
            console.log(storeElement);
            if (storeElement) {
                storeElement = value;
                console.log(`Setting value for ${storeId}: ${value}`, storeElement);
            }
        }*/

        // next function goes here; add comma above!

    }
})();

// SECTION 3: ONLOAD FUNCTIONS (functions executed on page load)
window.onload = function() {
    setTimeout(function() {
        
        // Call not globally accessible functions:
        if (window.dash_clientside && window.dash_clientside.clientside) {
            window.dash_clientside.clientside.toggleOptionsPanel();
            window.dash_clientside.clientside.moveDataTableButtons();
        }

        // Call globally accessible functions:
        observeStyleChanges();
    }, 1000);
};
