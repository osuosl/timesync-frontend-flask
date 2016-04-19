function hmsToSeconds(str)
{
    var splitStr = str.split(" "),
        hours = parseInt(splitStr[0]),
        minutes = parseInt(splitStr[2]),
        seconds = parseInt(splitStr[4]);

    return (hours * 3600) + (minutes * 60) + seconds;
}

function sortAlpha(a, b, direction)
{
    if (a < b)
    {
        return -1 * direction;
    }
    else if (a > b)
    {
        return 1 * direction;
    }
    else if (a == b)
    {
        return 0;
    }
}

function sortHMS(a, b, direction)
{
    var aSeconds = hmsToSeconds(a),
        bSeconds = hmsToSeconds(b);

    return (aSeconds - bSeconds) * direction;
}

function sortDate(a, b, direction)
{
    var aTimestamp = new Date(a).getTime() / 1000,
        bTimestamp = new Date(b).getTime() / 1000;

    return (aTimestamp - bTimestamp) * direction;
}

function sortLists(a, b, direction)
{
    var aList = a.split(" "),
        bList = b.split(" ");

    aList.sort();
    bList.sort();

    return sortAlpha(aList[0], bList[0], direction);
}

function sortTable(table, col, direction)
{
    var tableHead = Array.prototype.slice.call(table.tHead.rows, 0),
        tableBody = table.tBodies[0],
        tableRows = Array.prototype.slice.call(tableBody.rows, 0);

    tableRows = tableRows.sort(
        function (a, b) {
            var columnClass = tableHead[0].cells[col].className,
                aText = a.cells[col].textContent,
                bText = b.cells[col].textContent;

            if (columnClass === "alpha")
            {
                return sortAlpha(aText, bText, direction);
            }
            else if (columnClass === "hms")
            {
                return sortHMS(aText, bText, direction);
            }
            else if (columnClass === "date")
            {
                return sortDate(aText, bText, direction);
            }
            else if (columnClass == "list")
            {
                return sortLists(aText, bText, direction);
            }
            else
            {
                return 0; // Can't sort otherwise
            }
        });

    for (var i = 0; i < tableRows.length; i++)
    {
        tableBody.appendChild(tableRows[i]);
    }
}

function makeSortable(table)
{
    var tableHead = Array.prototype.slice.call(table.tHead.rows, 0);

    if (!tableHead) return;

    for (var i = 0; i < tableHead[0].cells.length; i++)
    {
        var columnClass = tableHead[0].cells[i].className;

        // Only make it sortable if the class is valid
        if (columnClass !== "alpha"
         && columnClass !== "hms"
         && columnClass !== "date"
         && columnClass !== "list")
        {
            continue;
        }

        // Make cursor indicate that it is clickable
        tableHead[0].cells[i].style.cursor = "pointer";

        // Closure to keep track of current sort direction
        function tableClosure (i) {
            var direction = 1;

            tableHead[0].cells[i].addEventListener('click',
                function () {
                    sortTable(table, i, direction);

                    direction *= -1; // Switch directions
                });
        }

        tableClosure(i);
    }
}

function makeAllSortable()
{
    var tables = document.body.getElementsByTagName('table');

    for (var i = 0; i < tables.length; i++)
    {
        makeSortable(tables[i]);

        sortTable(tables[i], 3, -1); // Initial sort by most recent
    }
}

window.onload = makeAllSortable;
