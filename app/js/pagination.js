/* Main function
Para:   listSelector (string)
        tableSelector (string)
        perPage (int)
*/
function pagination(listSelector, tableSelector, perPage) {
    var numOfItems = $(tableSelector + " tbody tr").length;
    var numOfPages = Math.ceil(numOfItems / perPage);
    var list = $(listSelector)[0];
    if (numOfItems > 0) {
        var paginate = new Paginate(numOfPages, numOfItems, perPage, list, tableSelector);
        paginate.constructMenu();
    }
}


// Pagination class function constructor
var Paginate = function(numOfPages, numOfItems, perPage, list, tableSelector){
    this.numOfPages = numOfPages;   // int
    this.numOfItems = numOfItems;   // int
    this.perPage = perPage;         // int
    this.tableSelector = tableSelector; // string
    this.currPageNum = 1;           // Current Page Number
    this.listItems = document.getElementsByClassName("paginate"); // [DOM obj]

    // Construct the button menus
    this.constructMenu = function() {
        // Constructor left arrow
        list.appendChild(makeListItem("disabled", true, "chevron_left", 1));
        list.appendChild(makeListItem("disabled", false, "..", 0)); // Index not set
        for (var i = 1; i <= numOfPages; i++) {
            list.appendChild(makeListItem("", false, i, i));
        }
        list.appendChild(makeListItem("disabled", false, "..", 0)); // Index not set
        // Constructor right arrow
        list.appendChild(makeListItem("disabled", true, "chevron_right", numOfPages));
        // Update menu so all index are updated
        this.updateMenu(1);
        this.hideButtons();
        this.showTable();
        location.hash = "#page-" + this.currPageNum;
        // Add Event Handler for each page button
        for (var i = 0; i < this.listItems.length; i++) {
            var menu = this;
            this.listItems[i].addEventListener("click", function() {
                window.location.hash = this.href;
                var classNames = this.className.split(" ");
                var clickable = true;
                // Check if button is disabled
                classNames.forEach(function(name) {
                    if (name == "disabled" || name == "active")
                        clickable = false;
                });
                if (clickable) {
                    menu.updateMenu(this.index);
                    menu.hideButtons();
                    menu.showTable();
                    location.hash = "#page-" + menu.currPageNum;
                }
            });
        }
    }

    // Update the menu, clickedIndex (int)
    this.updateMenu = function(clickedIndex) {
        // remove the active state of current active button
        this.setClass(this.currPageNum + 1, "");
        // update the current page number, and update the button active states
        this.currPageNum = this.listItems[clickedIndex + 1].index;
        var numOfButtons = this.listItems.length;
        this.updateIcon(numOfButtons);
        this.updateSkipButton(numOfButtons);

        // add active class to the new current page button
        this.setClass(this.currPageNum + 1, "active");
    }

    // update all the icons accordingly
    this.updateIcon = function(numOfButtons) {
        if (this.currPageNum == 1) {
            this.setClass(0, "disabled");
        }
        else {
            this.setClass(0, "");
        }
        if (this.currPageNum == this.numOfPages) {
            this.setClass(numOfButtons - 1, "disabled");
        }
        else {
            this.setClass(numOfButtons - 1, "");
        }
    }

    // update the ".." skipping button index
    this.updateSkipButton = function(numOfButtons) {
        if (this.currPageNum <= 2) {
            this.setClass(1, "disabled");
        }
        else {
            this.setClass(1, "");
            if (this.currPageNum < this.numOfPages) {
                this.listItems[1].index = this.currPageNum - 2;
            }
            else {
                this.listItems[1].index = this.currPageNum - 3;
            }
        }
        if (this.currPageNum >= this.numOfPages - 1) {
            this.setClass(numOfButtons - 2, "disabled");
        }
        else {
            this.setClass(numOfButtons - 2, "");
            if (this.currPageNum > 1) {
                this.listItems[numOfButtons - 2].index = this.currPageNum + 2;
            }
            else {
                this.listItems[numOfButtons - 2].index = this.currPageNum + 3;
            }
        }
        if (this.numOfPages <= 3) {
            this.setClass(1, "disabled");
            this.setClass(numOfButtons - 2, "disabled");
        }
    }

    // Hide buttons that are too far from current page
    this.hideButtons = function() {
        // show all buttons
        pageButtons = $(".paginate").slice(2, this.numOfPages + 2).hide();
        if (this.currPageNum <= 2){
            pageButtons.slice(0, 3).show();
        }
        else if (this.currPageNum >= this.numOfPages - 1) {
            pageButtons.slice(this.numOfPages - 3).show();
        }
        pageButtons.slice(this.currPageNum - 2, this.currPageNum + 1).show();
    }

    // Set the class Name for button (disabled, active)
    this.setClass = function(index, name) {
        // concat class name for button
        var classNames = this.listItems[index].className.split(" ");
        if (classNames[0] != name) {
            classNames[0] = name;
        }
        this.listItems[index].className = classNames[0] + " paginate";
        // set the cursor style for the button
        if (name == "disabled") {
            this.listItems[index].style.cursor = "default";
        }
        else {
            this.listItems[index].style.cursor = "pointer";
        }
    }

    // Show the table of a page
    this.showTable = function() {
        var start = this.perPage * (this.currPageNum - 1);
        var end = start + this.perPage;
        var table = $(this.tableSelector + " tbody tr");
        var slicedTable = table.hide().slice(start, end);
        slicedTable.show();
    }
}


/* Utility Functions */

/* Make Items in the list for pagination
 Para:  className (string)
        isIcon (bool)
        beActive (bool)
        itemContent (string, int)
        index (int)
*/
function makeListItem (className, isIcon, itemContent, index) {
    var li = document.createElement("li");
    li.style.cursor = "pointer";
    li.className = className;
    li.className += " paginate";
    // Set the index button points to
    li.index = index;
    var a = document.createElement("a");
    var text = document.createTextNode(itemContent);

    // Check if it is icon
    if (isIcon) {
        var i = document.createElement("i");
        i.className = "material-icons";
        a.appendChild(i);
        i.appendChild(text);
    }
    else {
        a.appendChild(text);
    }

    li.appendChild(a);
    return li;
}
