
# Gulf Quaterly Financial Scraper

This is a Python-based automation tool that scrapes, processes, renames, and uploads financial reports (PDFs) from various stock exchanges in the GCC (Gulf Cooperation Council) region.

Supported Countries:

- 🇸🇦 Saudi Arabia

- 🇧🇭 Bahrain

- 🇰🇼 Kuwait

- 🇦🇪 Dubai (UAE)

- 🇴🇲 Oman

- 🇶🇦 Qatar (QE)

- 🇦🇪 Abu Dhabi (ADX)


---

### 🧰 Features

- Extracts financial reports from official exchange sites for the given quarter

- Downloads and renames PDFs using custom suffixes

- Cleans and processes metadata (CSV)

- Unzips compressed reports (for Oman)

- Uploads all reports to Zoho WorkDrive

---

### 🚀 Getting Started

#### 1. Download code onto EC2 instance.

`scp -i "/path/to/your-key.pem" -r /path/to/code/financialScraper ec2-user@your-ec2-public-dns`

#### 2. SSH into the instance using your `.pem` key.

`ssh -i /path/to/your-key.pem ec2-user@your-ec2-public-dns`

#### 2. Install Dependencies

`pip install -r requirements.txt`
`playwright install`
`sudo apt install tmux`

#### 3. Install Google Chrome and Google ChromeDriver

`wget "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chrome-linux64.zip"
unzip chrome-linux64.zip
cd chrome-linux64
sudo mv chrome /usr/local/bin/google-chrome
cd ..`

`wget "https://storage.googleapis.com/chrome-for-testing-public/137.0.7151.119/linux64/chromedriver-linux64.zip"
unzip chromedriver-linux64.zip
cd chromedriver-linux64
sudo mv chromedriver /usr/local/bin/chromedriver
cd ..`
#### 3. Run the Scraper

`tmux new -s mysession`
`cd financialScraper`
`python main.py`

#### 4. Enter the Prompts for Quarter and Year
---


### 📬 Output

- Processed and renamed PDFs

- Files uploaded to Zoho (or another endpoint)


---

### 🧪 Testing

Run python3 `testmain.py`

---
