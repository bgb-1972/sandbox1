from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

class LexCoPropertySearch:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "https://www.lex-co.com/PropSearch/#/property"

    def open_search_page(self):
        self.driver.get(self.base_url)
        time.sleep(3)  # Wait for page to load

    def search_by_owner(self, owner_name):
        self.open_search_page()
        # Wait for the owner name input to be available
        time.sleep(2)
        # Find the owner name input (update selector as needed)
        owner_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Owner Name']")
        owner_input.clear()
        owner_input.send_keys(owner_name)
        owner_input.send_keys(Keys.RETURN)
        time.sleep(5)  # Wait for results
        return self.get_results()

    def get_results(self):
        # This method should be updated to parse the results table or list
        # Example: get all rows in the results table
        results = []
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                results.append([col.text for col in cols])
        except Exception as e:
            print(f"Error getting results: {e}")
        return results

    def close(self):
        self.driver.quit()


def main():
    """Simple CLI entrypoint to search properties by owner name.

    Usage: python lexco_property_search.py --owner "Owner Name"
    If no owner is provided, prompts interactively.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Search LexCo properties by owner name")
    parser.add_argument("--owner", "-o", help="Owner name to search for", required=False)
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode (default)")
    parser.add_argument("--no-headless", dest="headless", action="store_false", help="Run browser with UI")
    parser.set_defaults(headless=True)
    args = parser.parse_args()

    owner = args.owner
    if not owner:
        try:
            owner = input("Enter owner name to search: ")
        except EOFError:
            print("No owner name provided; exiting.")
            return

    searcher = None
    try:
        searcher = LexCoPropertySearch(headless=args.headless)
        results = searcher.search_by_owner(owner)
        if not results:
            print("No results found or unable to parse results.")
        else:
            print(f"Found {len(results)} result(s):")
            for i, row in enumerate(results, start=1):
                print(f"{i}: {row}")
    except Exception as e:
        print(f"Error during search: {e}")
    finally:
        if searcher:
            try:
                searcher.close()
            except Exception:
                pass


if __name__ == "__main__":
    main()
