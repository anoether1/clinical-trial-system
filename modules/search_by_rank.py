import requests
from models.nih_study_fields import NihInfoWithCountType, StudyFieldsResponseType, NihInfoType
from multiprocessing.dummy import Pool
from typing import Dict
from multiprocessing import Pool


class SearchNih:
    def __init__(self, searchQuery: str, fields: str):
        self.searchQuery = searchQuery
        self.fields = fields

    def search_by_rank(self, min_rnk: int, maxRank: int) -> StudyFieldsResponseType:
        params = {
            "expr": self.searchQuery,
            "fields": self.fields,
            "fmt": "json",
            "min_rnk": min_rnk,
            "max_rnk": maxRank,
        }
        url = "https://clinicaltrials.gov/api/query/study_fields?"
        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        return response.json()["StudyFieldsResponse"]

    def search_author_info(self, total: int) -> Dict[str, NihInfoType]:
        calculate_result = {}

        while total > 0:
            if total >= 1000:
                result = self.search_by_rank(total - 1000, total)
                total -= 1000
            else:
                result = self.search_by_rank(1, total)
                total -= total

            for study_field in result["StudyFields"]:
                central_contact_name = set(study_field["CentralContactName"])
                location_contact_name = set(study_field["LocationContactName"])
                # calculate central contact name
                if len(central_contact_name) > 0:
                    for name in central_contact_name:
                        calculate_result[name] = calculate_result.get(name, {})
                        calculate_result[name]["ContactEMail"] = (
                            calculate_result[name]
                            .get("ContactEMail", set([]))
                            .union(study_field["CentralContactEMail"])
                        )

                        calculate_result[name]["ContactPhone"] = (
                            calculate_result[name]
                            .get("ContactPhone", set([]))
                            .union(study_field["CentralContactPhone"])
                        )

                        calculate_result[name]["ContactPhoneExt"] = (
                            calculate_result[name]
                            .get("ContactPhoneExt", set([]))
                            .union(study_field["CentralContactPhoneExt"])
                        )

                elif len(location_contact_name) > 0:
                    for name in location_contact_name:
                        calculate_result[name] = calculate_result.get(name, {})

                        calculate_result[name]["ContactEMail"] = (
                            calculate_result[name]
                            .get("ContactEMail", set([]))
                            .union(study_field["LocationContactEMail"])
                        )

                        calculate_result[name]["ContactPhone"] = (
                            calculate_result[name]
                            .get("ContactPhone", set([]))
                            .union(study_field["LocationContactPhone"])
                        )

                        calculate_result[name]["ContactPhoneExt"] = (
                            calculate_result[name]
                            .get("ContactPhoneExt", set([]))
                            .union(study_field["LocationContactPhoneExt"])
                        )

        return calculate_result

    def get_calculate_author(self, search_author_result: Dict[str, NihInfoType]) -> Dict[str, NihInfoWithCountType]:
        results = Pool(4).map(self.process_author, search_author_result.keys())
        tmp = search_author_result.copy()
        for data in results:
            tmp[data[0]]["count"] = data[1] # type: ignore
        return tmp # type: ignore

    def process_author(self, author):
        params = {
            "expr": f"{self.searchQuery} AND {author}",
            "fields": "",
            "fmt": "json",
            "min_rnk": 1,
            "max_rnk": 15,
        }
        url = "https://clinicaltrials.gov/api/query/study_fields?"
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return (author, response.json()["StudyFieldsResponse"]["NStudiesReturned"])
