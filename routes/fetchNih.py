from fastapi import APIRouter, status, Query

from typing import Dict, Union

from modules.search_by_rank import SearchNih

responses: Dict[Union[int, str], Dict[str, str]] = {
    400: {"description": "You missed some parameters or paramters was not corrected"},
    403: {"description": "The data does not exists"},
    500: {"description": "Unknown error"},
}
router = APIRouter()


@router.get(
    "/api/rank",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    responses=responses,
    tags=["Search"],
    summary="Search by rank",
)
async def searchByRank(
    searchQuery: str = Query(
        description="Input search query and get nih info",
        example="(AREA[LocationCity]Taiwan OR AREA[LocationCity]Taipei) AND stroke",
    ),
):
    """
    Search user by rank
    """
    fields = "CentralContactName,CentralContactRole,CentralContactEMail,CentralContactPhone,CentralContactPhoneExt,"
    fields += "LocationContactEMail,LocationCity,LocationContactName,LocationContactPhone,LocationContactPhoneExt,LocationContactRole,LocationFacility,"
    fields += "OverallOfficialName"

    search_nih = SearchNih(searchQuery, fields)
    # get total amount of data
    total = search_nih.search_by_rank(1, 1)["NStudiesFound"]

    # calculate
    calcaulate_result = search_nih.search_author_info(150)
    # calcaulate_result = search_nih.search_author_info(total)

    result = search_nih.get_calculate_author(calcaulate_result)

    # Remove dirty data
    # recover the following three lines
    result.pop("C c w", None)
    result.pop("Study contact", None)
    result.pop("National taiwan university hospital", None)
    sorted_data = sorted(result.items(), key=lambda x: x[1]["count"], reverse=True)
    return sorted_data
