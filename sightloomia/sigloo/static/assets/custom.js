// SECTION 1: General JS function, applicable to all apps; added initially on load to set listeners and observers
const optionsWidth = 400;
let currentWindowHeight = window.innerHeight;

// Function to update the current window height
//function updateWindowHeight() {currentWindowHeight = window.innerHeight; console.log("HERE: ", currentWindowHeight)}
//window.addEventListener('resize', updateWindowHeight);
//updateWindowHeight();



////// --- django tabs management
// Django app framework: manage all tabs and mark currently active tab
document.addEventListener("DOMContentLoaded", function() {
    // Get the current path, ignoring any trailing slash
    const currentPath = window.location.pathname.replace(/\/$/, "");

    // Select all navigation links in the menu
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");

    navLinks.forEach(link => {
        // Get the link's href path, ignoring any trailing slash
        const linkPath = new URL(link.href).pathname.replace(/\/$/, "");
        // Check if the link's path matches the current path
        if (linkPath === currentPath) {
            // Remove 'active' from any previously active link to ensure only one is highlighted
            navLinks.forEach(navLink => navLink.classList.remove("active"));
            // Add 'active' to the matching link
            link.classList.add("active");
        }
    });
});


////// --- django/dash panels dynamic adjustment
// toogle apps option menu bar (leftPanel) and shift rightPanel content (app part only: graph and raw outputs)
window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.clientside = {
    toggleSidebar: function(n_clicks) {
        const leftPanelDiv = document.getElementById('left-panelDiv');
        const optionsDiv = document.getElementById('optionsDiv');
        const dataGraph = document.getElementById('data-graph');
        const optionsBtn = document.getElementById('options-btn');

        // Check if elements exist
        if (!leftPanelDiv || !optionsDiv) {
            console.log("Elements not found in Dash app.");
            return window.dash_clientside.no_update;
        }

        // Toggle expansion state based on current width
        const isExpanded = leftPanelDiv.style.width === `${optionsWidth}px`;
        
        leftPanelDiv.style.width = isExpanded ? '37px' : `${optionsWidth}px`;
        optionsDiv.style.display = isExpanded ? 'none' : 'block';

        const leftPanelWidth = isExpanded ? 37 : optionsWidth;
        const availableWidth = window.innerWidth - leftPanelWidth - 28;
        dataGraph.style.width = `${availableWidth}px`;
        dataGraph.style.left = `${leftPanelWidth}px`;
        const btnBG = isExpanded ? "#008CBA" : "#D6F2FA";
        const btnColor = isExpanded ? "white" : "#90B6C1";
        const btnText = isExpanded ? "≡" : "✕";
        optionsBtn.style.backgroundColor = btnBG;
        optionsBtn.style.color = btnColor; 
        optionsBtn.innerText = btnText;

        // Send a message to the main document with the updated width
        window.parent.postMessage({ action: 'updateDataGraph', availableWidth, leftPanelWidth }, '*');

        return window.dash_clientside.no_update;
    }
};

// Function to adjust data-graph width dynamically on window resize
function handleResize() {

    const leftPanelDiv = document.getElementById('left-panelDiv');
    const dataGraph = document.getElementById('data-graph');

    if (!leftPanelDiv || !dataGraph) return;

    const leftPanelWidth = leftPanelDiv.style.width === `${optionsWidth}px` ? optionsWidth : 37;
    const availableWidth = window.innerWidth - leftPanelWidth - 28;

    dataGraph.style.width = `${availableWidth}px`;
    dataGraph.style.left = `${leftPanelWidth}px`;

    // Send updated width to parent
    window.parent.postMessage({ action: 'updateDataGraph', availableWidth, leftPanelWidth }, '*');
}
// Listen for window resize to dynamically adjust widths
window.addEventListener('resize', handleResize);


// toogle apps option menu bar (leftPanel) and shift rightPanel content (html part only part only: data editor, separate shared app) 
window.addEventListener('message', (event) => {
    // Check for specific message action
    if (event.data && event.data.action === 'updateDataGraph') {
        const dataEditor = document.getElementById('data-editor-parent');
        const fixedTabs = document.getElementsByClassName('nav-item tab-fixed');
        if (dataEditor) {
            dataEditor.style.width = `${event.data.availableWidth}px`;
            dataEditor.style.left = `${event.data.leftPanelWidth - 37}px`;
            const fixedWidth = event.data.leftPanelWidth === optionsWidth ? `${(optionsWidth - 53) / 2}px` : '80px';
            Array.from(fixedTabs).forEach(tab => {tab.style.width = fixedWidth;});
        }
    }
});

// Function to adjust data-editor width dynamically on window resize
function handleMainResize() {
    const dataEditor = document.getElementById('data-editor-parent');

    // Recalculate availableWidth based on iframe's current sidebar width
    const iframe = document.querySelector('iframe');
    if (iframe && dataEditor) {
        const leftPanelWidth = parseInt(dataEditor.style.left, 10) + 37 || 37;
        const availableWidth = window.innerWidth - leftPanelWidth - 28;
        dataEditor.style.width = `${availableWidth}`;
    }
}
// Listen for window resize events in the main document
window.addEventListener('resize', handleMainResize);


// move 'data-graph' container depending on collapse state of the 'data-editor'
window.onload = function() {
    const iframes = document.querySelectorAll('iframe');
    const dataEditors = document.querySelectorAll('.data-editor');

    let isExpanded = false;

    dataEditors.forEach((dataEditor, index) => {

        // Function to set 'top' for the corresponding .data-graph inside the correct iframe
        function updateIframeTopProperty(iframe, editorHeight) {
            const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
            if (!iframeDoc) {
                console.log("INFO: Iframe document not accessible yet.");
                return;
            }

            const dataGraph = iframeDoc.querySelector('.data-graph');
            if (dataGraph) {
                dataGraph.style.top = `${editorHeight}px`;
            }
            const leftPanelDiv = iframeDoc.getElementById('left-panelDiv');
            if (leftPanelDiv){
                leftPanelDiv.style.height = `${window.innerHeight - 85}px`;
            }
        }

        // Set up ResizeObserver for each dataEditor to monitor height changes
        const resizeObserver = new ResizeObserver(entries => {
            for (let entry of entries) {
                const editorHeight = entry.contentRect.height;
                iframes.forEach(iframe => {
                    updateIframeTopProperty(iframe, editorHeight); // Update 'top' for .data-graph in iframe on resize
                });
            }
        });

        resizeObserver.observe(dataEditor);
        console.log("ResizeObserver set up for dataEditor", dataEditor);

        // Additional listener for window resize to handle any dynamic layout adjustments
        window.addEventListener('resize', () => {
            const editorHeight = dataEditor.offsetHeight;
            iframes.forEach(iframe => {
                updateIframeTopProperty(iframe, editorHeight); // Update 'top' for each iframe on resize
            });
        });
        console.log("Window resize listener added.");

        // Add onload event listener to each iframe to ensure it's fully loaded
        iframes.forEach(iframe => {
            iframe.onload = function() {
                const editorHeight = dataEditor.offsetHeight;
                updateIframeTopProperty(iframe, editorHeight); // Initial 'top' setting after iframe loads
            };
        });
    });
};


/////

document.addEventListener('DOMContentLoaded', function () {
    const cards = document.querySelectorAll('.draggable-card');

    cards.forEach(card => {
        // Make each card draggable
        card.setAttribute('draggable', true);

        card.addEventListener('dragstart', function (e) {
            e.dataTransfer.setData('text/plain', e.target.id);
            e.target.classList.add('dragging');
        });

        card.addEventListener('dragend', function (e) {
            e.target.classList.remove('dragging');
        });

        card.addEventListener('dragover', function (e) {
            e.preventDefault();
            const afterElement = getDragAfterElement(e.clientY);
            const container = card.parentNode;
            const draggedId = e.dataTransfer.getData('text/plain');
            const draggedCard = document.getElementById(draggedId);

            if (afterElement == null) {
                container.appendChild(draggedCard);
            } else {
                container.insertBefore(draggedCard, afterElement);
            }
        });
    });

    // Helper function to find where to insert the dragged element
    function getDragAfterElement(y) {
        const draggableElements = [...document.querySelectorAll('.draggable-card:not(.dragging)')];
        
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }
});
