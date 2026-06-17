# ML Monitoring & Responsible Use Plan

## 1. Monitoring Strategy (Post-Deployment)
To ensure the Churn API remains accurate and reliable in production, the following metrics will be tracked:
* **Data Drift:** Monitor incoming JSON feature payloads for distribution shifts (e.g., if average `recency_days` suddenly doubles, upstream data pipelines may be broken).
* **Prediction Distribution:** Track the ratio of High-Risk to Low-Risk predictions daily. A sudden spike to 90% High-Risk indicates a model anomaly.
* **API Errors:** Track 4xx and 5xx HTTP errors to ensure CRM systems are sending correctly formatted payloads.
* **Business Outcomes:** Join model predictions with actual customer behavior 60 days later to track real-world Precision and Recall.
* **Retraining Triggers:** The model will be retrained automatically if real-world Recall drops below 75%, or on a fixed quarterly schedule, whichever comes first.

## 2. Responsible Use Note
**How to use this API:**
* **Do:** Use these scores to prioritize VIP outreach, send personalized "we miss you" surveys, or trigger targeted retention discounts for price-sensitive segments.
* **Do Not:** Use this score to deny customer service, penalize customers, or make assumptions about a customer's financial status. The model detects *behavioral patterns*, not intent. Do not blindly give 50% discounts to every "High Risk" customer, as this will lead to margin erosion and discount conditioning.
