from typing import TypedDict, List, Set

class NihInfoWithCountType(TypedDict):
    ContactEMail: Set[str]
    ContactPhone: Set[str]
    ContactPhoneExt: Set[str]
    count: int


class NihInfoType(TypedDict):
    ContactEMail: Set[str]
    ContactPhone: Set[str]
    ContactPhoneExt: Set[str]


class StudyFieldsType(TypedDict):
    Rank: int
    CentralContactName: List[str]
    CentralContactRole: List[str]
    CentralContactEMail: List[str]
    CentralContactPhone: List[str]
    CentralContactPhoneExt: List[str]
    LocationContactEMail: List[str]
    LocationCity: List[str]
    LocationContactName: List[str]
    LocationContactPhone: List[str]
    LocationContactPhoneExt: List[str]
    LocationContactRole: List[str]
    LocationFacility: List[str]


class StudyFieldsResponseType(TypedDict):
    APIVrs: str
    DataVrs: str
    Expression: str
    NStudiesAvail: int
    NStudiesFound: int
    MinRank: int
    MaxRank: int
    NStudiesReturned: int
    FieldList: List[str]
    StudyFields: List[StudyFieldsType]


class NihStudyFieldType(TypedDict):
    StudyFieldsResponse: StudyFieldsResponseType
