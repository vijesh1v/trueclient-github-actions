#!/usr/bin/env python3
"""
TrueClient Script Executor
Converts and runs TrueClient scripts using Selenium WebDriver
"""
import os
import time
import json
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class TrueClientExecutor:
    def __init__(self, headless=True):
        self.setup_driver(headless)
        self.results = {
            "transactions": {},
            "steps": [],
            "start_time": datetime.now().isoformat(),
            "status": "running"
        }
    
    def setup_driver(self, headless=True):
        """Setup Chrome WebDriver with options"""
        chrome_options = webdriver.ChromeOptions()
        
        if headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
    
    def log_step(self, step_name, status="success", error_message=None):
        """Log step execution"""
        step_result = {
            "step": step_name,
            "status": status,
            "timestamp": datetime.now().isoformat()
        }
        
        if error_message:
            step_result["error"] = error_message
        
        self.results["steps"].append(step_result)
        print(f"📝 {step_name}: {status}")
    
    def start_transaction(self, transaction_name):
        """Start transaction timing"""
        self.current_transaction = transaction_name
        self.transaction_start_time = time.time()
        print(f"🟢 START TRANSACTION: {transaction_name}")
    
    def end_transaction(self, transaction_name, status=0):
        """End transaction and record timing"""
        if hasattr(self, 'transaction_start_time'):
            duration = time.time() - self.transaction_start_time
            self.results["transactions"][transaction_name] = {
                "status": "pass" if status == 0 else "fail",
                "duration_seconds": round(duration, 2),
                "end_time": datetime.now().isoformat()
            }
            print(f"🔴 END TRANSACTION: {transaction_name} - {duration:.2f}s")
    
    def navigate_to(self, url):
        """Navigate to URL - TrueClient step 1"""
        try:
            self.driver.get(url)
            self.log_step(f"Navigate to {url}")
            return True
        except Exception as e:
            self.log_step(f"Navigate to {url}", "error", str(e))
            return False
    
    def click_element(self, element_description, selector):
        """Click on element - Generic click method"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            element.click()
            self.log_step(f"Click {element_description}")
            return True
        except Exception as e:
            self.log_step(f"Click {element_description}", "error", str(e))
            return False
    
    def type_text(self, element_description, selector, text):
        """Type text into element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
            element.clear()
            element.send_keys(text)
            self.log_step(f"Type {text} in {element_description}")
            return True
        except Exception as e:
            self.log_step(f"Type in {element_description}", "error", str(e))
            return False
    
    def execute_petstore_script(self):
        """Execute your specific TrueClient script for PetStore"""
        print("🚀 Starting TrueClient Script Execution - PetStore")
        
        try:
            # Transaction 1: Navigate to PetStore
            self.start_transaction("Transaction_1")
            self.navigate_to("https://petstore.octoperf.com/actions/Catalog.action")
            self.end_transaction("Transaction_1", 0)
            
            # Transaction 2: Click Sign In
            self.start_transaction("Transaction_2")
            self.click_element("Sign In link", "//a[contains(text(), 'Sign In')]")
            self.end_transaction("Transaction_2", 0)
            
            # Transaction 3: Login Process
            self.start_transaction("Transaction_3")
            # Username
            self.click_element("username textbox", "//input[@name='username']")
            self.type_text("username textbox", "//input[@name='username']", "vv1234")
            # Password
            self.click_element("password field", "//input[@name='password']")
            self.type_text("password field", "//input[@name='password']", "password123")  # Replace with actual password
            # Login button
            self.click_element("Login button", "//input[@name='signon']")
            self.end_transaction("Transaction_3", 0)
            
            # Transaction 4: Click Fish Image
            self.start_transaction("Transaction_4")
            self.click_element("Fish image", "//area[@alt='Fish']")
            self.end_transaction("Transaction_4", 0)
            
            # Click specific fish product
            self.click_element("FI SW 01 link", "//a[contains(text(), 'FI-SW-01')]")
            
            # Transaction 5: Add to Cart
            self.start_transaction("Transaction_5")
            self.click_element("Add to Cart", "//a[contains(text(), 'Add to Cart')]")
            self.end_transaction("Transaction_5", 0)
            
            # Update quantity
            self.type_text("quantity field", "//input[@name='quantity']", "2")
            
            # Transaction 6: Proceed to Checkout
            self.start_transaction("Transaction_6")
            self.click_element("Proceed to Checkout", "//a[contains(text(), 'Proceed to Checkout')]")
            self.end_transaction("Transaction_6", 0)
            
            # Transaction 7: Continue
            self.start_transaction("Transaction_7")
            self.click_element("Continue button", "//input[@name='newOrder']")
            self.end_transaction("Transaction_7", 0)
            
            # Handle confirmation if needed
            try:
                self.click_element("Confirm", "//a[contains(text(), 'Confirm')]")
                self.log_step("Confirmed order")
            except:
                self.log_step("No confirmation needed", "info")
            
            # Transaction 8: Return to Main Menu
            self.start_transaction("Transaction_8")
            self.click_element("Return to Main Menu", "//a[contains(text(), 'Return to Main Menu')]")
            self.end_transaction("Transaction_8", 0)
            
            # Transaction 9: Sign Out
            self.start_transaction("Transaction_9")
            self.click_element("Sign Out", "//a[contains(text(), 'Sign Out')]")
            self.end_transaction("Transaction_9", 0)
            
            self.results["status"] = "completed"
            self.results["end_time"] = datetime.now().isoformat()
            print("✅ TrueClient script executed successfully!")
            
        except Exception as e:
            self.results["status"] = "failed"
            self.results["error"] = str(e)
            print(f"❌ Script execution failed: {e}")
        
        finally:
            # Take screenshot if needed
            try:
                screenshot_path = "results/execution_screenshot.png"
                self.driver.save_screenshot(screenshot_path)
                self.log_step(f"Screenshot saved: {screenshot_path}")
            except:
                pass
            
            self.driver.quit()
    
    def save_results(self):
        """Save execution results"""
        os.makedirs('results', exist_ok=True)
        
        # Save detailed results
        results_file = f"results/trueclient_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save summary for GitHub Actions
        summary = {
            "script": "TrueClient_PetStore",
            "execution_time": self.results["end_time"],
            "status": self.results["status"],
            "total_transactions": len(self.results["transactions"]),
            "passed_transactions": len([t for t in self.results["transactions"].values() if t["status"] == "pass"]),
            "results_file": results_file
        }
        
        with open('temp/execution_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary

def main():
    executor = TrueClientExecutor(headless=True)
    executor.execute_petstore_script()
    summary = executor.save_results()
    
    print("\n📊 EXECUTION SUMMARY:")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()