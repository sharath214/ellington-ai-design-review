# Ellington Properties — AI Design Review (Updated with Ingested Knowledge Sources)

Enterprise AI-assisted design review platform for Ellington Properties with human-in-the-loop validation, master developer DCR compliance, authority code checks, and complete audit trail persistence.

---

## 🌟 Key Features & Updates

### 1. Ingested Multi-Pillar Knowledge Base (327 Sources Indexed)
- **Authority Design Codes & Guidelines (90 files)**:
  - **Dubai Municipality (DM)**: Dubai Building Code (DBC 2021), Al Safaat Green Building Code, Dubai Universal Design Code, Area & FAR definitions, circulars.
  - **Dubai Civil Defense (DCD)**: UAE Fire & Life Safety Code 2018 (travel distances, egress staircases, pressurization, fire separation).
  - **DEWA**: Electrical Installations Regulations (substation sizing, clearances, road access).
  - **DDA / DHA / DTCM / RAK Municipality / Trakhees / RTA**: Healthcare guidelines, hotel & resort rating criteria, master planning rules.
- **Development Control Regulations / DCR (91 files)**:
  - Master Developer frameworks for **Meydan Horizon / Bukadra, Dubai Hills Estate (DHE), Business Bay, Nakheel (JVC, Palm Jumeirah, Al Furjan), Dubai Islands, Marjan Island (Vols 1–8), Downtown Jebel Ali, Dubai South, Sobha Hartland**.
- **Ellington Brand Guidelines (5 files)**:
  - Ellington Brand Book 2024, Signature Material Palette, Double-Height Entrance Lobbies, Balcony Proportions & Luxury Specs.
- **Sample Schematic Design Packages (141 files)**:
  - Real project package for **Plot 6117262 Bukadra / Meydan Horizon**: Concept Design Report, Architectural Plans (Podiums to Roof), FLS Plans, Structural Plans, and Infosight Acoustics Report.

### 2. Multi-Discipline Rule & Clause Engine (15 Active Rules)
- **DCR Planning**: Boundary setbacks, plot coverage (<= 70%), max building height, FAR/GFA efficiency.
- **Life Safety & Authorities**: UAE Fire Code egress travel distance (< 30m), stair pressurization (50 Pa), parking ratios (DBC 2021), universal accessibility, DEWA substations, Al Safaat thermal U-values.
- **Ellington Brand Standards**: Double-height grand arrival lobby (>= 6m), signature travertine/bronze materials, deep outdoor balconies (>= 1.8m), resort amenity decks.
- **Cross-Discipline Coordination**: Column grid alignment (podiums vs typical floors), inter-tenancy acoustic partitions (STC >= 55).

### 3. Integrated Navigation & Workflows
- **📊 Executive Dashboard**: Project-wide stage progression, stage milestone tracking, knowledge readiness indicators.
- **📚 Knowledge Base Explorer**: Searchable and filterable catalogue of all 327 ingested documents with full metadata and path lookup.
- **🏗️ AI Design Review Studio**: End-to-end workflow with 1-click sample loaders (Bukadra Arch, FLS, Acoustics/Struct), AI first-pass review, Design Manager decisions, consultant package generation (HTML report), resubmission delta review, and stage sign-off.
- **📜 Rule & Clause Library**: Complete database of all automated rules, standard clauses, severity levels, and expected evidence.
- **✅ Completed Stages & Audit History**: Full audit trail of completed stages with CSV and HTML evidence pack exports.

---

## 🚀 How to Run

```powershell
# 1. Activate environment and verify dependencies
.venv\Scripts\python.exe -m pip install -r requirements.txt

# 2. Run the Streamlit Application
.venv\Scripts\python.exe -m streamlit run app.py
```

Access the dashboard at: **`http://localhost:8501`**
