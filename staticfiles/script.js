
function showTab() {
    const sAuthorRankElement = document.getElementById("sAuthorRank");
    const showAuthorTab = document.getElementById("showAuthorTab");
    const authorRankTitle = document.getElementById("authorRankTitle");
    const searchFormElement = document.getElementById("searchForm");

    sAuthorRankElement.classList.add("slide-in");
    authorRankTitle.classList.add("slide-in");

    const originTitle = document.getElementById("originTitle");
    const getStarted = document.getElementById("getStarted");
    const introductionContent = document.getElementById("introductionContent");


    sAuthorRankElement.style.display = 'block';
    searchFormElement.style.display = 'block';

    authorRankTitle.style.display = 'block';
    showAuthorTab.style.display = 'none';
    originTitle.style.display = 'none';
    introductionContent.style.display = 'none';
    getStarted.style.display = 'none';
}


function addSearchAuthorQuery() {
    const searchQueryAuthor = document.getElementById("searchQueryAuthor").value;
    const exprInput = document.querySelector("input[name='exprAuthor']");
    exprInput.value = searchQueryAuthor;
}


function fadeElementsInSequence(elements) {
    const delay = 700; // Delay between fading in each element (in milliseconds)

    elements.forEach(function (elementId, index) {
        setTimeout(function () {
            const element = document.getElementById(elementId);
            element.classList.add("fade-in");
            element.style.display = "block";
        }, index * delay);
    });
}

const elementsToFadeIn = ["introductionContent", "getStarted", "searchContainer"];
fadeElementsInSequence(elementsToFadeIn);