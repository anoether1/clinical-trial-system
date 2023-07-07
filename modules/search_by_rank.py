import requests
from models.nih_study_fields import NihInfoWithCountType, StudyFieldsResponseType, NihInfoType
from typing import Dict
from concurrent.futures import ThreadPoolExecutor


class SearchNih:
    def __init__(self, search_query: str, fields: str):
        self.searchQuery = search_query
        self.fields = fields

    def filter_title(self, name: str):
        symbol_to_filter = [",", ".", ";", "/"]
        text_to_filter = ["ScD", "MD", "PhD", "MS", "MSc", "PHD", "Dr", "MSN",
                          "PT", "Doctor", "Master", "Bachelor"]
        for symbol in symbol_to_filter:
            name = name.replace(symbol, "")

        for title in text_to_filter:
            name = name.replace(title, "")
        return name.strip().capitalize()

    def search_by_rank(self, min_rnk: int, max_rnk: int) -> StudyFieldsResponseType:
        params = {
            "expr": self.searchQuery,
            "fields": self.fields,
            "fmt": "json",
            "min_rnk": min_rnk,
            "max_rnk": max_rnk,
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
                        contact_name = self.filter_title(name)
                        calculate_result[contact_name] = calculate_result.get(
                            contact_name, {})
                        calculate_result[contact_name]["ContactEMail"] = (
                            calculate_result[contact_name]
                            .get("ContactEMail", set([]))
                            .union(study_field["CentralContactEMail"])
                        )

                        calculate_result[contact_name]["ContactPhone"] = (
                            calculate_result[contact_name]
                            .get("ContactPhone", set([]))
                            .union(study_field["CentralContactPhone"])
                        )

                        calculate_result[contact_name]["ContactPhoneExt"] = (
                            calculate_result[contact_name]
                            .get("ContactPhoneExt", set([]))
                            .union(study_field["CentralContactPhoneExt"])
                        )

                elif len(location_contact_name) > 0:
                    for name in location_contact_name:
                        contact_name = self.filter_title(name)

                        calculate_result[contact_name] = calculate_result.get(
                            contact_name, {})

                        calculate_result[contact_name]["ContactEMail"] = (
                            calculate_result[contact_name]
                            .get("ContactEMail", set([]))
                            .union(study_field["LocationContactEMail"])
                        )

                        calculate_result[contact_name]["ContactPhone"] = (
                            calculate_result[contact_name]
                            .get("ContactPhone", set([]))
                            .union(study_field["LocationContactPhone"])
                        )

                        calculate_result[contact_name]["ContactPhoneExt"] = (
                            calculate_result[contact_name]
                            .get("ContactPhoneExt", set([]))
                            .union(study_field["LocationContactPhoneExt"])
                        )

        return calculate_result

    def get_calculate_author(self, search_author_result: Dict[str, NihInfoType]) -> Dict[str, NihInfoWithCountType]:

        results = {}
        # Set max workers to 48
        with ThreadPoolExecutor(max_workers=48) as executor:

            # 提交任務給執行緒池
            threads = [executor.submit(self.process_author, author)
                       for author in search_author_result.keys()]

            # 等待所有任務完成並獲取結果
            for thread in threads:
                # this will return author, count
                author, count = thread.result()
                results[author] = count
        # 更新原始結果
        tmp = search_author_result.copy()
        for author, count in results.items():
            tmp[author]["count"] = count  # type:ignore
        return tmp  # type:ignore

    def process_author(self, author: str):
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
