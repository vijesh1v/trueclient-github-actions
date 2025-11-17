#!/usr/bin/env python3
"""
TrueClient Script Executor - FIXED VERSION
Uses WebDriver Manager for automatic ChromeDriver management
"""
import os
import time
import json
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

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
        """Setup Chrome WebDriver with WebDriver Manager"""
        print("🚀 Setting up ChromeDriver...")
        
        chrome_options = webdriver.ChromeOptions()
        
        if headless:
            chrome_options.add_argument('--headless=new')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-logging')
        
        # Use WebDriver Manager to handle ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        
        print("✅ ChromeDriver setup completed")
    
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
        
        status_icon = "✅" if status == "success" else "❌" if status == "error" else "⚠️"
        print(f"{status_icon} {step_name}: {status}")
        
        if error_message:
            print(f"   Error: {error_message}")
    
    def start_transaction(self, transaction_name):
        """Start transaction timing"""
        self.current_transaction = transaction_name
        self.transaction_start_time = time.time()
        print(f"🟢 START TRANSACTION: {transaction_name}")
    
    def end_transaction(self, transaction_name, status=0):
        """End transaction and record timing"""
        if hasattr(self, 'transaction_start_time'):
            duration = time.time() - self.transaction_start_time
            transaction_status = "pass" if status == 0 else "fail"
            self.results["transactions"][transaction_name] = {
                "status": transaction_status,
                "duration_seconds": round(duration, 2),
                "end_time": datetime.now().isoformat()
            }
            status_icon = "✅" if transaction_status == "pass" else "❌"
            print(f"{status_icon} END TRANSACTION: {transaction_name} - {duration:.2f}s")
    
    def navigate_to(self, url, step_name="Navigate to URL"):
        """Navigate to URL"""
        try:
            print(f"🌐 Navigating to: {url}")
            self.driver.get(url)
            time.sleep(2)  # Allow page to load
            self.log_step(step_name)
            return True
        except Exception as e:
            self.log_step(step_name, "error", str(e))
            return False
    
    def click_element(self, element_description, selector, by_type=By.XPATH):
        """Click on element"""
        try:
            print(f"🖱️ Looking for: {element_description}")
            element = self.wait.until(EC.element_to_be_clickable((by_type, selector)))
            element.click()
            time.sleep(1)  # Allow action to complete
            self.log_step(f"Click {element_description}")
            return True
        except Exception as e:
            self.log_step(f"Click {element_description}", "error", str(e))
            return False
    
    def type_text(self, element_description, selector, text, by_type=By.XPATH):
        """Type text into element"""
        try:
            print(f"⌨️ Typing in: {element_description}")
            element = self.wait.until(EC.element_to_be_clickable((by_type, selector)))
            element.clear()
            element.send_keys(text)
            self.log_step(f"Type '{text}' in {element_description}")
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
            success = self.navigate_to("https://petstore.octoperf.com/actions/Catalog.action", "Navigate to PetStore")
            self.end_transaction("Transaction_1", 0 if success else 1)
            
            if not success:
                raise Exception("Failed to navigate to PetStore")
            
            # Take initial screenshot
            self.driver.save_screenshot("results/initial_page.png")
            
            # Transaction 2: Click Sign In
            self.start_transaction("Transaction_2")
            success = self.click_element("Sign In link", "//a[contains(text(), 'Sign In')]")
            self.end_transaction("Transaction_2", 0 if success else 1)
            
            # Transaction 3: Login Process
            self.start_transaction("Transaction_3")
            # Username
            self.click_element("username textbox", "//input[@name='username']")
            self.type_text("username textbox", "//input[@name='username']", "vv1234")
            # Password
            self.click_element("password field", "//input[@name='password']")
            self.type_text("password field", "//input[@name='password']", "password123")  # Update password
            # Login button
            success = self.click_element("Login button", "//input[@name='signon']")
            self.end_transaction("Transaction_3", 0 if success else 1)
            
            # Wait for login to complete
            time.sleep(3)
            
            # Transaction 4: Click Fish Image (using different selector)
            self.start_transaction("Transaction_4")
            success = self.click_element("Fish image", "//img[@src='../images/fish_icon.gif']")
            self.end_transaction("Transaction_4", 0 if success else 1)
            
            # Click specific fish product
            self.click_element("FI SW 01 link", "//a[contains(@href, 'FI-SW-01')]")
            
            # Transaction 5: Add to Cart
            self.start_transaction("Transaction_5")
            success = self.click_element("Add to Cart", "//a[contains(@href, 'addItemToCart')]")
            self.end_transaction("Transaction_5", 0 if success else 1)
            
            # Update quantity - wait for page to load
            time.sleep(2)
            self.type_text("quantity field", "//input[@name='quantity']", "2")
            
            # Transaction 6: Proceed to Checkout
            self.start_transaction("Transaction_6")
            success = self.click_element("Proceed to Checkout", "//a[contains(@href, 'newOrderForm')]")
            self.end_transaction("Transaction_6", 0 if success else 1)
            
            # Transaction 7: Continue
            self.start_transaction("Transaction_7")
            success = self.click_element("Continue button", "//input[@name='newOrder']")
            self.end_transaction("Transaction_7", 0 if success else 1)
            
            # Handle confirmation if needed
            try:
                self.click_element("Confirm", "//a[contains(text(), 'Confirm')]")
                self.log_step("Confirmed order", "info")
            except:
                self.log_step("No confirmation needed", "info")
            
            # Transaction 8: Return to Main Menu
            self.start_transaction("Transaction_8")
            success = self.click_element("Return to Main Menu", "//a[contains(text(), 'Main Menu')]")
            self.end_transaction("Transaction_8", 0 if success else 1)
            
            # Transaction 9: Sign Out
            self.start_transaction("Transaction_9")
            success = self.click_element("Sign Out", "//a[contains(text(), 'Sign Out')]")
            self.end_transaction("Transaction_9", 0 if success else 1)
            
            self.results["status"] = "completed"
            self.results["end_time"] = datetime.now().isoformat()
            print("✅ TrueClient script executed successfully!")
            
        except Exception as e:
            self.results["status"] = "failed"
            self.results["error"] = str(e)
            print(f"❌ Script execution failed: {e}")
            
            # Take screenshot on failure
            try:
                self.driver.save_screenshot("results/error_screenshot.png")
                print("📸 Screenshot saved: results/error_screenshot.png")
            except:
                pass
        
        finally:
            try:
                self.driver.quit()
                print("🔴 Browser closed")
            except:
                pass
    
    def save_results(self):
        """Save execution results"""
        os.makedirs('results', exist_ok=True)
        
        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"results/trueclient_results_{timestamp}.json"
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Calculate summary
        total_transactions = len(self.results["transactions"])
        passed_transactions = len([t for t in self.results["transactions"].values() if t["status"] == "pass"])
        
        summary = {
            "script": "TrueClient_PetStore",
            "execution_time": datetime.now().isoformat(),
            "status": self.results["status"],
            "total_transactions": total_transactions,
            "passed_transactions": passed_transactions,
            "success_rate": f"{(passed_transactions/total_transactions)*100:.1f}%" if total_transactions > 0 else "0%",
            "results_file": results_file
        }
        
        # Save summary
        os.makedirs('temp', exist_ok=True)
        with open('temp/execution_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        # Also create a simple text summary
        with open('temp/summary.txt', 'w') as f:
            f.write(f"TrueClient Execution Summary\n")
            f.write(f"============================\n")
            f.write(f"Status: {summary['status']}\n")
            f.write(f"Passed: {summary['passed_transactions']}/{summary['total_transactions']}\n")
            f.write(f"Success Rate: {summary['success_rate']}\n")
            f.write(f"Completed at: {summary['execution_time']}\n")
        
        return summary

def main():
    print("=" * 60)
    print("TrueClient Script Executor - GitHub Actions")
    print("=" * 60)
    
    try:
        executor = TrueClientExecutor(headless=True)
        executor.execute_petstore_script()
        summary = executor.save_results()
        
        print("\n📊 EXECUTION SUMMARY:")
        print("=" * 30)
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        # Exit with appropriate code
        sys.exit(0 if summary["status"] == "completed" else 1)
        
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
