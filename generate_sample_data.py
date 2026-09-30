"""
Generates rich sample submission and resubmission texts based on the real Bukadra Plot 6117262 schematic packages.
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent

SAMPLE_ARCH = """PROJECT: ELLINGTON BUKADRA RESIDENTIAL TOWER
LOCATION: PLOT 6117262, MEYDAN HORIZON / BUKADRA, DUBAI, UAE
STAGE: SCHEMATIC DESIGN (100%)
DISCIPLINE: ARCHITECTURE & PLANNING
SUBMISSION VERSION: V1.0

1. EXECUTIVE SUMMARY & DEVELOPMENT METRICS
The proposed luxury residential development on Plot 6117262 comprises 4 Podium levels (P1 to P4), 1 Ground Floor, and 31 Typical Residential Floors (G+4P+31F+Roof).
- Total Built-Up Area (BUA): 48,250 sq.m
- Total Gross Floor Area (GFA): 32,800 sq.m (compliant with Meydan Horizon Master Plan FAR allocation 4.5)
- Plot Area: 7,288 sq.m
- Proposed Building Height: 128.5 m Above Ground Level (AGL) / Max Permissible AOD 145m.
- Ground Floor Active Retail & Signature Double-Height Entrance Lobby (7.2m clear height).

2. PLANNING & SETBACKS (MEYDAN HORIZON DCR)
- Front Road Setback: 6.0 m provided to property line.
- Side Setbacks: 4.5 m provided between podium edge and adjacent plot boundary.
- Rear Setback: 5.0 m provided to canal promenade buffer.
- Podium Coverage: 68% (Meydan Horizon DCR maximum permissible 70%).

3. VEHICULAR CIRCULATION & PARKING
- Total Parking Provided: 412 bays located across Ground and 4 Podium floors.
- Residential Unit Allocation: 1-bed (1 bay), 2-bed (1 bay), 3-bed (2 bays), Penthouses (3 bays).
- Visitor Parking: 35 dedicated visitor bays located on Ground Floor.
- Accessible Parking: 9 designated universal accessible bays adjacent to core elevators (compliant with Dubai Universal Design Code).
- Ingress/Egress: Dual-lane vehicular access from primary collector street with 15m queuing reservoir.

4. FAÇADE DESIGN & MATERIALITY (ELLINGTON BRAND STANDARDS 2024)
- High-performance low-E double glazed unitized curtain wall system (U-value = 1.6 W/m²K, SHGC = 0.28).
- Signature palette featuring fluted architectural terracotta, warm travertine cladding panels, and champagne-bronze powder coated aluminum louvers.
- Expansive cantilevered balconies with minimum 2.0m depth featuring frameless laminated safety glass balustrades.

5. AMENITY PODIUM & ROOF LANDSCAPE
- Level 4 Podium Deck includes resort-style 25m infinity edge swimming pool, children's splash pool, outdoor yoga deck, and landscaped BBQ pavilions.
- Double-height indoor fitness centre, wellness spa, and private cinema room.
"""

SAMPLE_FLS = """PROJECT: ELLINGTON BUKADRA RESIDENTIAL TOWER
LOCATION: PLOT 6117262, MEYDAN HORIZON, DUBAI, UAE
STAGE: SCHEMATIC DESIGN
DISCIPLINE: FIRE & LIFE SAFETY (FLS)
SUBMISSION VERSION: V1.0

1. APPLICABLE CODE BASE
- UAE Fire & Life Safety Code of Practice 2018 (UAE Fire Code).
- Dubai Civil Defense (DCD) Requirements for High-Rise Residential Buildings (Occupancy Class A).
- NFPA 101 Life Safety Code (reference baseline).

2. MEANS OF EGRESS & EXIT CAPACITY
- Two independent 2-hour fire-rated exit staircases (Stair 1 and Stair 2) provided continuously from 31st Floor down to Ground level with direct discharge to exterior open space.
- Maximum Travel Distance: Common path travel distance is 14.2m (< 15m allowed); Total travel distance to nearest exit staircase is 26.8m (< 30m maximum allowed under UAE Fire Code).
- Exit Stair Width: 1200mm clear width with 150mm treads and 175mm risers.
- Fire Door Specifications: 120-min fire-rated, self-closing doors with panic hardware and magnetic hold-open linked to BMS/FACP.

3. SMOKE MANAGEMENT & PRESSURIZATION
- Dedicated staircase pressurization fans providing positive pressure differential (50 Pa ± 5 Pa) in accordance with DCD guidelines.
- Lift lobby smoke containment and pressurized firefighter emergency elevator shaft.

4. FIRE SUPPRESSION & DETECTION
- Automatic wet-pipe sprinkler system throughout all residential units, corridors, basements, and podium parking (NFPA 13 compliant).
- Class I Standpipe system with landing valves located in all exit stairwell landings.
- Fire water reserve: 45,000 Gallon dedicated fire storage tank with UL/FM certified electric, diesel, and jockey pumps.
- DCD 24x7 Direct Alarm Monitoring connectivity hub located in Ground Floor Fire Control Room.
"""

SAMPLE_ACOUSTICS_STRUCT = """PROJECT: ELLINGTON BUKADRA RESIDENTIAL TOWER
LOCATION: PLOT 6117262, MEYDAN HORIZON, DUBAI, UAE
STAGE: SCHEMATIC DESIGN
DISCIPLINE: ACOUSTICS & STRUCTURAL ENGINEERING
SUBMISSION VERSION: V1.0

1. ACOUSTIC DESIGN CRITERIA (INFOSIGHT ACOUSTIC REPORT)
- Internal Ambient Noise Levels: Bedrooms NC 30 (LAeq 35 dB), Living Rooms NC 35 (LAeq 40 dB), Corridors NC 40.
- Sound Transmission Class (STC) & Field Sound Transmission:
  * Inter-tenancy separating walls: STC 55 / DnT,w 50 dB (double plasterboard with acoustic insulation quilt).
  * Floor/Ceiling impact insulation: IIC 55 / L'n,w <= 55 dB with resilient acoustic underlay beneath porcelain tiles.
  * Mechanical plant room enclosure: STC 60 with vibration isolation spring mounts for chillers and pumps.
- Facade Acoustic Glazing: Minimum Rw+Ctr 38 dB against surrounding traffic noise from Ras Al Khor and Meydan collector road.

2. STRUCTURAL SCHEME & GRID ALIGNMENT
- Gravity & Lateral Load Resisting System: Reinforced concrete dual system with central shear core walls and perimeter columns.
- Typical Floor Slab: 225mm thick post-tensioned flat slab system.
- Transfer Slab: Level 1 Podium Transfer Plate (1200mm thick RC slab) transferring upper residential tower columns to 8.4m x 8.4m podium parking column grid.
- Column alignment verified: Upper tower vertical loads align directly with shear core and transfer plate drop panels.
- Deep Foundation: Continuous Flight Auger (CFA) bored cast-in-situ piles socketed into Dubai sandstone layer.
"""

SAMPLE_RESUBMISSION = """PROJECT: ELLINGTON BUKADRA RESIDENTIAL TOWER
LOCATION: PLOT 6117262, MEYDAN HORIZON, DUBAI, UAE
STAGE: SCHEMATIC DESIGN — RESUBMISSION PACKAGE
DISCIPLINE: MULTI-DISCIPLINARY CONSOLIDATED
SUBMISSION VERSION: V2.0 (CONSULTANT RESPONSE TO DESIGN REVIEW COMMENTS)

1. CONSULTANT RESPONSE TO REVIEW FINDINGS

[Finding ID: DCR-SETBACK-001 - Boundary Setbacks]
RESOLVED: Detailed setback demarcation schedule added to Sheet AR-1000 and AR-1001.
- Front road setback confirmed at 6.0m.
- Side setback confirmed at 4.5m with clear boundary dimensioning.
- Rear canal setback confirmed at 5.0m.

[Finding ID: AUTH-DM-PARKING-012 - Parking Provision & Ratios]
RESOLVED: Consolidated parking schedule updated on Sheet AR-0030.
- Total 412 residential bays provided (exceeding DM minimum requirement of 385 bays).
- 35 dedicated visitor bays and 9 universal accessible bays clearly demarcated.

[Finding ID: AUTH-DCD-EGRESS-010 - UAE Fire Code Travel Distances]
RESOLVED: Fire & Life Safety egress analysis plans FLS-1001 through FLS-1036 updated with exact travel distance line paths.
- Maximum single direction dead-end travel distance: 12.4m (< 15m allowable).
- Maximum travel distance to exit stair: 26.8m (< 30m allowable).
- DCD compliance stamp included on title blocks.

[Finding ID: ELL-BRAND-PALETTE-021 - Ellington 2024 Brand Material Palette]
RESOLVED: Material specifications sheet updated to include Ellington Signature 2024 Travertine Light Classico, Brushed Champagne Bronze aluminum framing, and Low-E acoustic glazing specifications.

[Finding ID: COORD-STR-COLUMN-030 - Column Grid Continuity]
RESOLVED: Superimposed architectural and structural overlay drawing AR-STR-OVERLAY-01 submitted confirming 100% column coordination across Podium Level 4 to Typical Floor 1 transfer zones.
"""

def generate():
    (BASE_DIR / "sample_schematic_arch.txt").write_text(SAMPLE_ARCH.strip(), encoding="utf-8")
    (BASE_DIR / "sample_schematic_fls.txt").write_text(SAMPLE_FLS.strip(), encoding="utf-8")
    (BASE_DIR / "sample_schematic_acoustics_struct.txt").write_text(SAMPLE_ACOUSTICS_STRUCT.strip(), encoding="utf-8")
    (BASE_DIR / "sample_schematic_resubmission_v2.txt").write_text(SAMPLE_RESUBMISSION.strip(), encoding="utf-8")
    print("Sample packages created successfully.")

if __name__ == "__main__":
    generate()
