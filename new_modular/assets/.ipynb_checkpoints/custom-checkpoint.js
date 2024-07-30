// SECTION 1: GLOBALLY ACCESSIBLE FUNCTIONS

// F tmp
function SaveItem() {
//  console.log('');
  return alert('Do you want save it?'); 
}

// F tmp
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
function observeStyleChanges() {
    var buttons = document.querySelectorAll('.dt-buttons');
    var observerCallback = function(mutationsList) {
        for (var mutation of mutationsList) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                var targetElement = mutation.target;
                if (targetElement.style.display === 'none') {
                    MoveDataTableButtons();
                }
            }
        }
    };
    var observerOptions = { attributes: true, attributeFilter: ['style'] };

    buttons.forEach(function(button) {
        var observer = new MutationObserver(observerCallback);
        observer.observe(button, observerOptions);
    });
}



// SECTION 2: MAIN FUNCTION WITH CALLBACKS

(function(){
  if(!window.dash_clientside) {window.dash_clientside = {};}
  window.dash_clientside.clientside = {

// F1: Add Item buttons for each data table: manage datatable (save, cache, close)
      CreateItemButtons: () => {

        var y = document.getElementById("edition-items");
        var items = y.getElementsByClassName('accordion-item');
        
        if (items.length > 0) {
          for(var i = 0; i < items.length; i++) {      
            var item = items[i];
            btns = items[i].getElementsByClassName("accordion-body")[0].children.item(0);
            console.log("CreateItemButtons: ", btns);                                        // DEBUG
            header = items[i].getElementsByClassName('accordion-header')[0];        
            counts = header.getElementsByTagName('button');
            if (counts.length == 1) {
              header.getElementsByClassName('accordion-button')[0].setAttribute('style', 'display: inline-flex;');
              header.appendChild(btns);
            };
          };
        };
        return '';
      },

// F2: Add DT buttons for each data table: edit datatable (add col/row, toggle, export, etc)
      MoveDataTableButtons: function() {
        // Get all the DataTable menus
        var y = document.getElementById("edition-items");
        if (y) {
          var items = y.getElementsByClassName('accordion-body');
          if (items.length > 0) {
            for(var i = 0; i < items.length; i++) {      
              var item = items[i];
              var menu = item.getElementsByClassName('dash-spreadsheet-menu')[0];
              var refElem  = item.getElementsByClassName('dash-spreadsheet-menu-item')[0];
              var buttons = item.getElementsByClassName('dt-buttons')[0];
              var format = buttons.getElementsByClassName('export-format')[0];
              console.log("MoveDataTableButtons: ", buttons)                                 // DEBUG
              
              if (menu && refElem && buttons) {
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
              } else {
                console.log('Element Menu, Reference or Buttons not found');
              }
            };
          };
        } else {
          console.log('Element with ID "edition-items" not found');
        }
        return '';
        observeStyleChanges();
      },

      
// final closing brackets below
  }
})();



// SECTION3: ONLOAD FUNCTIONS
window.onload = function() {
    setTimeout(function() {
        
        // Call not globally accessible functions:
        if (window.dash_clientside && window.dash_clientside.clientside) {
            window.dash_clientside.clientside.MoveDataTableButtons();
        }

        // Call globally accessible functions:
        observeStyleChanges();
    }, 1000);
};





