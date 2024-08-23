let rankingType = "qs";
let rankingTypeData = [];
let pageIndex = 0;
let totalUniversities;
let totalPages;
let itemsPerPage;

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
        return `/api/qs_universities/?page=${pageIndex}`;
    } else if (rankingType == "the") {
        return `/api/the_universities/?page=${pageIndex}`;
    } else {
        return "";
    }
}

async function displayEntries() {
    try {
        const data = await getEntries();
        rankingTypeData = { rankingType, entries: data };
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
            rank: entry.qs_rank,
            name: entry.title,
            overall_score: entry.overall_score,
            totalUniversities: entry.total_records
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

// Display fetched data in the UI
function displayEntriesList() {
    const body = document.querySelector('#unvListing');
    body.innerHTML = '';

    let r = pageIndex * 10; // For ordering
    rankingTypeData.entries.forEach(entry => {
        r++;
        const row = document.createElement('div');
        row.className = "custom-rectangle3";
        row.innerHTML = `
            <table class="pizda">
                <thead>
                    <tr>
                        <th>${r}</th>
                        <th>${entry.name}</th>
                        <th>${entry.rank}</th>
                        <th>${entry.overall_score}</th>
                    </tr>
                </thead>
            </table>
        `;
        body.appendChild(row);
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
