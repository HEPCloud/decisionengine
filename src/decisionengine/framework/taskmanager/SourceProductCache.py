# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0


class SourceProductCache:
    def __init__(self, expected_products, logger):
        self.expected_source_products = expected_products
        self.sources_have_run_once = False
        self.data = {}
        self.logger = logger
        self.logger.debug(f"Expected source products {self.expected_source_products}")

    def update(self, new_data):
        # FIXME: Should we update the cache every time we call update? Probably.
        if self.sources_have_run_once:
            return new_data

        self.data.update(**new_data)
        missing_products = self.expected_source_products - set(self.data.keys())
        if missing_products:
            self.logger.info(f"Waiting on more data (missing {missing_products})")
            return None

        self.logger.info("All sources have executed at least once")
        self.sources_have_run_once = True
        # Return the whole cache the first time it is completely full
        return self.data
