This repository is part of the Bharatiya Antariksh Hackathon 2025 submission. It presents an AI-powered system to predict PM2.5 air pollution using a fusion of MODIS AOD (satellite), MERRA-2 (reanalysis), and OpenAQ (ground-based) data.
While this prototype uses New Delhi for demonstration, the ultimate goal is to scale it to a grid-level prediction model for all of India.

Problem Statement
Air pollution monitoring in India is limited due to sparse and unreliable ground-level sensors. Many regions lack real-time PM2.5 data, making early warnings and mitigation difficult.
Our solution fills this gap by combining:
Satellite Aerosol Optical Depth (AOD) data
MERRA-2 reanalysis atmospheric data
Ground-based PM2.5 measurements
This allows PM2.5 prediction even in sensor-less regions.

Results
Metric:-
Value
RMSE        57.23 µg/m³
R² Score    0.88

Feature Importance Highlights:
Temperature (T2M, TS)
Wind (U10M, V10M)
AOD
Total Precipitable Water (TQV)
Sea Level Pressure (SLP)

Data Sources
MODIS AOD: NASA GES DISC
MERRA-2 Reanalysis: NASA GES DISC
Ground PM2.5: OpenAQ API

