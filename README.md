# Dangdang Book Scraper 📚

This is a practical web scraping project that collects book data from Dangdang.com based on search keywords.

## 🔍 Features

- Automates keyword search and multi-page crawling
- Saves book info (title, price, publisher, etc.) to Excel
- Downloads book cover images with unique filenames
- Handles missing images or download failures gracefully

## 🛠 Tech Stack

- Python
- Selenium
- openpyxl (for Excel export)

## 📂 Project Structure

dangdang-scraper/
├── src/
│ ├── scraper.py
│ ├── utils.py
├── output/
│ ├── images/
├── README.md
├── requirements.txt

## 🚀 How to Run

1. Install requirements:
   pip install -r requirements.txt
2. Run the scraper:
   python src/scraper.py

## 🧠 Learning Purpose

This project helps me master:

- Web automation with Selenium
- Excel and image handling in Python
- Exception handling and modular design
