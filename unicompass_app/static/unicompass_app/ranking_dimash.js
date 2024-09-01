let rankingType = "qs";
let rankingTypeData = [];
let kzUniversitiesData = [];
let pageIndex = 0;
let totalUniversities;
let totalPages;
let itemsPerPage;
let subject = 'general';

// Fetches data and calculates total pages dynamically
async function countPages() {
    const url = fetchData();

    try {
        const response = await fetch(url);
        const data = await response.json();

        // Get the total records and items per page from the response
        totalUniversities = data.total_records;
        totalPages = data.total_pages;
        itemsPerPage = data.items_per_page;

        console.log(`Total Records: ${totalUniversities}, Total Pages: ${totalPages}, Items Per Page: ${itemsPerPage}`);

        createPagination(1);  // Initialize pagination with the first page
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Fetches the correct URL based on the ranking type and page index
function fetchData() {
    if (rankingType == "qs") {
        return `/api/qs_universities/?page=${pageIndex}&subject=${subject}`;
    } else if (rankingType == "the") {
        return `/api/the_universities/?page=${pageIndex}&subject=${subject}`;
    } else {
        return "";
    }
}

// Fetches data from the KZ API
async function fetchKZUniversities() {
    try {
        const response = await fetch('/api/kz_universities/');
        const data = await response.json();

        if (!data.data) throw new Error("No KZ data found");

        return data.data.map(entry => ({
            name: entry.title
        }));
    } catch (error) {
        console.error('Error fetching KZ universities data:', error);
        throw error;
    }
}

async function displayEntries() {
    try {
        const data = await getEntries();
        rankingTypeData = { rankingType, entries: data };

        // Fetch KZ universities and store the result
        kzUniversitiesData = await fetchKZUniversities();

        displayEntriesList();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

// Fetches and formats the entries for display
async function getEntries() {
    const url = fetchData();

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!data.data) throw new Error("No data found");

        return data.data.map(entry => ({
            rank: entry.rank,
            name: entry.title,
            overall_score: entry.overall_score
        }));
    } catch (error) {
        console.error('Error fetching some universities data:', error);
        throw error;
    }
}

// Creates the pagination buttons dynamically
function createPagination(currentPage) {
    const pagination = document.querySelector('.pagination');
    pagination.innerHTML = '';

    let startPage, endPage;
    const maxButtons = 5;  // You can set how many buttons you want visible at a time

    if (totalPages <= maxButtons) {
        startPage = 1;
        endPage = totalPages;
    } else if (currentPage <= 3) {
        startPage = 1;
        endPage = maxButtons;
    } else if (currentPage + 2 >= totalPages) {
        startPage = totalPages - maxButtons + 1;
        endPage = totalPages;
    } else {
        startPage = currentPage - 2;
        endPage = currentPage + 2;
    }

    // Generate pagination buttons
    for (let i = startPage; i <= endPage; i++) {
        const pageButton = document.createElement('div');
        pageButton.className = 'page-item';
        pageButton.innerHTML = i;

        if (i === currentPage) {
            pageButton.classList.add('active');
        }

        pageButton.addEventListener('click', () => {
            pageIndex = i - 1;
            displayEntries();
            createPagination(i);
        });

        pagination.appendChild(pageButton);
    }
}

// Display fetched data in the UI, including KZ universities with a separator
function displayEntriesList() {
    const rbody = document.getElementById('unvListin');
    rbody.innerHTML = '';

    let r = pageIndex * 10; // For ordering
    rankingTypeData.entries.forEach(entry => {
        r++;
        const row = document.createElement('div');
        const rtable = document.createElement('table');
        rtable.className = "University";
        row.className = "custom-button";
        rtable.innerHTML = `
            <thead>
                <tr>
                    <th>${r}</th>
                    <th>${entry.name}</th>
                    <th>${entry.rank}</th>
                    <th>${entry.overall_score}</th>
                </tr>
            </thead>
        `;
        row.appendChild(rtable);
        rbody.appendChild(row);
    });

    // Add a line separator after QS and THE universities
    const separator = document.createElement('hr');
    rbody.appendChild(separator);

    // Display KZ universities below the separator
    kzUniversitiesData.forEach(entry => {
        const row = document.createElement('div');
        const rtable = document.createElement('table');
        rtable.className = "University";
        row.className = "custom-button";
        rtable.innerHTML = `
            <thead>
                <tr>
                    <th>${r + 1}</th>
                    <th>${entry.name}</th>
                </tr>
            </thead>
        `;
        row.appendChild(rtable);
        rbody.appendChild(row);
        r++;
    });
}

// Initialize the data fetching and pagination setup on page load
document.addEventListener('DOMContentLoaded', async function () {

    try {
        await countPages();  // Fetch data and setup pagination
        await displayEntries();  // Display entries for the first page
    } catch (error) {
        console.error('Error initializing page:', error);
    }
});

function toggleSwitch(takenRank) {
    if (takenRank != rankingType) {
        rankingType = takenRank;
        console.log(`The ranking is ${rankingType}`)
        pageIndex = 0;

        // Clear the search input field
        const searchInput = document.querySelector('.search-input');
        searchInput.value = '';

        // Refresh the data
        countPages();
        displayEntries();
        createPagination(1);
    }
}


// All animation functions::::
function leftSwitchRank() {
    subject = 'general'
    const btn = document.getElementById('btn-rank');
    btn.style.left = '0px';

}

function rightSwitchRank() {
    subject = 'general'
    const btn = document.getElementById('btn-rank');
    btn.style.left = '157px';
}

function leftSwitchSubject() {
    const btn = document.getElementById('btn-subject');
    btn.style.left = '0px';
}

function rightSwitchSubject() {
    const btn = document.getElementById('btn-subject');
    btn.style.left = '157px';
    if (rankingType == 'the') {
        window.location.hash = 'popup2';
        closeButton = document.querySelector('.close');
        if (closeButton.click) {
            leftSwitchSubject();
        }
    }
    else if (rankingType == 'qs') {
        window.location.hash = 'popup1';
        closeButton = document.querySelector('.close');
        if (closeButton.click) {
            leftSwitchSubject();
        }
    }
    document.querySelectorAll('#popup1 button[data-subject], #popup2 button[data-subject], ul li button').forEach(function(button) {
        button.addEventListener('click', function() {

            subject = this.parentElement.getAttribute('data-subject') || this.getAttribute('data-subject');

            displayEntries();
            closeButton = document.querySelector('.close');
            closeButton.click();
        });
    });
}

async function instantSearch() {
    const searchTerm = document.querySelector('.search-input').value.trim().toLowerCase();
    const rbody = document.getElementById('unvListin');

    if (!rbody) {
        console.error('Element with id "unvListin" not found.');
        return;
    }

    rbody.innerHTML = ''; // Clear previous results

    if (searchTerm === '') {
        displayEntriesList(); // Display all data if search term is empty
        return;
    }

    // Filter QS and THE universities
    const searchResults = rankingTypeData.entries.filter(entry => 
        entry.name.toLowerCase().includes(searchTerm)
    );

    // Filter KZ universities directly from the kzUniversitiesData array
    const searchResultsKZ = kzUniversitiesData.filter(entry => 
        entry.name.toLowerCase().includes(searchTerm)
    );

    let r = pageIndex * 10; // Reset rank counter

    if (searchResults.length > 0) {
        searchResults.forEach(entry => {
            r++;
            const row = document.createElement('div');
            const rtable = document.createElement('table');
            rtable.className = "University";
            row.className = "custom-button";
            rtable.innerHTML = `
                <thead>
                    <tr>
                        <th>${r}</th>
                        <th>${entry.name}</th>
                        <th>${entry.rank}</th>
                        <th>${entry.overall_score}</th>
                    </tr>
                </thead>
            `;
            row.appendChild(rtable);
            rbody.appendChild(row);
        });
    }

    if (searchResultsKZ.length > 0) {
        searchResultsKZ.forEach(entry => {
            r++;
            const row = document.createElement('div');
            const rtable = document.createElement('table');
            rtable.className = "University";
            row.className = "custom-button";
            rtable.innerHTML = `
                <thead>
                    <tr>
                        <th>${r}</th>
                        <th>${entry.name}</th>
                    </tr>
                </thead>
            `;
            row.appendChild(rtable);
            rbody.appendChild(row);
        });
    } else if (searchResults.length === 0 && searchResultsKZ.length === 0) {
        // No results found
        const noResultsRow = document.createElement('div');
        noResultsRow.className = "no-results";
        noResultsRow.innerHTML = `<p>No results found for "${searchTerm}".</p>`;
        rbody.appendChild(noResultsRow);
    }
}
