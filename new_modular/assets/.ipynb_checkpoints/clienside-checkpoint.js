/**
 * Toggle the display of the options panel on the left.
 * @param {number} n_clicks - The number of times the toggle button has been clicked.
 */
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    optionsPanel: {
        toggleOptions: function(n_clicks) {
            var x = document.getElementById("optionsDiv");
            var y = document.getElementById("btn-options");
            var z = document.getElementById("left-panelDiv");
            if (x.style.display === "none") {
                x.style.display = "block";
                y.style.backgroundColor = "#D6F2FA";
                y.style.color = "#90B6C1";
                y.innerText = "✕";
                z.style.width = "25vw";
            } else {
                x.style.display = "none";
                y.style.backgroundColor = "#008CBA";
                y.style.color = "white";
                y.innerText = "≡";
                z.style.width = "2.7%";
            }
        }
    },
    rightPanel: {
        /**
         * Automatically unfold the Edit Input Data panel when user selects to edit any file.
         * @param {Array<number>} n_clicks - An array of click counts for each edit button.
         * @param {Array<string>} activeItems - Currently active items in the accordion.
         * @returns {Array<string>} - Updated list of active items.
         */
        unfoldEditPanel: function(n_clicks, activeItems) {
            var isClicked = n_clicks.some(function(clicks) { return clicks > 0; });
            if (!activeItems) { activeItems = []; }
            if (isClicked && !activeItems.includes('item-11')) {
                activeItems.push('item-11');
                return activeItems;
            }
            return activeItems;
        },
        
         /**
         * Create item buttons for DataTables.
         * This function handles the logic for creating buttons in a DataTable.
         */
        createItemButtons: function() {
            var buttons = document.querySelectorAll('[id^="item-"]');
            buttons.forEach(function(button) {
                // Add your custom button creation logic here
                button.innerText = "Item Button";
                button.style.backgroundColor = "#28a745";
                button.style.color = "white";
                button.style.border = "none";
                button.style.padding = "5px 10px";
                button.style.cursor = "pointer";
            });
        },
        
        /**
         * Create DataTable buttons.
         * This function handles the logic for moving DataTable buttons.
         * @param {Array} children - The children of the edition items container.
         */
        moveDataTableButtons: function(children) {
            // Logic for moving DataTable buttons
            var dataTableButtons = document.querySelectorAll('[id^="datatable-button-"]');
            dataTableButtons.forEach(function(button) {
                // Add your custom logic for moving buttons here
                button.style.margin = "5px";
                button.style.backgroundColor = "#ffc107";
                button.style.color = "black";
                button.style.border = "1px solid #dee2e6";
                button.style.padding = "5px 10px";
                button.style.cursor = "pointer";
            });
        }
    }
});
