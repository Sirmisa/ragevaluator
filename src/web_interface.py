from playwright.sync_api import sync_playwright
from typing import Optional

class WebInterface:
    """Class to handle web interactions with the RAG system using Playwright."""
    
    def __init__(self, url: str):
        """
        Initialize the web interface.
        
        Args:
            url (str): The URL of the RAG system's web interface
        """
        self.url = url
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self) -> None:
        """Start the browser and navigate to the RAG system page."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto(self.url)

    def send_query(self, query: str, input_selector: str, submit_selector: str) -> Optional[str]:
        """
        Send a query to the RAG system and get the response.
        
        Args:
            query (str): The question to ask
            input_selector (str): CSS selector for the input field
            submit_selector (str): CSS selector for the submit button
            
        Returns:
            Optional[str]: The response from the RAG system, or None if there's an error
        """
        try:
            # Clear any existing input
            self.page.fill(input_selector, "")
            
            # Type the query
            self.page.fill(input_selector, query)
            
            # Click the submit button
            self.page.click(submit_selector)
            
            # Wait for response (you might need to adjust the selector and timing)
            response_selector = ".response-class"  # Adjust based on actual webpage
            self.page.wait_for_selector(response_selector)
            
            # Get the response text
            response = self.page.text_content(response_selector)
            return response.strip() if response else None
            
        except Exception as e:
            print(f"Error sending query: {str(e)}")
            return None

    def close(self) -> None:
        """Close the browser and cleanup resources."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
