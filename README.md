# Automarketer

Automarketer is an automated email marketing platform that uses customer segmentation and AI-generated content to deliver personalized marketing emails. It clusters customers, generates tailored email content for each segment, and can send real emails via SMTP.

## Features

- Customer data ingestion and preprocessing
- KMeans clustering for customer segmentation
- AI-powered email generation for each cluster
- Editable email templates via a Streamlit dashboard
- Real email sending using Gmail SMTP
- Logging and saving of sent emails and cluster profiles

## Project Structure

```
automarketer/
│
├── data/                     # Customer + email data
│   ├── marketing_campaign.csv
│   └── cluster_emails.csv
│
├── src/                      # Core logic
│   ├── ingest.py
│   ├── preprocess.py
│   ├── cluster.py
│   ├── email_generator.py
│   ├── send_real_email.py
│   └── utils.py
│
├── dashboard.py              # Streamlit UI
├── requirements.txt
├── .env                      # API keys (not committed)
└── README.md
```

## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Create a `.env` file in the root directory:
     ```
     SENDER_EMAIL=your_gmail_address@gmail.com
     SENDER_PASSWORD=your_gmail_app_password
     ```

4. **Prepare your data:**
   - Place your customer data CSV (e.g., `marketing_campaign.csv`) in the `data/` folder.

## Usage

### 1. Run the Main Pipeline

This will preprocess data, cluster customers, generate emails, and save results.

```sh
python main.py
```

- Outputs:
  - `data/clustered_customers.csv`: Customers with cluster labels
  - `data/cluster_emails.csv`: Generated emails for each cluster

### 2. Edit and Regenerate Emails (Streamlit Dashboard)

```sh
streamlit run dashboard.py
```

- Edit email templates for each cluster
- Regenerate emails using the LLM
- Save changes to `data/cluster_emails.csv`

### 3. Send a Test Email

```sh
python src/send_real_email.py
```

- Sends a sample email to the address specified in `.env`

## File Descriptions

- `main.py`: Main script for clustering and email generation
- `dashboard.py`: Streamlit app for editing and regenerating emails
- `src/send_real_email.py`: Script to send a test email
- `src/`: Core modules:
  - `ingest.py`: Data loading
  - `preprocess.py`: Data preprocessing
  - `cluster.py`: Clustering logic
  - `email_generator.py`: AI email generation
  - `utils.py`: Helper functions

## Requirements

- Python 3.8+
- See `requirements.txt` for all dependencies

## Notes

- For Gmail SMTP, you may need to create an [App Password](https://support.google.com/accounts/answer/185833) if 2FA is enabled.
- Data files are expected in the `data/` directory.

