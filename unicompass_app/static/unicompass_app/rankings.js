let rankingType = "qs";
let rankingTypeData = [];
let kzUniversitiesData = [];
let pageIndex = 0;
let totalUniversities;
let totalUniversitiesKZ;
let totalPages = 0;
let itemsPerPage;
let subject = "general";
let searchTerm = ""; // Added this variable to keep track of the search term

async function countPages() {
  const url = fetchData();
  const urlKZ = fetchKZUniversities();

  try {
    const response = await fetch(url);
    const data = await response.json();

    totalUniversities = data.total_records;
    itemsPerPage = data.items_per_page;
    temp = totalUniversities + totalUniversitiesKZ;

    while (temp % itemsPerPage != 0) {
      temp++;
    }
    totalPages = temp / itemsPerPage; // if 51 / 10

    console.log(
      `Total Records: ${totalUniversities}, Total Pages: ${totalPages}, Items Per Page: ${itemsPerPage}`
    );
    console.log(
      `Total Records KZ: ${totalUniversitiesKZ}, Total Pages: ${itemsPerPage}`
    );

    createPagination(1); // Initialize pagination with the first page
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

function fetchData() {
  if (rankingType == "qs") {
    return `/api/uni/qs/`;
  } else if (rankingType == "the") {
    return `/api/uni/the/?page=${pageIndex}&subject=${subject}`;
  } else {
    return "";
  }
}

async function fetchKZUniversities() {
  try {
    const response = await fetch("/api/kz_universities/");
    const data = await response.json();

    if (!data.data) throw new Error("No KZ data found");

    totalUniversitiesKZ = data.total_records;

    return data.data.map((entry) => ({
      name: entry.title,
    }));
  } catch (error) {
    console.error("Error fetching KZ universities data:", error);
    throw error;
  }
}

async function displayEntries() {
  try {
    const data = await getEntries();
    rankingTypeData = { rankingType, entries: data };

    kzUniversitiesData = await fetchKZUniversities();

    displayEntriesList();
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

async function getEntries() {
  const url = fetchData();

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!data.data) throw new Error("No data found");

    if (rankingType == "qs") {
      return data.data.map((entry) => ({
        rank: entry.qs_rank,
        title: entry.qs_title,
        overall_score: entry.qs_overall_score,
        nid: entry.qs_nid,
      }));
    } else if (rankingType == "the") {
      return data.data.map((entry) => ({
        rank: entry.the_rank,
        title: entry.the_title,
        overall_score: entry.the_overall_score,
        nid: entry.the_nid,
      }));
    }
  } catch (error) {
    console.error("Error fetching some universities data:", error);
    throw error;
  }
}

function createPagination(currentPage) {
  const pagination = document.querySelector(".pagination");
  pagination.innerHTML = "";

  let startPage, endPage;
  const maxButtons = 5;

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

  for (let i = startPage; i <= endPage; i++) {
    const pageButton = document.createElement("div");
    pageButton.className = "page-item";
    pageButton.innerHTML = i;

    if (i === currentPage) {
      pageButton.classList.add("active");
    }

    pageButton.addEventListener("click", () => {
      pageIndex = i - 1;
      displayEntries();
      createPagination(i);
    });

    pagination.appendChild(pageButton);
  }
}

function displayEntriesList() {
  const rbody = document.getElementById("unvListin");
  rbody.innerHTML = "";

  let r = pageIndex * itemsPerPage;
  rankingTypeData.entries.forEach((entry) => {
    r++;
    const row = document.createElement("div");
    const rtable = document.createElement("table");
    rtable.className = "University";
    row.className = "custom-button";

    // Add event listener for redirect
    row.addEventListener("click", () => {
      window.location.href = `/unipage/${entry.nid}`; // Redirect to the university page with its ID
    });

    rtable.innerHTML = `<thead>
                <tr>
                    <th>${r}</th>
                    <th>${entry.title}</th>
                    <th>${entry.rank}</th>
                    <th>${entry.overall_score}</th>
                </tr>
            </thead>`;
    row.appendChild(rtable);
    rbody.appendChild(row);
  });

  if (r == totalUniversities) {
    displayEntriesListKZ(r);
  }
}

function displayEntriesListKZ(r) {
  const rbody = document.getElementById("unvListin");
  r++;
  const separator = document.createElement("hr");
  rbody.appendChild(separator);
  kzUniversitiesData.forEach((entry) => {
    const row = document.createElement("div");
    const rtable = document.createElement("table");
    rtable.className = "University";
    row.className = "custom-button";

    // Add event listener for redirect
    row.addEventListener("click", () => {
      window.location.href = `/unipage/?id=${entry.id}`; // Redirect to the university page with its ID
    });

    rtable.innerHTML = `<thead>
                <tr>
                    <th>${r}</th>
                    <th>${entry.name}</th>
                </tr>
            </thead>`;
    row.appendChild(rtable);
    rbody.appendChild(row);
    r++;
  });
}

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await countPages();
    await displayEntries();
  } catch (error) {
    console.error("Error initializing page:", error);
  }
});

function toggleSwitch(takenRank) {
  if (takenRank != rankingType) {
    rankingType = takenRank;
    console.log(`The ranking is ${rankingType}`);
    pageIndex = 0;

    const searchInput = document.querySelector(".search-input");
    searchInput.value = "";

    countPages();
    displayEntries();
    createPagination(1);
  }
}

function leftSwitchRank() {
  subject = "general";
  const btn = document.getElementById("btn-rank");
  btn.style.left = "0px";
  leftSwitchSubject();
}

function rightSwitchRank() {
  subject = "general";
  const btn = document.getElementById("btn-rank");
  btn.style.left = "157px";
  leftSwitchSubject();
}

function leftSwitchSubject() {
  const btn = document.getElementById("btn-subject");
  btn.style.left = "0px";
  subject = "general";
  displayEntries();
}

function rightSwitchSubject() {
  const btn = document.getElementById("btn-subject");
  btn.style.left = "157px";
  if (rankingType == "the") {
    window.location.hash = "popup2";
    closeButton = document.querySelector(".close");
    if (closeButton.click) {
      leftSwitchSubject();
    }
  } else if (rankingType == "qs") {
    window.location.hash = "popup1";
    closeButton = document.querySelector(".close");
    if (closeButton.click) {
      leftSwitchSubject();
    }
  }
  document
    .querySelectorAll(
      "#popup1 button[data-subject], #popup2 button[data-subject], ul li button"
    )
    .forEach(function (button) {
      button.addEventListener("click", function () {
        subject =
          this.parentElement.getAttribute("data-subject") ||
          this.getAttribute("data-subject");
        displayEntries();
        window.location.hash = "";
        btn.style.left = "157px";
      });
    });
}

async function instantSearch() {
  searchTerm = document
    .querySelector(".search-input")
    .value.trim()
    .toLowerCase();
  const rbody = document.getElementById("unvListin");

  if (!rbody) {
    console.error('Element with id "unvListin" not found.');
    return;
  }

  rbody.innerHTML = "";

  if (searchTerm === "") {
    displayEntriesList();
    createPagination(1); // Reset pagination when search term is cleared
    return;
  }

  const searchResults = rankingTypeData.entries.filter((entry) =>
    entry.name.toLowerCase().includes(searchTerm)
  );

  const searchResultsKZ = kzUniversitiesData.filter((entry) =>
    entry.name.toLowerCase().includes(searchTerm)
  );

  let filteredUniversities = searchResults.length + searchResultsKZ.length;
  totalPages = Math.ceil(filteredUniversities / itemsPerPage);

  createPagination(1); // Update pagination based on the search results

  let r = 0;

  if (searchResults.length > 0) {
    searchResults.forEach((entry) => {
      r++;
      const row = document.createElement("div");
      const rtable = document.createElement("table");
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
    searchResultsKZ.forEach((entry) => {
      r++;
      const row = document.createElement("div");
      const rtable = document.createElement("table");
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
  }

  const separator = document.createElement("hr");
  rbody.appendChild(separator);
}

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-input");

  if (searchInput) {
    searchInput.addEventListener("input", instantSearch);
  } else {
    console.error('Element with class "search-input" not found.');
  }
});
