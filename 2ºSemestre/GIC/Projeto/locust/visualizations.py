import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Setup
sns.set(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load the CSV file
file_path = "./frontend/locust_frontend_bytebazaar_requests.csv"
df = pd.read_csv(file_path)

# Optional: Remove the 'Aggregated' row
df = df[df['Name'] != 'Aggregated']

# Create output directory
output_dir = "api_plots"
os.makedirs(output_dir, exist_ok=True)

# Plot: Average Response Time by Endpoint
plt.figure()
sns.barplot(data=df.sort_values('Average Response Time', ascending=False), 
            y='Name', x='Average Response Time', palette='viridis')
plt.title('Average Response Time by Endpoint')
plt.xlabel('Average Response Time (ms)')
plt.ylabel('Endpoint')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "average_response_time_by_endpoint.png"))
plt.show()