class URLs:
    """
    This class contains the urls of all the routes of the trefle API
    """
    def __init__(self, version='v1'):
        self._version = version
        self._base_url = f"https://trefle.io/{self._version}/"
        # Plants hierarchy routes
        self._kingdoms = "kingdoms"  # kingdoms
        self._subkingdoms = "subkingdoms"  # subkingdoms
        self._divisions = "divisions"  # divisions
        self._division_classes = "division_classes"  # division classes
        self._division_orders = "division_orders"  # division orders
        self._families = "families"  # families
        self._genus = "genus"  # genus
        self._species = "species"  # species
        self._plants = "plants"  # plants
        # search routes
        self._search_plants = self._plants + "/search"
        self._search_species = self._species + "search"
        self._plants_by_distributions = "distributions/{zone_id}/plants"
        self._plants_by_genus = self._genus + "{genus_id}/plants"
        # Plants report routes
        self._report_plants = self._plants + "/{id}/report"
        self._report_species = self._species + "/{id}/report"
        # Distributions zones routes
        self._distributions = "distributions"
        self._distribution_by_id = self._distributions + "/{id}"
        # Authentication routes
        self._client_side_token = "auth/claim"
        # Corrections routes
        self._corrections = "corrections"
        self._correction_by_id = self._corrections + "/{id}"
        self._submit_correction = self._corrections + "/species/{record_id}"

        self._urls = [url for url in self.__dir__() if '_' not in url[:2] and
                      'url' in url]

    def __iter__(self):
        for url in self._urls:
            yield url

    def __len__(self):
        return len(self._urls)

    def base_url(self):
        return self._base_url

    def kingdoms_url(self):
        return self._base_url + self._kingdoms

    def subkingdoms_url(self):
        return self._base_url + self._subkingdoms

    def divisions_url(self):
        return self._base_url + self._divisions

    def division_classes_url(self):
        return self._base_url + self._division_classes

    def division_orders_url(self):
        return self._base_url + self._division_orders

    def families_url(self):
        return self._base_url + self._families

    def genus_url(self):
        return self._base_url + self._genus

    def species_url(self):
        return self._base_url + self._species

    def plants_url(self):
        return self._base_url + self._plants

    def search_plants_url(self):
        return self._base_url + self._search_plants

    def search_species_url(self):
        return self._base_url + self._search_species

    def plants_by_distributions_url(self):
        """
        Returns a format-able string
        `base_url/distributions/{zone_id}/plants`\n
        """
        return self._base_url + self._plants_by_distributions

    def plants_by_genus_url(self):
        """
        Returns a format-able string
        `base_url/{genus_id}/plants`\n
        """
        return self._base_url + self._plants_by_genus

    def report_plants_url(self):
        """
        Returns a format-able string
        `base_url/plants_url/{id}/report`\n
        """
        return self._base_url + self._report_plants

    def report_species_url(self):
        """
        Returns a format-able string
        `base_url/species_url/{id}/report`\n
        """
        return self._base_url + self._report_species

    def distributions_url(self):
        return self._base_url + self._distributions

    def distribution_by_id_url(self):
        """
        Returns a format-able string
        `base_url/distributions_url/{id}`\n
        """
        return self._base_url + self._distribution_by_id

    def client_side_token_url(self):
        return self._base_url + self._client_side_token

    def corrections_url(self):
        return self._base_url + self._corrections

    def corrections_by_id_url(self):
        """
        Returns a format-able string
        `base_url/corrections_url/{id}`\n
        """
        return self._base_url + self._correction_by_id

    def submit_correction_url(self):
        """
        Returns a format-able string
        `base_url/corrections_url/species/{record_id}`\n
        """
        return self._base_url + self._submit_correction


settings = {
    "url": "https://trefle.io/{}",
    "endpoints": {
        "base": {
            "kingdoms": "_",
            "subkingdoms": "_",
            "divisions": "_",
            "division_classes": "_",
            "division_orders": "_",
            "families": "_",
            "genus": "_",
            "species": "_",
            "plants": "_"
        },
        "search": {
            "base": {
                "plants": "_",
                "species": "_",
            },
            "by_key": {
                "plants_by_distributions": "distributions/{zone_id}/plants",
                "plants_by_genus": ""
            }
        }
    }
}