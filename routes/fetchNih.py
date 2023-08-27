from fastapi import APIRouter, status, Query

from typing import Dict, Union

from fastapi.responses import JSONResponse

from modules.search_by_rank import SearchNih

responses: Dict[Union[int, str], Dict[str, str]] = {
    400: {"description": "You missed some parameters or paramters was not corrected"},
    403: {"description": "The data does not exists"},
    500: {"description": "Unknown error"},
}
router = APIRouter()


@router.get(
    "/api/general",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    responses=responses,
    tags=["Search"],
    summary="Search all research",
)
async def search_all_research(
    searchQuery: str = Query(
        description="Input search query and get nih info (Taiwan only)",
        example="stroke",
    ),
):
    """
    Search All
    """
    fields = 'NCTId,BriefTitle,Condition,CentralContactName,CentralContactEMail,CentralContactPhone,CentralContactPhoneExt,CentralContactRole,'
    fields += 'ResponsiblePartyInvestigatorFullName,ResponsiblePartyInvestigatorTitle,ResponsiblePartyInvestigatorAffiliation,ResponsiblePartyOldNameTitle,ResponsiblePartyOldOrganization,'
    fields += 'OverallOfficialName'
    searchQuery = f'(AREA[LocationCountry]Taiwan OR AREA[LocationCity]Taipei) AND {searchQuery}'
    search_nih = SearchNih(searchQuery, fields)
    # get total amount of data
    total = search_nih.search_by_rank(1, 1).get("NStudiesFound", None)
    if not total:
        return JSONResponse({"message": "No study found"}, status_code=400)
    output = search_nih.search_all_researchs(total)
    return {"data": output, "total": len(output)}


@router.get(
    "/api/rank",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    responses=responses,
    tags=["Search"],
    summary="Search by rank",
)
def searchByRank(
    searchQuery: str = Query(
        description="Input search query and get nih info (Taiwan only)",
        example="stroke",
    ),
):
    """
    Search user by rank
    """
    fields = "CentralContactName,CentralContactRole,CentralContactEMail,CentralContactPhone,CentralContactPhoneExt,"
    fields += "LocationContactEMail,LocationCity,LocationContactName,LocationContactPhone,LocationContactPhoneExt,LocationContactRole,LocationFacility,"
    fields += "OverallOfficialName"
    searchQuery = f'(AREA[LocationCountry]Taiwan OR AREA[LocationCity]Taipei) AND {searchQuery}'
    search_nih = SearchNih(searchQuery, fields)
    # get total amount of data
    total = search_nih.search_by_rank(1, 1).get("NStudiesFound", None)
    if not total:
        return JSONResponse({"message": "No study found"}, status_code=400)

    # calculate
    calcaulate_result = search_nih.search_author_info(total)

    result = search_nih.get_calculate_author(calcaulate_result)

    # Remove dirty data
    # recover the following three lines
    result.pop("C c w", None)
    result.pop("Study contact", None)
    # result.pop("National taiwan university hospital", None)
    sorted_data = sorted(
        result.items(), key=lambda x: x[1]["count"], reverse=True)
    return {"data": sorted_data, "total": total}
