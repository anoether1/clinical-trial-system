const OriginTitle = document.getElementById("OriginTitle");

function showTab(tab) {
    const sAuthorRank = document.getElementById("sAuthorRank");
    const showAuthorTab = document.getElementById("showAuthorTab");
    const authorRankTitle = document.getElementById("authorRankTitle");
    const introduction = document.getElementById("introduction");

    introduction.style.display = 'none';
    sAuthorRank.style.display = 'block';
    authorRankTitle.style.display = 'block';
    showAuthorTab.style.display = 'none';
    OriginTitle.style.display = 'none';
}


function addSearchAuthorQuery() {
    const searchQueryAuthor = document.getElementById("searchQueryAuthor").value;
    const exprInput = document.querySelector("input[name='exprAuthor']");
    const queryInputOnly = document.querySelector("input[name='queryInputOnly']");
    exprInput.value = "(AREA[LocationCountry]Taiwan OR AREA[LocationCity]Taipei) AND " + searchQueryAuthor;
    queryInputOnly.value = searchQueryAuthor;
}