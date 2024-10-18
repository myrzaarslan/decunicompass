let rankingType = "qs";
let rankingTypeData = [];
let pageIndex = 0;
let totalUniversities;
let totalPages = 0;
let itemsPerPage = 10; // Set default items per page
let subject = "general";
let searchTerm = "";
let currentPage = 0;

// Map for THE subjects
const subjectFieldsMap_THE = {
  arts_and_humanities: "the_rank_arts",
  engineering: "the_rank_eng",
  business_and_economics: "the_rank_bus",
  law: "the_rank_law",
  clinical_and_health: "the_rank_clin",
  life_sciences: "the_rank_life",
  computer_science: "the_rank_comp",
  physical_sciences: "the_rank_phys",
  education: "the_rank_edu",
  psychology: "the_rank_phych",
};

// Map for QS subjects
const subjectFieldsMap_QS = {
  arts_and_humanities: "qs_rank_arts_humanities",
  linguistics: "qs_rank_linguistics",
  music: "qs_rank_music",
  theology_divinity_religious_studies: "qs_rank_theology",
  archaeology: "qs_rank_archaeology",
  architecture_and_built_environment: "qs_rank_architecture",
  art_and_design: "qs_rank_art_design",
  classics_and_ancient_history: "qs_rank_classics",
  english_language_and_literature: "qs_rank_english",
  history: "qs_rank_history",
  art_history: "qs_rank_art_history",
  modern_languages: "qs_rank_modern_languages",
  performing_arts: "qs_rank_performing_arts",
  philosophy: "qs_rank_philosophy",
  engineering_and_technology: "qs_rank_eng_tech",
  engineering_chemical: "qs_rank_chem_eng",
  engineering_civil_and_structural: "qs_rank_civil_eng",
  computer_science_and_information_systems: "qs_rank_comp_sci",
  data_science_and_artificial_intelligence: "qs_rank_data_sci",
  engineering_electrical_and_electronic: "qs_rank_elec_eng",
  engineering_petroleum: "qs_rank_pet_eng",
  engineering_mechanical: "qs_rank_mech_eng",
  engineering_mineral_and_mining: "qs_rank_mining_eng",
  natural_sciences: "qs_rank_nat_sci",
  chemistry: "qs_rank_chemistry",
  earth_and_marine_sciences: "qs_rank_earth_marine_sci",
  environmental_sciences: "qs_rank_env_sci",
  geography: "qs_rank_geography",
  geology: "qs_rank_geology",
  geophysics: "qs_rank_geophysics",
  materials_sciences: "qs_rank_materials_sci",
  mathematics: "qs_rank_math",
  physics_and_astronomy: "qs_rank_physics_astronomy",
  life_sciences_and_medicine: "qs_rank_life_sci",
  agriculture_and_forestry: "qs_rank_agriculture",
  anatomy_and_physiology: "qs_rank_anatomy",
  biological_sciences: "qs_rank_bio_sci",
  dentistry: "qs_rank_dentistry",
  medicine: "qs_rank_medicine",
  pharmacy: "qs_rank_pharmacy",
  nursing: "qs_rank_nursing",
  psychology: "qs_rank_psychology",
  veterinary_science: "qs_rank_vet_sci",
};

function fetchData() {
  return `/api/uni/?items_per_page=50`;
}

async function getEntries() {
  const url = fetchData();

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (!data.data) throw new Error("No data found");

    return data.data.map((entry) => {
      // Создаем объект, который содержит общую информацию о университете
      let universityData = {
        id: entry.id,
        rank_qs: entry.qs_rank,
        rank_the: entry.the_rank,
        title_qs: entry.qs_title,
        title_the: entry.the_title,
        title_kz: entry.kz_title,
        overall_score_qs: entry.qs_overall_score,
        overall_score_the: entry.the_overall_score,
        nid_qs: entry.qs_nid,
        nid_the: entry.the_nid,

        arts_and_humanities: entry.the_rank_arts,
        engineering: entry.the_rank_eng,
        business_and_economics: entry.the_rank_bus,
        law: entry.the_rank_law,
        clinical_and_health: entry.the_rank_clin,
        life_sciences: entry.the_rank_life,
        computer_science: entry.the_rank_comp,
        physical_sciences: entry.the_rank_phys,
        education: entry.the_rank_edu,
        psychology: entry.the_rank_phych,
      };

      // Add THE subject-specific rankings
      for (const rankField of Object.values(subjectFieldsMap_QS)) {
        if (entry[rankField]) {
          universityData[rankField] = entry[rankField];
        }
      }

      // Add QS subject-specific rankings
      for (const rankField of Object.values(subjectFieldsMap_THE)) {
        if (entry[rankField]) {
          universityData[rankField] = entry[rankField];
        }
      }

      return universityData;
    });
  } catch (error) {
    console.error("Error fetching some universities data:", error);
    throw error;
  }
}

async function displayEntries() {
  try {
    const data = await getEntries();
    rankingTypeData = { entries: data };
    displayEntriesList();
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

function displayEntriesList() {
  let table = document.getElementsByClassName("Dimash_Listing")[0];
  table.innerHTML = "";

  let filteredUniversities = filterAndSortUniversities();
  updatePagination(filteredUniversities);

  let start = pageIndex * itemsPerPage;
  let end = start + itemsPerPage;

  for (let i = start; i < end && i < filteredUniversities.length; i++) {
    const entry = filteredUniversities[i]; // Contains university data
    const row = document.createElement("tr");

    let title, rank, overall_score;

    if (rankingType === "the" && entry.title_the) {
      title = entry.title_the;
      rank = entry.rank_the;
      overall_score = entry.overall_score_the;
    } else if (rankingType === "qs" && entry.title_qs) {
      title = entry.title_qs;
      rank = entry.rank_qs;
      overall_score = entry.overall_score_qs;
    } else {
      title = entry.title_kz;
      rank = "--";
      overall_score = "--";
    }

    const cell1 = document.createElement("th");
    cell1.textContent = i + 1;

    const cell2 = document.createElement("th");
    cell2.textContent = title;

    const cell3 = document.createElement("th");
    cell3.textContent = rank;

    const cell4 = document.createElement("th");
    cell4.textContent = overall_score;

    // Add click event to row for redirection
    row.addEventListener("click", () => {
      window.location.href = `/unipage/${entry.id}`; // Redirect with university ID
    });

    row.appendChild(cell1);
    row.appendChild(cell2);
    row.appendChild(cell3);
    row.appendChild(cell4);
    table.appendChild(row);
  }
  table.className = "Dimash_Listing";
}

function subjectIsChanged(new_subject) {
  subject = new_subject;
  pageIndex = 0;
  window.location.hash = "";
  const btn = document.getElementById("btn-subject");
  btn.style.left = "157px";
  displayEntriesList();
}

document.addEventListener("DOMContentLoaded", async function () {
  try {
    await displayEntries();
  } catch (error) {
    console.error("Error initializing page:", error);
  }
});

function filterAndSortUniversities() {
  let filteredUniversities = [];

  if (subject === "general") {
    if (rankingType === "qs") {
      let rankedUniversities = rankingTypeData.entries.filter(
        (entry) => entry.rank_qs
      );
      let unrankedUniversities = rankingTypeData.entries.filter(
        (entry) => !entry.rank_qs && !entry.rank_the
      );

      filteredUniversities = rankedUniversities.concat(unrankedUniversities);
    } else if (rankingType === "the") {
      let rankedUniversities = rankingTypeData.entries.filter(
        (entry) => entry.rank_the
      );
      let unrankedUniversities = rankingTypeData.entries.filter(
        (entry) => !entry.rank_qs && !entry.rank_the
      );

      filteredUniversities = rankedUniversities.concat(unrankedUniversities);
    }
  } else {
    let subjectField;

    if (rankingType === "qs") {
      subjectField = subjectFieldsMap_QS[subject];
      filteredUniversities = rankingTypeData.entries.filter(
        (entry) => entry[subjectField]
      );
    }
    if (rankingType === "the") {
      subjectField = subjectFieldsMap_THE[subject];
      filteredUniversities = rankingTypeData.entries.filter(
        (entry) => entry[subjectField]
      );
    }
  }

  return filteredUniversities;
}

function updatePagination(filteredUniversities) {
  totalPages = Math.ceil(filteredUniversities.length / itemsPerPage);
  createPagination(pageIndex + 1); // Pass current page index correctly
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
      displayEntriesList();
      createPagination(i);
    });

    pagination.appendChild(pageButton);
  }
}

// BUTTONS
function toggleSwitch(takenRank) {
  if (takenRank != rankingType) {
    rankingType = takenRank;
    console.log(`The ranking is ${rankingType}`);
    pageIndex = 0;

    const searchInput = document.querySelector(".search-input");
    searchInput.value = "";

    // countPages();
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
    if (subject === "general") {
      leftSwitchSubject();
    }
  } else if (rankingType == "qs") {
    window.location.hash = "popup1";
    closeButton = document.querySelector(".close");
    if (closeButton.click) {
      leftSwitchSubject();
    }
  }
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

  rbody.innerHTML = ""; // Clear previous results

  // First, apply subject filter
  let filteredUniversities = filterAndSortUniversities();

  // If there is a search term, further filter the universities
  if (searchTerm != "") {
    filteredUniversities = filteredUniversities.filter(
      (entry) =>
        (entry.title_qs && entry.title_qs.toLowerCase().includes(searchTerm)) ||
        (entry.title_the &&
          entry.title_the.toLowerCase().includes(searchTerm)) ||
        (entry.title_kz && entry.title_kz.toLowerCase().includes(searchTerm))
    );
  } else {
    // If no results are found, display a message
    rbody.innerHTML = "<div>No results found.</div>";
  }

  // Update pagination based on the search results
  totalPages = Math.ceil(filteredUniversities.length / itemsPerPage);
  createPagination(1); // Update pagination based on the search results
}

document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.querySelector(".search-input");

  if (searchInput) {
    searchInput.addEventListener("input", instantSearch);
  } else {
    console.error('Element with class "search-input" not found.');
  }
});
