function hmsToSeconds(str) {
    var splitStr = str.split(" "),
        hours = parseInt(splitStr[0]),
        minutes = parseInt(splitStr[2]),
        seconds = parseInt(splitStr[4]);

    return (hours * 3600) + (minutes * 60) + seconds;
}

function sortAlpha(a, b, direction) {
    var a_lower = a.toLowerCase();
    var b_lower = b.toLowerCase();

    if (a_lower < b_lower) {
        return -1 * direction;
    } else if (a_lower > b_lower) {
        return 1 * direction;
    } else if (a_lower == b_lower) {
        return 0;
    }
}

function sortHMS(a, b, direction) {
    var aSeconds = hmsToSeconds(a),
        bSeconds = hmsToSeconds(b);

    return (aSeconds - bSeconds) * direction;
}

function sortDate(a, b, direction) {
    var aTimestamp = new Date(a).getTime() / 1000,
        bTimestamp = new Date(b).getTime() / 1000;

    return (aTimestamp - bTimestamp) * direction;
}

function sortLists(a, b, direction) {
    var aList = a.split(" "),
        bList = b.split(" ");

    aList.sort();
    bList.sort();

    return sortAlpha(aList[0], bList[0], direction);
}

function paginateTable(tableSelector, perPage, pageNum) {
    var showStart = perPage * (pageNum - 1);
    var showEnd = showStart + perPage;

    $(tableSelector + " tbody tr").hide().slice(showStart, showEnd).show();
}

function addPagination(tableSelector, perPage) {
    $("#paginator").pagination({
        items: $(tableSelector + " tbody tr").length,
        itemsOnPage: perPage,
        cssStyle: "compact-theme",
        onPageClick: function(pageNumber) {
            paginateTable(tableSelector, perPage, pageNumber);
        }
    });
}

function sortTable(tableSelector, perPage, column, order) {
    var table = $(tableSelector);
    var tableBody = table.find("tbody");
    var tableItems = tableBody.find("tr");
    var headerClass = table.find("th").eq(column).attr("class").split(' ')[0];
    var direction = (order === "asc") ? 1 : -1;
    var pageAnchor = window.location.hash;
    var pageNum;

    if (pageAnchor.length > 0) {
        pageNum = parseInt(pageAnchor.split('-')[1]);
    } else {
        pageNum = 1;
    }

    tableItems.sort(function(a, b) {
        var aText = $(a).find("td").eq(column).text();
        var bText = $(b).find("td").eq(column).text();

        if (headerClass === "alpha") {
            return sortAlpha(aText, bText, direction);
        } else if (headerClass === "hms")  {
            return sortHMS(aText, bText, direction);
        } else if (headerClass === "date") {
            return sortDate(aText, bText, direction);
        } else if (headerClass == "list") {
            return sortLists(aText, bText, direction);
        } else {
            return 0; // Can't sort otherwise
        }
    }).appendTo(tableBody);
    if (headerClass != "alpha" || "hms" || "date" || "list") {
        paginateTable(tableSelector, perPage, pageNum);
    }
}

function makeSortable(tableSelector, perPage, initColumn, initDirection) {
    var columnSelector = tableSelector + " th";

    // Change pointer type on sortable headers
    $(columnSelector).filter(function() {
        return this.className.length > 0;
    }).css({"cursor": "pointer"});

    // Add click handler to table headers
    $(columnSelector).click(function() {
        $(columnSelector).not($(this)).removeClass("sorted-asc sorted-desc");
        if ($(this)[0].className == "") {
            return;
        }
        if ($(this).hasClass("sorted-asc") || $(this).hasClass("sorted-desc")) {
            $(this).toggleClass("sorted-asc sorted-desc");
        } else {
            $(this).addClass("sorted-asc");
        }

        sortTable(tableSelector,
                  perPage,
                  $(this).index(),
                  this.className.split('-')[1]);
    });

    $(columnSelector).eq(initColumn).addClass("sorted-" + initDirection);

    sortTable(tableSelector,
              perPage,
              initColumn,
              initDirection);
}
