from playwright.sync_api import sync_playwright
import csv
import alerts
from urllib.parse import urljoin


def run_scraper():
	with sync_playwright() as p:
		browser = p.chromium.launch(headless=False)
		context = browser.new_context()
		page = context.new_page()


		with open("scraped_properties.csv", mode="w", newline="", encoding="utf-8") as file:
			writer = csv.writer(file)

			writer.writerow(["Listing Title", "Price", "Description"])

			total_price_sum = 0.0
			highest_price = 0.0
			lowest_price = float('inf')
			scraped_count = 0

			for page_number in range(1, 3):
				print(f"\n--- SCRAPING PAGE {page_number} ---\n")


				target_url = f"http://books.toscrape.com/catalogue/page-{page_number}.html"
				print(f"Navigating to {target_url}...")
				page.goto(target_url)
				

				items = page.query_selector_all("article.product_pod")
				print(f"Found {len(items)} items on this page!.\n")

				scraped_items_data = []


				for item in items:
					title_element = item.query_selector("h3 a")
					title = title_element.get_attribute("title") if title_element else "Unknown"

					price_element = item.query_selector("p.price_color")
					price = price_element.inner_text() if price_element else "$0.00"


					relative_url = title_element.get_attribute("href") if title_element else None
					#description = "No Description found"

					scraped_items_data.append({
						"title": title,
						"price": price,
						"relative_url": relative_url
					})

				for data in scraped_items_data:
					title = data["title"]
					price = data["price"]
					relative_url = data["relative_url"]
					description = "No description found"


					cleaned_price = float(price[1:])


					if relative_url:
						# deep_page_url = f"http://books.toscrape.com/catalogue/{relative_url}"
						# print(f" Jumping Inside: {title[:25]}")
						deep_page_url = urljoin(page.url, relative_url)
						print(f"Jumping Inside {title[:25]}...")
						page.goto(deep_page_url)




						desc_element = page.query_selector("#product_description + p")
						if desc_element:
							description = desc_element.inner_text().strip()

						page.goto(target_url)

					scraped_count += 1
					total_price_sum += cleaned_price

					if cleaned_price > highest_price:
						highest_price = cleaned_price

					if cleaned_price < lowest_price:
						lowest_price = cleaned_price

					writer.writerow([title, price, description])
					print(f" Product: {title[:20]} | Price: {price}")

					if cleaned_price < 15.00:
						alerts.send_discord_alert(title, price, deep_page_url)
						alerts.send_email_alert(title, price, deep_page_url)

				next_button = page.query_selector("li.next a")

				if next_button:
					print("Next button found! clicking to go to the next page...")
					next_button.click()
					page_number += 1
				else:
					print("\nNo 'Next' button found. We have reached the finalpage!'")
					break

			average_price = total_price_sum / scraped_count if scraped_count > 0 else 0.0
			print("\n==============================================")
			print("            MARKET ANALYTICS REPORT             ")
			print(f" Total Properties Processed : {scraped_count}")
			print(f" Total Portfolio Value      : ${total_price_sum:.2f}")
			print(f" Average Market Price       : ${average_price:.2f}")
			print(f"Premium/ highest Listing    : ${highest_price:.2f}")
			print(f"Discount / lowest Listing    : ${lowest_price:.2f}")
			print("=================================================")


		print(f"\n--- All Pages Successfully Scrubbed and Saved! ---")


		input("Scraper is paused. Press enter in the terminal here to close the browser...")

		context.close()
		browser.close()

if __name__ == "__main__":
	run_scraper()






