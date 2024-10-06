# Evacuation-planning-sp
Our model takes into account a wide range of factors including local geography, available infrastructure, population distribution, and the nature of the threat (landslides and heavy rainfall).# Evacuation Planner

## Overview

The Evacuation Planner is a sophisticated system designed to generate evacuation plans based on real-time weather and seismic data. It assesses threats, identifies affected areas, determines evacuation routes, and allocates resources for efficient evacuation procedures.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/evacuation-planner.git
   cd evacuation-planner
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `config.json` file in the project root directory with the following structure:

   ```json
   {
     "grid_size": [100, 100],
     "location": "New York",
     "latitude": 40.7128,
     "longitude": -74.0060,
     "max_rainfall": 100,
     "max_earthquake_magnitude": 10,
     "earthquake_lookback_days": 7,
     "earthquake_radius_km": 100,
     "earthquake_api_endpoint": "https://earthquake.usgs.gov/fdsnws/event/1/query",
     "threat_factors": ["rainfall", "landslide_risk", "soil_saturation", "slope_angle"],
     "threat_assessment_weights": [0.3, 0.3, 0.2, 0.2],
     "threat_percentile": 70,
     "safe_zones": [[10, 10], [90, 90], [10, 90], [90, 10]],
     "people_per_vehicle": 50
   }
   ```

   Adjust the values according to your specific requirements and location.

2. Create a `.env` file in the project root directory with your Weather API key:

   ```
   WEATHER_API_KEY=your_api
# Comprehensive Evacuation Plan for Rudraprayag, Uttarakhand
## Landslide and Heavy Rainfall Emergency

### 1. Situation Assessment
- **Location**: Rudraprayag district, Uttarakhand
- **Primary Threats**: Landslides triggered by heavy rainfall, potential flash floods
- **Affected Areas**: 
  - Augustmuni (High Risk)
  - Ukhimath (High Risk)
  - Chandrapuri (Moderate Risk)
  - Tilwara (Moderate Risk)
  - Riverside settlements along Mandakini and Alaknanda rivers (High Risk)
- **Population at Risk**: Approximately 50,000 residents
- **Current Weather**: Continuous heavy rainfall (200mm in last 24 hours)
- **Geological Factors**: 
  - Soil saturation levels: 85-90%
  - Average slope angle in high-risk areas: 30-40 degrees

### 2. Threat Level Assessment
- Threat levels calculated using weighted factors:
  - Rainfall intensity (30%)
  - Landslide risk based on geological data (30%)
  - Soil saturation (20%)
  - Slope angle (20%)
- Areas with threat level above 70th percentile are prioritized for immediate evacuation

### 3. Identification of Affected Areas
- High-Risk Zones (Immediate Evacuation):
  - Augustmuni town center and surrounding villages
  - Ukhimath hillside communities
  - Riverside settlements within 500m of Mandakini and Alaknanda rivers
- Moderate-Risk Zones (Prepared for Evacuation):
  - Chandrapuri
  - Tilwara
  - Settlements 500m-1km from rivers

### 4. Safe Zones and Emergency Shelters
1. Rudraprayag Town
   - Primary: Government Inter College grounds (Capacity: 10,000)
   - Secondary: Rudraprayag Stadium (Capacity: 5,000)
2. Agastyamuni
   - Primary: Nagar Panchayat office area (Capacity: 5,000)
   - Secondary: Agastyamuni Degree College (Capacity: 3,000)
3. Guptkashi
   - Primary: Guptkashi Inter College (Capacity: 7,000)
   - Secondary: Vishwanath Temple grounds (Capacity: 4,000)
4. Sonprayag
   - Emergency shelter: Sonprayag Helipad area (Capacity: 2,000)

### 5. Evacuation Routes and Traffic Management
1. Augustmuni to Rudraprayag
   - Primary: NH107 → Rudraprayag (22 km)
   - Alternate: Via Gopeshwar-Chamoli road (35 km)
2. Ukhimath to Guptkashi
   - Primary: Ukhimath-Guptkashi road (25 km)
   - Alternate: Via Chopta-Mandal road (40 km)
3. Chandrapuri to Agastyamuni
   - Primary: Local road → NH107 → Agastyamuni (15 km)
4. Tilwara to Rudraprayag
   - Primary: NH107 → Rudraprayag (18 km)
5. Riverside settlements
   - Use nearest connection to NH107, then proceed to designated safe zone

Traffic Management:
- One-way traffic system on NH107 towards safe zones
- Police checkpoints at major junctions to direct traffic
- Emergency vehicles given priority access

### 6. Evacuation Priorities
1. Extremely high-risk areas (visible land movement, proximity to rivers)
2. Vulnerable populations (elderly, disabled, pregnant women, children)
3. Areas with highest threat level assessment
4. Moderate-risk zones
5. General population in lower-risk areas

### 7. Transportation Plan
- 100 government buses deployed to designated pickup points
- 50 4x4 vehicles for hard-to-reach areas
- 5 helicopters on standby for critical evacuations and supply delivery
- Private vehicles allowed on specific routes, escorted by police

### 8. Communication Strategy
- Emergency alerts via:
  - Mobile SMS (collaboration with telecom providers)
  - Local FM radio stations (All India Radio Rudraprayag)
  - Social media platforms (WhatsApp groups, Facebook)
- Loudspeaker announcements in villages (100 units deployed)
- Door-to-door notifications by local police and 500 volunteers
- Regular updates through District Emergency Operations Center (DEOC)

### 9. Resource Allocation
- Personnel:
  - 500 police officers for traffic management and security
  - 200 medical staff distributed across evacuation zones and shelters
  - 1000 volunteers for assistance and coordination
- Vehicles:
  - 100 buses (seating capacity: 50 each)
  - 50 4x4 vehicles
  - 5 helicopters
- Supplies:
  - 100,000 food packets
  - 200,000 liters of drinking water
  - 50,000 blankets
  - 10,000 first aid kits
- Equipment:
  - 20 earthmovers for debris clearance
  - 50 satellite phones for emergency communication
  - 100 power generators

### 10. Evacuation Timeline
- **Hour 0-2**: 
  - Issue evacuation orders
  - Deploy emergency response teams
  - Begin evacuation of extremely high-risk areas
- **Hour 2-6**: 
  - Continue priority evacuations
  - Open all emergency shelters
  - Start transportation from designated pickup points
- **Hour 6-12**: 
  - Evacuate moderate-risk zones
  - Conduct search and rescue for isolated individuals
  - Begin shelter management operations
- **Hour 12-24**: 
  - Complete main evacuation operations
  - Secure evacuated areas
  - Establish long-term shelter management
- **Hour 24+**: 
  - Maintain shelters
  - Monitor weather and landslide activity
  - Begin damage assessment in safe areas

### 11. Special Considerations
- Continuous monitoring of rainfall, river levels, and landslide activity
- Regular clearing of debris from NH107 and other crucial routes
- Coordination with Indian Army and NDRF for complex rescue operations
- Medical camps in each shelter with isolation facilities for COVID-19 precautions

### 12. Post-Evacuation Measures
- Regular situation updates to evacuees via shelter management teams
- Damage assessment teams to evaluate when it's safe to return
- Initiate recovery and rehabilitation plans
- Psychological support teams for trauma counseling
- Coordination with state and national authorities for relief funds and resources

### 13. Plan Review and Update
- Hourly review of evacuation progress
- Update plan based on real-time data and ground reports
- Daily briefing with all stakeholders to adjust strategies as needed

This plan should be executed in coordination with the State Disaster Response Force (SDRF), National Disaster Response Force (NDRF), local administration, and other relevant agencies. It should be adapted in real-time based on the evolving situation on the ground.
