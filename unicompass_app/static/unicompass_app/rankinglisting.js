//TODO add other subjects, fix query unipage, fix alert

let currentSource = 'topuniversities';
let currentData = [];

const subjectMap = {
    "qs-general": '3897789',
    "qs-engineering-technologies": '3948167',
    "qs-arts-humanities": '3948166',
    "qs-life-sciences-medicine": '3948168',
    "qs-natural-sciences": '3948169',
    "qs-social-sciences-management": '3948170',
    "qs-linguistics": '3948214',
    "qs-music": '3948226',
    "qs-theology-divinity-religious": '3948201',
    "qs-archaeology": '3948175',
    "qs-architecture-built-environment": '3948176',
    "qs-art-design": '3948177',
    "qs-classics-ancient-history": '3948181',
    "qs-english-language-literature": '3948194',
    "qs-history": '3948202',
    "qs-history-of-art": '3948220',
    "qs-modern-languages": '3948219',
    "qs-performing-arts": '3948215',
    "qs-philosophy": '3948211',
    "the-general": 'general'
};

async function getEntriesTopUniversities(subject = 'qs-general') {
    const subjectId = subjectMap[subject];
    const url = `/api/qs_universities/?items_per_page=1000`; // Fetch all items

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
        console.error('Error fetching Top Universities data:', error);
        throw error;
    }
}

async function getEntriesTimesHigherEducation(subjectname = 'general') {
    const url = `/api/the_universities/?items_per_page=1000`; // Fetch all items

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (!data.data) throw new Error("No data found");

        return data.data.map(entry => ({
            rank: entry.rank,
            name: entry.name,
            overall_score: entry.scores_overall,
        }));
    } catch (error) {
        console.error('Error fetching data from your API:', error);
        throw error;
    }
}

async function displayEntries(element) {
    const subject = element.getAttribute('data-subject');
    const subjectName = element.textContent;

    const alertContent = document.getElementById('alertContent');
    alertContent.textContent = `Ranking: ${currentSource === 'topuniversities' ? 'QS' : 'THE'}\nSubject Filter: ${subjectName}`;

    document.getElementById('loadingSpinner').style.display = 'block';

    try {
        let data;
        if (currentSource === 'topuniversities') {
            data = await getEntriesTopUniversities(subject);
        } else if (currentSource === 'timeshighereducation') {
            data = await getEntriesTimesHigherEducation(subject);
        }
        currentData = { subject, entries: data };
        displayEntriesList();
    } catch (error) {
        console.error('Error fetching data:', error);
    } finally {
        document.getElementById('loadingSpinner').style.display = 'none';
        $(`#modal-${currentSource}`).modal('hide');
    }
}

function displayEntriesList() {
    const tbody = document.querySelector('#unisTable tbody');
    tbody.innerHTML = '';

    const actualRanking = document.querySelector('#actualRanking');
    actualRanking.innerHTML = currentSource === 'topuniversities' ? 'Rank by QS' : 'Rank by THE';

    let r = 0; // Initialize rank counter
    currentData.entries.forEach(entry => {
        r++;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${r}</td>
            <td>${entry.name}
                <div class="details-button-container">
                    <button class="btn btn-info" onclick="redirectToUniversityPage('${entry.name}')">Details</button>
                </div>
            </td>
            <td>${entry.rank}</td>
            <td>${entry.overall_score}</td>
        `;
        tbody.appendChild(row);
    });
}

function switchSource(source) {
    currentSource = source;
    const modalId = `#modal-${source}`;
    $(modalId).modal('show');
}

async function instantSearch() {
    const searchTerm = document.getElementById('searchBar').value.trim().toLowerCase();
    const tbody = document.querySelector('#unisTable tbody');
    tbody.innerHTML = ''; // Clear previous results

    if (searchTerm === '') {
        displayEntriesList(); // Display all data if search term is empty
        return;
    }

    const searchResults = currentData.entries.filter(entry => entry.name.toLowerCase().includes(searchTerm));

    if (searchResults.length > 0) {
        let r = 0; // Reset rank counter
        searchResults.forEach(entry => {
            r++;
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${r}</td>
                <td>${entry.name}
                    <div class="details-button-container">
                        <button class="btn btn-info" onclick="redirectToUniversityPage('${entry.name}')">Details</button>
                    </div>
                </td>
                <td>${entry.rank}</td>
                <td>${entry.overall_score}</td>
            `;
            tbody.appendChild(row);
        });
    } else {
        // No results found
        const noResultsRow = document.createElement('tr');
        noResultsRow.innerHTML = `<td colspan="4">No results found for "${searchTerm}".</td>`;
        tbody.appendChild(noResultsRow);
    }
}

function redirectToUniversityPage(uni) {
    let formattedUni;

    // Check for abbreviation at the end in parentheses
    const abbreviationMatch = uni.match(/\(([^)]+)\)$/);
    if (abbreviationMatch) {
        formattedUni = abbreviationMatch[1].toLowerCase();
    } else {
        // Format the university name
        formattedUni = uni.toLowerCase()
            .replace(/\s+/g, '-')  // Replace spaces with hyphens
            .replace(/[()]/g, '')  // Remove parentheses
            .replace(/,/g, '')     // Remove commas
            .replace(/-+$/, '');   // Remove any trailing hyphens
    }

    window.location.href = `/unipage/${formattedUni}`;
}

document.addEventListener('DOMContentLoaded', async function() {
    const element = document.querySelector('[data-subject="qs-general"]');
    if (element) {
        try {
            await displayEntries(element);
        } catch (error) {
            console.error('Error displaying initial entries:', error);
        }
    } else {
        console.error('No element found with data-subject="qs-general"');
    }
});
