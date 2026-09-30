import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import re
import json
from pathlib import Path

try:
    from pypdf import PdfReader
except Exception:
    PdfReader = None

try:
    from docx import Document
except Exception:
    Document = None

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title='Ellington AI Design Review Management System',
    page_icon='🏗️',
    layout='wide',
    initial_sidebar_state='expanded'
)

BASE_DIR = Path(__file__).parent
STAGE_HISTORY_FILE = BASE_DIR / 'stage_history.json'
KNOWLEDGE_CATALOG_FILE = BASE_DIR / 'knowledge_catalog.json'

# ---------------------------------------------------------
# Custom Styling (Ellington Luxury Aesthetic)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, .brand-font {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3.5rem;
    }
    
    /* Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #0A192F 0%, #0E2A47 60%, #173B61 100%);
        padding: 24px 28px;
        border-radius: 12px;
        color: #FFFFFF;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(10, 25, 47, 0.15);
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    
    .header-banner .title {
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-banner .gold-badge {
        background: linear-gradient(135deg, #D4AF37 0%, #AA820A 100%);
        color: #0A192F;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .header-banner .subtitle {
        color: #94A3B8;
        font-size: 0.92rem;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    /* Process Bar */
    .process-container {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 12px 18px;
        margin-bottom: 22px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }
    
    .process-step {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #475569;
    }
    
    .process-step.active {
        color: #0B315E;
        font-weight: 700;
    }
    
    .step-num {
        background: #E2E8F0;
        color: #334155;
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
    }
    
    .process-step.active .step-num {
        background: #0B315E;
        color: #FFFFFF;
    }
    
    /* Cards */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        transition: transform 0.15s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .card-label {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    
    .card-value {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0F172A;
        margin-top: 4px;
        font-family: 'Outfit', sans-serif;
    }
    
    .notice-box {
        background: #F0F9FF;
        border-left: 4px solid #0284C7;
        padding: 12px 16px;
        border-radius: 6px;
        color: #0C4A6E;
        font-size: 0.88rem;
        margin: 14px 0;
    }
    
    .human-box {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 12px 16px;
        border-radius: 6px;
        color: #78350F;
        font-size: 0.88rem;
        margin: 14px 0;
    }
    
    .client-box {
        background: #F0FDF4;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 6px;
        color: #064E3B;
        font-size: 0.88rem;
        margin: 14px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Design Stage Definitions
# ---------------------------------------------------------
STAGE_ORDER = [
    'Concept Design',
    'Schematic Design',
    'Detailed Design',
    'Tender Package'
]

def clean_stage_name(name):
    if not name:
        return 'Schematic Design'
    for s in STAGE_ORDER:
        if s.lower() in name.lower():
            return s
    return name


# ---------------------------------------------------------
# Comprehensive Multi-Discipline Rule Catalogue
# ---------------------------------------------------------
COMPREHENSIVE_RULES = [
    # 1. DCR & Planning (Feature F3.1)
    {
        'id': 'DCR-SETBACK-001',
        'pillar': 'Development Regulations (DCR)',
        'source': 'Meydan Horizon / Master Plan DCR',
        'category': 'Boundary Setbacks',
        'discipline': 'Architecture & Planning',
        'severity': 'High',
        'drawing_ref': 'AR-1000 / AR-1001',
        'keywords': ['setback', 'boundary', 'property line', 'buffer', 'road setback'],
        'expected': 'Explicit front, rear, and side setback dimensions matching master development regulations.',
        'issue_if_missing': True,
        'standard_clause': 'DCR Cl. 4.2: Minimum 6.0m road setback and 4.5m side plot setbacks required.',
        'cost_delta': 0,
        'schedule_delta': '1.0 week'
    },
    {
        'id': 'DCR-PLOTCOV-002',
        'pillar': 'Development Regulations (DCR)',
        'source': 'Development Control Regulations',
        'category': 'Plot Coverage & Footprint',
        'discipline': 'Architecture & Planning',
        'severity': 'Medium',
        'drawing_ref': 'AR-0029 (Area Summary)',
        'keywords': ['plot coverage', 'footprint', 'podium coverage', 'coverage ratio'],
        'expected': 'Plot coverage calculations verifying podium and tower footprints comply with master limit (<= 70%).',
        'issue_if_missing': True,
        'standard_clause': 'DCR Cl. 5.1: Maximum podium plot coverage shall not exceed 70% of total plot area.',
        'cost_delta': 0,
        'schedule_delta': '0.5 weeks'
    },
    {
        'id': 'DCR-HEIGHT-003',
        'pillar': 'Development Regulations (DCR)',
        'source': 'Master Development Control Regulations',
        'category': 'Building Height & Storeys',
        'discipline': 'Architecture & Planning',
        'severity': 'High',
        'drawing_ref': 'AR-2001 to AR-2004',
        'keywords': ['height', 'storey', 'story', 'floor level', 'aod', 'agl', 'elevation'],
        'expected': 'Building height (AGL / AOD) and storey breakdown clearly defined for zoning & aviation limits.',
        'issue_if_missing': True,
        'standard_clause': 'DCR Cl. 3.4: Permissible height limit G+4P+31F with max allowable AOD elevation.',
        'cost_delta': 0,
        'schedule_delta': '1.5 weeks'
    },
    {
        'id': 'DCR-FAR-004',
        'pillar': 'Development Regulations (DCR)',
        'source': 'Dubai Development Authority / DM Standards',
        'category': 'FAR / GFA Compliance',
        'discipline': 'Architecture & Planning',
        'severity': 'High',
        'drawing_ref': 'AR-0012 to AR-0028',
        'keywords': ['gfa', 'gross floor area', 'far', 'floor area ratio', 'bua', 'built-up area'],
        'expected': 'GFA and BUA computations demonstrating compliance with approved FAR allocation.',
        'issue_if_missing': True,
        'standard_clause': 'DDA ZA-DC-REG-02: GFA computations must exclude permitted exemptions (balconies, mechanical, parking).',
        'cost_delta': 0,
        'schedule_delta': '1.0 week'
    },

    # 2. Authority Life Safety & Building Codes (Feature F3.1)
    {
        'id': 'AUTH-DCD-EGRESS-010',
        'pillar': 'Authority Codes',
        'source': 'Dubai Civil Defense (UAE Fire Code 2018)',
        'category': 'Fire & Life Safety Egress',
        'discipline': 'Fire & Life Safety',
        'severity': 'High',
        'drawing_ref': 'FLS-1001 to FLS-1036',
        'keywords': ['travel distance', 'egress', 'exit stair', 'staircase', 'means of egress', 'dead end'],
        'expected': 'Travel distances to exit stairs <= 30m and dead-end corridor <= 15m in accordance with UAE Fire Code.',
        'issue_if_missing': True,
        'standard_clause': 'UAE Fire Code 2018 Ch. 3: Max travel distance to nearest enclosed exit stair shall not exceed 30m.',
        'cost_delta': 120000,
        'schedule_delta': '2.0 weeks'
    },
    {
        'id': 'AUTH-DCD-STAIR-011',
        'pillar': 'Authority Codes',
        'source': 'Dubai Civil Defense (UAE Fire Code 2018)',
        'category': 'Staircase Pressurization & Fire Doors',
        'discipline': 'Fire & Life Safety',
        'severity': 'High',
        'drawing_ref': 'FLS-1037 / MEP-FLS-01',
        'keywords': ['pressurization', 'fire door', 'fire rating', 'discharge', 'smoke management', 'firefighter elevator'],
        'expected': '2-hour fire-rated exit enclosures, 50 Pa positive pressurization, and direct ground exterior discharge.',
        'issue_if_missing': True,
        'standard_clause': 'UAE Fire Code 2018 Ch. 10: Exit stairs in high-rise buildings require 2-hour rating and mechanical pressurization.',
        'cost_delta': 85000,
        'schedule_delta': '1.5 weeks'
    },
    {
        'id': 'AUTH-DM-PARKING-012',
        'pillar': 'Authority Codes',
        'source': 'Dubai Building Code (DBC 2021) / DM',
        'category': 'Parking Ratios & Allocation',
        'discipline': 'Planning & Regulations',
        'severity': 'Medium',
        'drawing_ref': 'AR-0030 (Schedules)',
        'keywords': ['parking', 'car park', 'parking bay', 'visitor parking', 'residential bays'],
        'expected': 'Parking provision adhering to unit bedroom count ratios plus dedicated visitor and accessible bays.',
        'issue_if_missing': True,
        'standard_clause': 'DM DBC 2021 Part E: Residential parking min 1 bay (1-2 bed), 2 bays (3+ bed) plus 10% visitor provision.',
        'cost_delta': 150000,
        'schedule_delta': '1.0 week'
    },
    {
        'id': 'AUTH-DM-UNIVERSAL-013',
        'pillar': 'Authority Codes',
        'source': 'Dubai Universal Design Code 2017',
        'category': 'Accessibility & Universal Design',
        'discipline': 'Architecture & Planning',
        'severity': 'Medium',
        'drawing_ref': 'AR-1001 (Ground Floor)',
        'keywords': ['accessible', 'barrier-free', 'universal design', 'ramp', 'pod', 'disabled'],
        'expected': 'Barrier-free pedestrian pathways, compliant ramp gradients (1:12), and accessible parking close to lifts.',
        'issue_if_missing': True,
        'standard_clause': 'Dubai Universal Design Code: Mandatory universal accessibility features across public and amenity zones.',
        'cost_delta': 35000,
        'schedule_delta': '0.5 weeks'
    },
    {
        'id': 'AUTH-DEWA-SUBST-014',
        'pillar': 'Authority Codes',
        'source': 'DEWA Regulations for Electrical Installations',
        'category': 'DEWA Substation & Clearances',
        'discipline': 'MEP & Utilities',
        'severity': 'High',
        'drawing_ref': 'AR-1001 / MEP-SUB-01',
        'keywords': ['substation', 'dewa', 'transformer', 'switchgear', 'clear height', 'vehicular access'],
        'expected': 'Dedicated ground-level DEWA substation with direct road access, equipment doors, and 4.0m clear height.',
        'issue_if_missing': False,
        'standard_clause': 'DEWA Electrical Regulations 2017: Transformer and HV rooms require ground road-facing accessibility.',
        'cost_delta': 90000,
        'schedule_delta': '2.0 weeks'
    },
    {
        'id': 'AUTH-DM-GREEN-015',
        'pillar': 'Authority Codes',
        'source': 'Dubai Municipality (Al Safaat Green Building Code)',
        'category': 'Thermal Performance & Glazing',
        'discipline': 'Landscape & Sustainability',
        'severity': 'Medium',
        'drawing_ref': 'SPEC-FACADE-01',
        'keywords': ['u-value', 'shgc', 'thermal', 'glazing', 'insulation', 'al safaat', 'green building'],
        'expected': 'Façade and roof envelope thermal insulation U-values compliant with Al Safaat Silver/Golden standards.',
        'issue_if_missing': True,
        'standard_clause': 'Al Safaat Green Building Code: Roof U-value <= 0.30 W/m²K, Wall U-value <= 0.57 W/m²K, Glazing SHGC <= 0.30.',
        'cost_delta': 110000,
        'schedule_delta': '1.0 week'
    },

    # 3. Ellington Brand Guidelines & Luxury Specs (Feature F3.1)
    {
        'id': 'ELL-BRAND-LOBBY-020',
        'pillar': 'Brand Standards',
        'source': 'Ellington Brand Guidelines 2024',
        'category': 'Signature Arrival & Double-Height Lobby',
        'discipline': 'Brand & Finishes',
        'severity': 'Medium',
        'drawing_ref': 'AR-1001 & AR-3001',
        'keywords': ['lobby', 'entrance', 'double-height', 'arrival', 'concierge', 'drop-off'],
        'expected': 'Signature grand double-height entrance lobby (minimum 6.0m clear ceiling) with dedicated drop-off.',
        'issue_if_missing': True,
        'standard_clause': 'Ellington Brand Standards: Premium hospitality-grade arrival experience with signature double-height volume.',
        'cost_delta': 75000,
        'schedule_delta': '0.5 weeks'
    },
    {
        'id': 'ELL-BRAND-PALETTE-021',
        'pillar': 'Brand Standards',
        'source': 'Ellington Brand Guidelines 2024',
        'category': 'Signature Material Palette & Façade',
        'discipline': 'Brand & Finishes',
        'severity': 'Medium',
        'drawing_ref': 'AR-2001 to AR-2004',
        'keywords': ['material', 'finish', 'travertine', 'bronze', 'terracotta', 'fluted', 'champagne', 'wood'],
        'expected': 'Façade and interior public area specifications featuring Ellington signature 2024 premium material palette.',
        'issue_if_missing': True,
        'standard_clause': 'Ellington Palette 2024: Natural stone / travertine, brushed bronze metallics, and architectural fluted accents.',
        'cost_delta': 180000,
        'schedule_delta': '1.5 weeks'
    },
    {
        'id': 'ELL-BRAND-BALCONY-022',
        'pillar': 'Brand Standards',
        'source': 'Ellington Brand Guidelines 2024',
        'category': 'Balcony Depth & Outdoor Living',
        'discipline': 'Architecture & Façade',
        'severity': 'Low',
        'drawing_ref': 'AR-1006 to AR-1036',
        'keywords': ['balcony', 'terrace', 'outdoor', 'balustrade', 'cantilever', 'glazing'],
        'expected': 'Generous private outdoor balconies with minimum 1.8m usable depth and frameless safety balustrades.',
        'issue_if_missing': True,
        'standard_clause': 'Ellington Residential Standard: Seamless indoor-outdoor living with deep usable balconies.',
        'cost_delta': 45000,
        'schedule_delta': '0.5 weeks'
    },
    {
        'id': 'ELL-BRAND-AMENITY-023',
        'pillar': 'Brand Standards',
        'source': 'Ellington Brand Guidelines 2024',
        'category': 'Resort-Style Amenities & Pool Deck',
        'discipline': 'Landscape & Sustainability',
        'severity': 'Medium',
        'drawing_ref': 'AR-1005 (Level 4 Podium)',
        'keywords': ['infinity pool', 'pool', 'amenity', 'clubhouse', 'fitness', 'spa', 'yoga', 'landscaped podium'],
        'expected': 'Resort-style infinity edge pool, landscaped podium deck, fitness studio, and signature wellness amenities.',
        'issue_if_missing': True,
        'standard_clause': 'Ellington Signature Living: Integrated wellness amenities and hotel-inspired leisure podium.',
        'cost_delta': 95000,
        'schedule_delta': '1.0 week'
    },

    # 4. Cross-Discipline Coordination (Meeting Notes & BRD Scope)
    {
        'id': 'COORD-EXT-STAIR-005',
        'pillar': 'Project Submissions & Packages',
        'source': 'Approved Architectural Master Plan vs Landscape Package',
        'category': 'External Staircase / Landscape Consistency',
        'discipline': 'Landscape & Architecture',
        'severity': 'High',
        'drawing_ref': 'AR-1001 (Ground) vs LS-101 (Landscape)',
        'keywords': ['stair', 'staircase', 'external stair', 'podium stair', 'landscape steps'],
        'expected': 'External staircase connecting podium landscape to ground floor must be consistently reflected in both architectural and landscape submissions.',
        'issue_if_missing': False,
        'standard_clause': 'Cross-Discipline Alignment: External circulation stairs from Master Plan must exist in both Architecture and Landscape drawings.',
        'cost_delta': 45000,
        'schedule_delta': '1.0 week'
    },
    {
        'id': 'COORD-STR-COLUMN-030',
        'pillar': 'Project Submissions & Packages',
        'source': 'Bukadra Plot 6117262 Structural & Architectural Coordination',
        'category': 'Column Grid & Transfer Alignment',
        'discipline': 'Structural',
        'severity': 'High',
        'drawing_ref': 'AR-STR-OVERLAY-01',
        'keywords': ['column', 'grid', 'transfer slab', 'shear wall', 'alignment', 'structural'],
        'expected': 'Structural column grid alignment verified between podium parking levels and upper residential tower.',
        'issue_if_missing': False,
        'standard_clause': 'Engineering Coordination: Tower columns must transfer safely onto podium grid without obstructing drive aisles.',
        'cost_delta': 320000,
        'schedule_delta': '2.5 weeks'
    },
    {
        'id': 'COORD-ACOUSTIC-031',
        'pillar': 'Project Submissions & Packages',
        'source': 'Sample Schematic Package (Infosight Acoustic Report)',
        'category': 'Acoustic Partition & Noise Criteria',
        'discipline': 'Acoustics',
        'severity': 'Medium',
        'drawing_ref': 'ACOUSTIC-RPT-01',
        'keywords': ['acoustic', 'stc', 'noise', 'ambient noise', 'partition', 'iic', 'rw+ctr', 'reverberation'],
        'expected': 'Acoustic design criteria meeting NC 30-35 for bedrooms and minimum STC 55 between adjoining residential units.',
        'issue_if_missing': True,
        'standard_clause': 'Infosight Acoustic Criteria: Inter-tenancy separating walls STC >= 55; bedroom ambient noise <= NC 30.',
        'cost_delta': 65000,
        'schedule_delta': '1.0 week'
    },
]

RULE_BY_ID = {r['id']: r for r in COMPREHENSIVE_RULES}


# ---------------------------------------------------------
# Default Consultant Action Items (Pre-populated for Bukadra)
# ---------------------------------------------------------
DEFAULT_BUKADRA_CONSULTANT_ITEMS = [
    {
        'Item #': 1,
        'Finding ID': 'DCR-SETBACK-001',
        'Drawing Reference': 'AR-1000 / AR-1001',
        'Category': 'Boundary Setbacks',
        'Reference Source': 'Meydan Horizon / Master Plan DCR',
        'Severity': 'High',
        'Standard Clause': 'DCR Cl. 4.2: Minimum 6.0m road setback and 4.5m side plot setbacks required.',
        'Consultant Comment': 'Please provide dimensioned setback annotations on sheets AR-1000 and AR-1001 confirming compliance with Meydan Horizon 6.0m road setback and 4.5m side setbacks.',
        'Reviewer Decision': 'Confirm Issue',
        'Estimated Cost (AED)': 0,
        'Estimated Schedule Impact': '1.0 week'
    },
    {
        'Item #': 2,
        'Finding ID': 'AUTH-DM-PARKING-012',
        'Drawing Reference': 'AR-0030 (Schedules)',
        'Category': 'Parking Ratios & Allocation',
        'Reference Source': 'Dubai Building Code (DBC 2021) / DM',
        'Severity': 'Medium',
        'Standard Clause': 'DM DBC 2021 Part E: Residential parking min 1 bay (1-2 bed), 2 bays (3+ bed) plus 10% visitor provision.',
        'Consultant Comment': 'Please clarify total parking breakdown by apartment type and confirm 35 visitor bays and 9 accessible bays on Sheet AR-0030.',
        'Reviewer Decision': 'Need Clarification',
        'Estimated Cost (AED)': 150000,
        'Estimated Schedule Impact': '1.0 week'
    },
    {
        'Item #': 3,
        'Finding ID': 'AUTH-DCD-EGRESS-010',
        'Drawing Reference': 'FLS-1001 to FLS-1036',
        'Category': 'Fire & Life Safety Egress',
        'Reference Source': 'Dubai Civil Defense (UAE Fire Code 2018)',
        'Severity': 'High',
        'Standard Clause': 'UAE Fire Code 2018 Ch. 3: Max travel distance to nearest enclosed exit stair shall not exceed 30m.',
        'Consultant Comment': 'Provide travel distance path analysis drawing verifying maximum 30m travel distance to exit staircases across all typical floor layouts.',
        'Reviewer Decision': 'Confirm Issue',
        'Estimated Cost (AED)': 120000,
        'Estimated Schedule Impact': '2.0 weeks'
    },
    {
        'Item #': 4,
        'Finding ID': 'ELL-BRAND-PALETTE-021',
        'Drawing Reference': 'AR-2001 to AR-2004',
        'Category': 'Signature Material Palette & Façade',
        'Reference Source': 'Ellington Brand Guidelines 2024',
        'Severity': 'Medium',
        'Standard Clause': 'Ellington Palette 2024: Natural stone / travertine, brushed bronze metallics, and architectural fluted accents.',
        'Consultant Comment': 'Update façade specification schedule to reference Ellington 2024 Signature Travertine Light Classico and Brushed Champagne Bronze accents.',
        'Reviewer Decision': 'Modify & Confirm',
        'Estimated Cost (AED)': 180000,
        'Estimated Schedule Impact': '1.5 weeks'
    },
    {
        'Item #': 5,
        'Finding ID': 'COORD-STR-COLUMN-030',
        'Drawing Reference': 'AR-STR-OVERLAY-01',
        'Category': 'Column Grid & Transfer Alignment',
        'Reference Source': 'Bukadra Plot 6117262 Structural & Architectural Coordination',
        'Severity': 'High',
        'Standard Clause': 'Engineering Coordination: Tower columns must transfer safely onto podium grid without obstructing drive aisles.',
        'Consultant Comment': 'Submit structural overlay drawing confirming column grid transfer between Level 4 Podium and Level 1 typical tower.',
        'Reviewer Decision': 'Need Clarification',
        'Estimated Cost (AED)': 320000,
        'Estimated Schedule Impact': '2.5 weeks'
    }
]


# ---------------------------------------------------------
# Helper Functions & State Management
# ---------------------------------------------------------
def load_knowledge_catalog():
    if not KNOWLEDGE_CATALOG_FILE.exists():
        return []
    try:
        data = json.loads(KNOWLEDGE_CATALOG_FILE.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except Exception:
        return []

def load_stage_history():
    if not STAGE_HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(STAGE_HISTORY_FILE.read_text(encoding='utf-8'))
        return data if isinstance(data, list) else []
    except Exception:
        return []

def save_stage_history(records):
    try:
        STAGE_HISTORY_FILE.write_text(json.dumps(records, indent=2), encoding='utf-8')
    except Exception:
        pass

def upsert_stage_status(project, stage, discipline, status, reviewer='', note='', consultant_data=None):
    records = load_stage_history()
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    norm_stage = clean_stage_name(stage)
    
    match = None
    for rec in records:
        if rec.get('project') == project and clean_stage_name(rec.get('stage')) == norm_stage:
            match = rec
            break
            
    if match is None:
        match = {
            'project': project, 'stage': norm_stage, 'discipline': discipline,
            'status': status, 'reviewer': reviewer, 'note': note,
            'updated_at': now, 'completed_at': now if status.startswith('Completed') else '',
            'consultant_items': consultant_data or []
        }
        records.append(match)
    else:
        match['status'] = status
        match['stage'] = norm_stage
        match['reviewer'] = reviewer or match.get('reviewer', '')
        match['note'] = note or match.get('note', '')
        match['updated_at'] = now
        if status.startswith('Completed'):
            match['completed_at'] = now
        else:
            match['completed_at'] = ''
        if consultant_data:
            match['consultant_items'] = consultant_data
    save_stage_history(records)

def project_stage_rows(project_name):
    records = load_stage_history()
    rows = []
    for stage_name in STAGE_ORDER:
        matches = [
            r for r in records
            if r.get('project') == project_name and clean_stage_name(r.get('stage')) == stage_name
        ]
        if matches:
            matches = sorted(matches, key=lambda x: x.get('updated_at', ''), reverse=True)
            rec = matches[0]
            rows.append({
                'Stage': stage_name,
                'Status': rec.get('status', 'Not Started'),
                'Discipline': rec.get('discipline', '—'),
                'Reviewer': rec.get('reviewer', '—') or '—',
                'Last Updated': rec.get('updated_at', '—')
            })
        else:
            rows.append({
                'Stage': stage_name,
                'Status': 'Not Started',
                'Discipline': '—',
                'Reviewer': '—',
                'Last Updated': '—'
            })
    return pd.DataFrame(rows)

def get_stage_consultant_df(project_name, stage_name, discipline_name):
    records = load_stage_history()
    norm = clean_stage_name(stage_name)
    for r in records:
        if r.get('project') == project_name and clean_stage_name(r.get('stage')) == norm:
            if r.get('consultant_items'):
                return pd.DataFrame(r.get('consultant_items'))
    return pd.DataFrame(DEFAULT_BUKADRA_CONSULTANT_ITEMS)

def get_stage_full_review_df(project_name, stage_name, discipline_name):
    if 'review_df' in st.session_state and not st.session_state['review_df'].empty:
        return st.session_state['review_df']
    
    sample_file = BASE_DIR / "sample_schematic_arch.txt"
    text = sample_file.read_text(encoding='utf-8') if sample_file.exists() else ""
    df = run_ai_review(text)
    cons_map = {item['Finding ID']: item for item in DEFAULT_BUKADRA_CONSULTANT_ITEMS}
    for idx, row in df.iterrows():
        fid = row['Finding ID']
        if fid in cons_map:
            df.at[idx, 'Reviewer Decision'] = cons_map[fid]['Reviewer Decision']
            df.at[idx, 'Consultant Comment'] = cons_map[fid]['Consultant Comment']
            df.at[idx, 'Reviewer Note'] = 'Confirmed by Senior Design Manager.'
        else:
            df.at[idx, 'Reviewer Decision'] = 'Reject AI Finding'
            df.at[idx, 'Reviewer Note'] = 'Acceptable per standard details.'
    return df

def calculate_compliance_score(df):
    """
    Feature F3.3: Compliance Score Calculation
    Weighted formula deducting points for unaddressed gaps.
    """
    score = 100
    for _, row in df.iterrows():
        status = row.get('AI Status')
        sev = row.get('Severity', 'Medium')
        if status == 'Potential Gap':
            if sev == 'High':
                score -= 14
            elif sev == 'Medium':
                score -= 8
            elif sev == 'Low':
                score -= 3
        elif status == 'Needs Baseline Comparison':
            score -= 6
    return max(0, min(100, score))

def complete_current_stage(meta, reviewer='', note='', status='Completed'):
    upsert_stage_status(meta['project'], meta['stage'], meta['discipline'], status, reviewer=reviewer, note=note)
    st.session_state['stage_completed'] = True
    st.session_state['stage_completion_status'] = status
    st.session_state['stage_completion_time'] = datetime.now().strftime('%Y-%m-%d %H:%M')

def extract_text_from_file(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    uploaded_file.seek(0)
    if name.endswith('.txt'):
        return data.decode('utf-8', errors='ignore')
    if name.endswith('.pdf') and PdfReader:
        try:
            reader = PdfReader(BytesIO(data))
            return '\n'.join((p.extract_text() or '') for p in reader.pages)
        except Exception as e:
            return f"Error reading PDF: {e}"
    if name.endswith('.docx') and Document:
        try:
            doc = Document(BytesIO(data))
            return '\n'.join(p.text for p in doc.paragraphs)
        except Exception as e:
            return f"Error reading DOCX: {e}"
    return ''

def snippet(text, keyword, window=140):
    m = re.search(re.escape(keyword), text, flags=re.I)
    if not m:
        return ''
    start = max(0, m.start() - window)
    end = min(len(text), m.end() + window)
    s = re.sub(r'\s+', ' ', text[start:end]).strip()
    return ('…' if start else '') + s + ('…' if end < len(text) else '')

def run_ai_review(text, rules_to_run=COMPREHENSIVE_RULES):
    t = text.lower()
    results = []
    for rule in rules_to_run:
        found_kw = next((kw for kw in rule['keywords'] if kw.lower() in t), None)
        rule_sev = rule.get('severity', 'Medium')
        if found_kw:
            status = 'Evidence Found'
            severity = 'Info' if rule.get('issue_if_missing', True) else 'Needs Comparison'
            finding = f"Confirmed evidence for {rule['category']} detected in submitted package."
            evidence = snippet(text, found_kw)
            confidence = 94 if len(evidence) > 80 else 82
        else:
            if rule.get('issue_if_missing', True):
                status = 'Potential Gap'
                severity = rule_sev
                finding = f"No explicit evidence detected for {rule['category']}. Verification against {rule['source']} required."
                evidence = f"No keyword match found for {', '.join(rule['keywords'][:3])}."
                confidence = 75
            else:
                status = 'Needs Baseline Comparison'
                severity = rule_sev
                finding = f"Cross-discipline verification required against approved baseline master plan / structural sheets."
                evidence = 'Cross-discipline baseline verification needed.'
                confidence = 90

        default_consultant = (
            f"Please verify {rule['category']} against {rule['source']} ({rule.get('standard_clause', '')}) and submit revised drawing / specification."
            if status != 'Evidence Found' else ''
        )
        
        results.append({
            'Finding ID': rule['id'],
            'Pillar': rule['pillar'],
            'Category': rule['category'],
            'Drawing Ref': rule.get('drawing_ref', 'AR-GENERAL'),
            'Reference Source': rule['source'],
            'AI Status': status,
            'Severity': severity,
            'Confidence': f'{confidence}%',
            'AI Finding': finding,
            'Evidence / Reason': evidence,
            'Standard Clause': rule.get('standard_clause', '—'),
            'Cost Delta (AED)': rule.get('cost_delta', 0) if status != 'Evidence Found' else 0,
            'Schedule Impact': rule.get('schedule_delta', '0 wks') if status != 'Evidence Found' else '0 wks',
            'Reviewer Decision': 'Pending Review',
            'Reviewer Note': '',
            'Consultant Comment': default_consultant,
        })
    return pd.DataFrame(results)

def consultant_items(df):
    publishable = ['Confirm Issue', 'Modify & Confirm', 'Need Clarification']
    return df[df['Reviewer Decision'].isin(publishable)].copy()

def compare_resubmission(resub_text, confirmed_df):
    t = resub_text.lower()
    rows = []
    for _, old in confirmed_df.iterrows():
        rule = RULE_BY_ID.get(old['Finding ID'])
        found_kw = next((kw for kw in rule['keywords'] if kw.lower() in t), None) if rule else None
        
        id_found = old['Finding ID'].lower() in t
        
        if id_found or found_kw:
            if old['Reviewer Decision'] == 'Need Clarification':
                delta_status = 'Response / Clarification Detected'
            else:
                delta_status = 'Potentially Resolved'
            evidence = snippet(resub_text, old['Finding ID'] if id_found else found_kw)
        else:
            if old['Reviewer Decision'] == 'Need Clarification':
                delta_status = 'Clarification Still Required'
            else:
                delta_status = 'Still Open / No Evidence Found'
            evidence = 'No matching response or evidence detected in resubmission text.'
            
        rows.append({
            'Finding ID': old['Finding ID'],
            'Category': old['Category'],
            'Drawing Ref': old.get('Drawing Ref', 'AR-GENERAL'),
            'Previous Consultant Comment': old['Consultant Comment'],
            'AI Delta Status': delta_status,
            'Resubmission Evidence': evidence,
            'Final Reviewer Decision': 'Pending Final Review',
            'Final Reviewer Note': '',
        })
    return pd.DataFrame(rows)

def build_comments_tracker_html(df, meta):
    items = consultant_items(df)
    if items.empty:
        rows = "<tr><td colspan='8'>No reviewer-confirmed comments to issue.</td></tr>"
    else:
        rows = ''.join(
            f"<tr><td><b>{idx+1}</b></td><td><b>{r['Finding ID']}</b></td><td>{r.get('Drawing Ref', 'AR-GENERAL')}</td><td>{r['Category']}</td>"
            f"<td>{r['Reference Source']}</td><td><span class='badge-{r['Severity'].lower()}'>{r['Severity']}</span></td>"
            f"<td>{r['Consultant Comment']}</td><td>{r['Reviewer Decision']}</td></tr>"
            for idx, (_, r) in enumerate(items.iterrows())
        )
    return f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>Ellington Properties — Design Comments Tracker</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #1E293B; background: #F8FAFC; }}
    .header {{ background: #0A192F; color: white; padding: 24px; border-radius: 8px; border-bottom: 4px solid #D4AF37; }}
    h1 {{ margin: 0; font-size: 24px; color: #FFFFFF; }}
    .note {{ background: #EFF6FF; border-left: 4px solid #3B82F6; padding: 14px; margin: 20px 0; border-radius: 4px; font-size: 13px; color: #1E40AF; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
    .meta-card {{ background: white; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); }}
    .meta-card b {{ color: #64748B; font-size: 11px; text-transform: uppercase; }}
    .meta-card div {{ font-size: 15px; font-weight: 700; color: #0F172A; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: white; border-radius: 8px; overflow: hidden; }}
    th, td {{ padding: 10px 12px; border: 1px solid #E2E8F0; font-size: 12px; text-align: left; vertical-align: top; }}
    th {{ background: #F1F5F9; color: #0F172A; font-weight: 700; text-transform: uppercase; font-size: 11px; }}
    .badge-high {{ background: #FEE2E2; color: #991B1B; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; }}
    .badge-medium {{ background: #FEF3C7; color: #92400E; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 10px; }}
    .badge-low {{ background: #E0E7FF; color: #3730A3; padding: 3px 8px; border-radius: 4px; font-size: 10px; }}
</style>
</head>
<body>
<div class='header'>
    <h1>Ellington Properties — Design Comments Tracker</h1>
    <p style='margin: 4px 0 0 0; color: #94A3B8; font-size: 13px;'>Formal Design Comment Logging & Consultant Action Register</p>
</div>
<div class='note'>
    <b>Official Review Register:</b> Generated by Ellington AI Design Review Management System. Only Design Manager authorized items appear in this register.
</div>
<div class='meta-grid'>
    <div class='meta-card'><b>Project</b><div>{meta['project']}</div></div>
    <div class='meta-card'><b>Stage</b><div>{meta['stage']}</div></div>
    <div class='meta-card'><b>Discipline</b><div>{meta['discipline']}</div></div>
    <div class='meta-card'><b>Submission</b><div>{meta['version']}</div></div>
</div>
<table>
    <thead>
        <tr><th>Item #</th><th>Finding ID</th><th>Drawing Ref</th><th>Category</th><th>Reference Authority / Standard</th><th>Severity</th><th>Consultant Action Required</th><th>Status</th></tr>
    </thead>
    <tbody>{rows}</tbody>
</table>
</body>
</html>"""

def build_evidence_pack(meta, initial_df, consultant_df, delta_df=None, final_status='Completed'):
    init_rows = ''.join(
        f"<tr><td><b>{r['Finding ID']}</b></td><td>{r.get('Drawing Ref', 'AR-GENERAL')}</td><td>{r['Category']}</td><td>{r['AI Status']}</td><td>{r['Severity']}</td><td>{r['Reviewer Decision']}</td><td>{r['Reviewer Note']}</td></tr>"
        for _, r in initial_df.iterrows()
    )
    cons_rows = ''.join(
        f"<tr><td><b>{r['Finding ID']}</b></td><td>{r.get('Drawing Ref', 'AR-GENERAL')}</td><td>{r['Consultant Comment']}</td><td>{r['Reviewer Decision']}</td></tr>"
        for _, r in consultant_df.iterrows()
    ) if not consultant_df.empty else "<tr><td colspan='4'>No consultant-facing comments generated.</td></tr>"
    
    if delta_df is not None and not delta_df.empty:
        delta_rows = ''.join(
            f"<tr><td><b>{r['Finding ID']}</b></td><td>{r['AI Delta Status']}</td><td>{r['Final Reviewer Decision']}</td><td>{r['Final Reviewer Note']}</td></tr>"
            for _, r in delta_df.iterrows()
        )
    else:
        delta_rows = "<tr><td colspan='4'>No resubmission reviewed yet.</td></tr>"

    return f"""<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<title>Ellington Properties — Full Audit Evidence Pack</title>
<style>
    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; color: #1E293B; background: #F8FAFC; }}
    .header {{ background: #0A192F; color: white; padding: 24px; border-radius: 8px; border-bottom: 4px solid #D4AF37; }}
    h1 {{ margin: 0; font-size: 24px; color: #FFFFFF; }}
    h2 {{ color: #0B315E; font-size: 16px; margin-top: 28px; border-bottom: 2px solid #E2E8F0; padding-bottom: 6px; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin: 20px 0; }}
    .meta-card {{ background: white; border: 1px solid #E2E8F0; padding: 12px; border-radius: 6px; }}
    .meta-card b {{ color: #64748B; font-size: 11px; text-transform: uppercase; }}
    .meta-card div {{ font-size: 15px; font-weight: 700; color: #0F172A; margin-top: 4px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background: white; border-radius: 6px; overflow: hidden; }}
    th, td {{ padding: 10px 12px; border: 1px solid #E2E8F0; font-size: 12px; text-align: left; vertical-align: top; }}
    th {{ background: #F1F5F9; color: #0F172A; font-weight: 700; font-size: 11px; }}
    .status-badge {{ display: inline-block; background: #059669; color: white; padding: 6px 14px; border-radius: 6px; font-weight: bold; font-size: 13px; }}
</style>
</head>
<body>
<div class='header'>
    <h1>Ellington Properties — Complete Audit Evidence Pack</h1>
    <p style='margin: 4px 0 0 0; color: #94A3B8; font-size: 13px;'>Full Lifecycle Audit Trail: AI First-Pass Audit → Design Manager Validation → Consultant Resubmission → Final Sign-Off</p>
</div>
<div style='margin: 20px 0;'>
    <b>Stage Workflow Status:</b> <span class='status-badge'>{final_status}</span>
</div>
<div class='meta-grid'>
    <div class='meta-card'><b>Project</b><div>{meta['project']}</div></div>
    <div class='meta-card'><b>Stage</b><div>{meta['stage']}</div></div>
    <div class='meta-card'><b>Discipline</b><div>{meta['discipline']}</div></div>
    <div class='meta-card'><b>Cycle</b><div>{meta['version']} → Resubmission</div></div>
</div>

<h2>1. AI First-Pass Findings & Design Manager Checkpoint</h2>
<table>
    <thead><tr><th>ID</th><th>Drawing Ref</th><th>Category</th><th>AI Initial Status</th><th>Severity</th><th>Reviewer Decision</th><th>Reviewer Note</th></tr></thead>
    <tbody>{init_rows}</tbody>
</table>

<h2>2. Authorized Consultant Comments Package</h2>
<table>
    <thead><tr><th>ID</th><th>Drawing Ref</th><th>Consultant Comment / Action Required</th><th>Reviewer Status</th></tr></thead>
    <tbody>{cons_rows}</tbody>
</table>

<h2>3. Consultant Resubmission & AI Delta Review</h2>
<table>
    <thead><tr><th>ID</th><th>AI Delta Status</th><th>Final Reviewer Decision</th><th>Final Note</th></tr></thead>
    <tbody>{delta_rows}</tbody>
</table>
</body>
</html>"""


# ---------------------------------------------------------
# Sidebar Navigation & Branding
# ---------------------------------------------------------
PAGES = [
    "📊 Executive Dashboard",
    "🏗️ AI Design Review Studio",
    "✅ Completed Stages & Audit History"
]

if 'nav_radio' not in st.session_state or st.session_state['nav_radio'] not in PAGES:
    st.session_state['nav_radio'] = PAGES[0]

# Handle deferred navigation redirect (set before widget renders)
if st.session_state.get('_nav_redirect'):
    st.session_state['nav_radio'] = st.session_state.pop('_nav_redirect')

with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 12px 0 16px 0;'>
        <div style='font-size: 1.45rem; font-weight: 800; color: #0A192F; font-family: Outfit, sans-serif; letter-spacing: 0.05em;'>ELLINGTON</div>
        <div style='font-size: 0.72rem; color: #AA820A; font-weight: 700; letter-spacing: 0.15em;'>AI DESIGN REVIEW</div>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio(
        "Navigation",
        PAGES,
        key="nav_radio",
        label_visibility="collapsed"
    )
    
    st.divider()
    st.caption("🔒 **Human Authority Gate: Active**")


# ---------------------------------------------------------
# 1. EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if page == "📊 Executive Dashboard":
    st.markdown("""
    <div class='header-banner'>
        <div class='title'>
            <span>Executive Design Review Dashboard</span>
            <span class='gold-badge'>Enterprise</span>
        </div>
        <div class='subtitle'>Portfolio-wide tracking across Concept Design, Schematic Design, Detailed Design, and Tender Package milestones.</div>
    </div>
    """, unsafe_allow_html=True)
    
    records = load_stage_history()
    projects = sorted(list(set(r.get('project') for r in records if r.get('project'))))
    default_projects = ['Ellington Bukadra Tower (Plot 6117262)', 'Ellington Beach House (Palm Jumeirah)', 'Mercer House (Uptown)']
    for p in default_projects:
        if p not in projects:
            projects.append(p)
            
    selected_project = st.selectbox("Select Project Portfolio", projects)
    dash = project_stage_rows(selected_project)
    
    completed_count = int(dash['Status'].astype(str).str.startswith('Completed').sum())
    active_count = int(dash['Status'].isin(['In Review', 'Human Review Complete', 'Consultant Action Required', 'Resubmission Review']).sum())
    not_started = int((dash['Status'] == 'Not Started').sum())
    
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Total Design Stages</div><div class='card-value'>{len(STAGE_ORDER)}</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Stages Completed</div><div class='card-value' style='color:#059669;'>{completed_count}</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Active in Review</div><div class='card-value' style='color:#0284C7;'>{active_count}</div></div>", unsafe_allow_html=True)
    with c4:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Not Started</div><div class='card-value' style='color:#64748B;'>{not_started}</div></div>", unsafe_allow_html=True)
        
    st.markdown("### Stage Progression Matrix")
    st.dataframe(dash, use_container_width=True, hide_index=True)
    
    progress_val = completed_count / len(STAGE_ORDER) if STAGE_ORDER else 0.0
    st.progress(progress_val)
    st.caption(f"**{int(progress_val * 100)}% Milestone Completion** ({completed_count} of {len(STAGE_ORDER)} design stages finalized for {selected_project}).")
    
    # ---------------------------------------------------------
    # ACTIVE STAGE ACTION CENTER
    # ---------------------------------------------------------
    st.divider()
    st.markdown("### ⚡ Active Stage Action Center")
    st.caption("Directly view pending consultant comments, download the comments package, or resume review:")
    
    active_records = [
        r for r in records
        if r.get('project') == selected_project and r.get('status') not in ['Not Started', 'Completed', 'Completed with Open Items']
    ]
    
    if not active_records:
        st.success("✅ No stages currently require action for this project. All stages are either Completed or Not Started.")
    else:
        for act in active_records:
            stage_name = clean_stage_name(act.get('stage'))
            status_val = act.get('status')
            disc_val = act.get('discipline', 'Architecture & Planning')
            rev_val = act.get('reviewer', 'Senior Design Manager')
            upd_val = act.get('updated_at', 'Recent')
            
            with st.container():
                st.markdown(f"""
                <div style='background: #FFFBEB; border: 1px solid #FCD34D; border-left: 6px solid #F59E0B; border-radius: 8px; padding: 18px; margin-bottom: 16px;'>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div style='font-size: 1.2rem; font-weight: 700; color: #92400E; font-family: Outfit, sans-serif;'>
                            ⚠️ {stage_name} — {disc_val}
                        </div>
                        <span style='background: #F59E0B; color: #FFFFFF; padding: 5px 14px; border-radius: 6px; font-size: 0.82rem; font-weight: 700;'>
                            {status_val}
                        </span>
                    </div>
                    <div style='color: #78350F; font-size: 0.88rem; margin-top: 6px;'>
                        <b>Authorizing Reviewer:</b> {rev_val} &nbsp;|&nbsp; <b>Last Updated:</b> {upd_val}
                    </div>
                    <div style='color: #451A03; font-size: 0.86rem; margin-top: 10px; background: rgba(255,255,255,0.75); padding: 10px 14px; border-radius: 6px;'>
                        <b>Workflow State & Next Steps:</b> First-pass AI review was completed and human-confirmed findings were issued to the consultant. 
                        The stage is currently waiting for the consultant's revised submission (e.g. V2.0 Resubmission) to execute the AI Delta Review and achieve final sign-off.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Fetch consultant items
                items_df = get_stage_consultant_df(selected_project, stage_name, disc_val)
                
                with st.expander(f"📋 View {len(items_df)} Confirmed Consultant Action Items for {stage_name}", expanded=True):
                    st.dataframe(items_df, use_container_width=True, hide_index=True)
                
                act_col1, act_col2, act_col3 = st.columns([1.3, 1, 1])
                with act_col1:
                    if st.button(f"🚀 Resume Review in Studio (Ingest Resubmission)", key=f"resume_{stage_name}", type="primary", use_container_width=True):
                        st.session_state['project'] = selected_project
                        st.session_state['stage'] = stage_name
                        st.session_state['discipline'] = disc_val
                        st.session_state['consultant_package_ready'] = True
                        st.session_state['consultant_df'] = items_df
                        st.session_state['review_df'] = get_stage_full_review_df(selected_project, stage_name, disc_val)
                        st.session_state['meta'] = {
                            'project': selected_project,
                            'stage': stage_name,
                            'discipline': disc_val,
                            'version': 'V1.0',
                            'dcr': 'Meydan Horizon / Bukadra DCR'
                        }
                        st.session_state['_nav_redirect'] = "🏗️ AI Design Review Studio"
                        st.rerun()
                with act_col2:
                    report_html = build_comments_tracker_html(get_stage_full_review_df(selected_project, stage_name, disc_val), {'project': selected_project, 'stage': stage_name, 'discipline': disc_val, 'version': 'V1.0'})
                    st.download_button(
                        f"📥 Download Comments Tracker (HTML)",
                        report_html,
                        file_name=f"ellington_comments_tracker_{stage_name.replace(' ', '_')}.html",
                        mime="text/html",
                        key=f"dl_{stage_name}",
                        use_container_width=True
                    )
                with act_col3:
                    with st.popover(f"✅ Fast Complete Stage"):
                        st.caption("Design Manager Override: Complete this stage directly without waiting for resubmission.")
                        fast_note = st.text_input("Sign-off Note", "Design Manager accepted consultant clarification. Stage completed.", key=f"fast_note_{stage_name}")
                        if st.button("Confirm Complete Stage", key=f"confirm_fast_{stage_name}", type="primary"):
                            complete_current_stage(
                                {'project': selected_project, 'stage': stage_name, 'discipline': disc_val},
                                reviewer=rev_val or "Design Manager",
                                note=fast_note,
                                status="Completed"
                            )
                            st.success("Stage marked as Completed!")
                            st.rerun()

    st.divider()
    st.markdown("### Platform Review Capabilities")
    f_c1, f_c2, f_c3, f_c4 = st.columns(4)
    f_c1.info("🔍 **Automated First-Pass Review**\n\nCompliance check against DCRs, UAE Fire Code, and Brand Standards.")
    f_c2.info("📋 **Design Comments Tracker**\n\nOfficial drawing-referenced comment logging with severity.")
    f_c3.info("🎯 **Compliance Scoring**\n\n0–100% weighted score with resubmission threshold triggers.")
    f_c4.info("💰 **Estimated Cost Impact**\n\nEstimated cost impact (AED) and schedule implications for identified compliance gaps.")
    st.stop()


# ---------------------------------------------------------
# 2. KNOWLEDGE BASE EXPLORER
# ---------------------------------------------------------
elif page == "📚 Knowledge Base Explorer (327 Sources)":
    st.markdown("""
    <div class='header-banner'>
        <div class='title'>
            <span>Knowledge Base Explorer</span>
            <span class='gold-badge'>327 Files Ingested</span>
        </div>
        <div class='subtitle'>Real-time searchable library of ingested Authority Codes, DCRs, Brand Standards, and Project Packages.</div>
    </div>
    """, unsafe_allow_html=True)
    
    catalog = load_knowledge_catalog()
    if not catalog:
        st.error("Knowledge catalog not found. Please run index_knowledge.py.")
        st.stop()
        
    df_cat = pd.DataFrame(catalog)
    
    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Total Ingested Files", len(df_cat))
    s2.metric("Authorities & Codes", len(df_cat[df_cat['top_category_display'] == 'Authority Codes']))
    s3.metric("DCR Master Guidelines", len(df_cat[df_cat['top_category_display'] == 'Development Regulations (DCR)']))
    s4.metric("Sample Schematic Sheets", len(df_cat[df_cat['top_category_display'] == 'Project Submissions & Packages']))
    
    st.markdown("### Filter & Search Catalog")
    f1, f2, f3 = st.columns([1.5, 1, 1])
    with f1:
        search_kw = st.text_input("🔍 Search by filename, keyword, code or subfolder", placeholder="e.g. fire, setback, DBC, Meydan, travertine, DEWA...")
    with f2:
        top_cats = ['All Categories'] + sorted(list(df_cat['top_category_display'].unique()))
        sel_top_cat = st.selectbox("Category Pillar", top_cats)
    with f3:
        all_disciplines = ['All Disciplines'] + sorted(list(df_cat['discipline'].unique()))
        sel_discipline = st.selectbox("Discipline", all_disciplines)
        
    filtered = df_cat.copy()
    if sel_top_cat != 'All Categories':
        filtered = filtered[filtered['top_category_display'] == sel_top_cat]
    if sel_discipline != 'All Disciplines':
        filtered = filtered[filtered['discipline'] == sel_discipline]
    if search_kw.strip():
        kw = search_kw.lower()
        filtered = filtered[
            filtered['name'].str.lower().str.contains(kw) |
            filtered['relative_path'].str.lower().str.contains(kw) |
            filtered['sub_category'].str.lower().str.contains(kw)
        ]
        
    st.caption(f"Showing **{len(filtered)}** matching documents from knowledge base:")
    
    display_table = filtered[['id', 'name', 'top_category_display', 'sub_category', 'discipline', 'size_display', 'extension']]
    display_table = display_table.rename(columns={
        'id': 'ID',
        'name': 'Document Name',
        'top_category_display': 'Knowledge Pillar',
        'sub_category': 'Authority / Master Developer',
        'discipline': 'Discipline',
        'size_display': 'Size',
        'extension': 'Type'
    })
    
    st.dataframe(display_table, use_container_width=True, hide_index=True)
    
    with st.expander("📄 Document Inspector & Full Path Lookup"):
        selected_id = st.selectbox("Select Document ID to Inspect", filtered['id'].tolist() if not filtered.empty else [])
        if selected_id:
            row = filtered[filtered['id'] == selected_id].iloc[0]
            st.markdown(f"**Document Name:** `{row['name']}`")
            st.markdown(f"**Knowledge Pillar:** {row['top_category_display']} → `{row['sub_category']}`")
            st.markdown(f"**Discipline:** {row['discipline']}")
            st.markdown(f"**File Size:** {row['size_display']} ({row['extension']} file)")
            st.markdown(f"**Full System Path:** `{row['full_path']}`")
            st.info(f"Applicable to Review Stages: Concept Design, Schematic Design, Detailed Design, Tender Package")
    st.stop()


# ---------------------------------------------------------
# 4. RULE & CLAUSE LIBRARY
# ---------------------------------------------------------
elif page == "📜 Rule & Clause Library":
    st.markdown("""
    <div class='header-banner'>
        <div class='title'>
            <span>Rule & Clause Knowledge Library</span>
            <span class='gold-badge'>17 Active Multi-Discipline Rules</span>
        </div>
        <div class='subtitle'>Automated AI compliance rules mapped against Authority Codes, DCRs, Brand Standards, and Cross-Discipline Memory.</div>
    </div>
    """, unsafe_allow_html=True)
    
    df_rules = pd.DataFrame(COMPREHENSIVE_RULES)
    
    r1, r2 = st.columns([1, 1])
    with r1:
        pillar_filter = st.selectbox("Filter by Knowledge Pillar", ['All Pillars'] + sorted(list(df_rules['pillar'].unique())))
    with r2:
        sev_filter = st.selectbox("Filter by Severity", ['All Severities', 'High', 'Medium', 'Low'])
        
    filtered_rules = df_rules.copy()
    if pillar_filter != 'All Pillars':
        filtered_rules = filtered_rules[filtered_rules['pillar'] == pillar_filter]
    if sev_filter != 'All Severities':
        filtered_rules = filtered_rules[filtered_rules['severity'] == sev_filter]
        
    for _, r in filtered_rules.iterrows():
        with st.container():
            st.markdown(f"#### `{r['id']}` — {r['category']}")
            c1, c2, c3 = st.columns([1, 1, 1])
            c1.markdown(f"**Pillar:** {r['pillar']}")
            c2.markdown(f"**Reference Source:** {r['source']}")
            c3.markdown(f"**Severity:** `{r.get('severity', 'Medium')}` | **Discipline:** {r['discipline']}")
            st.markdown(f"**Typical Drawing Reference:** `{r.get('drawing_ref', 'AR-GENERAL')}`")
            st.markdown(f"**Standard Requirement / Clause:** {r['standard_clause']}")
            st.markdown(f"**Expected Submission Evidence:** {r['expected']}")
            st.markdown(f"**Estimated Change Impact:** Cost: `AED {r.get('cost_delta', 0):,}` | Schedule: `{r.get('schedule_delta', '0 wks')}`")
            st.caption(f"Target Keywords: {', '.join(r['keywords'])}")
            st.divider()
    st.stop()


# ---------------------------------------------------------
# 5. COMPLETED STAGES & AUDIT HISTORY
# ---------------------------------------------------------
elif page == "✅ Completed Stages & Audit History":
    st.markdown("""
    <div class='header-banner'>
        <div class='title'>
            <span>Completed Stages & Audit Trail</span>
            <span class='gold-badge'>Persistent Ledger</span>
        </div>
        <div class='subtitle'>Full immutable audit history of completed design reviews and Design Manager authorizations.</div>
    </div>
    """, unsafe_allow_html=True)
    
    records = [r for r in load_stage_history() if str(r.get('status', '')).startswith('Completed')]
    if not records:
        st.info("No stages have been completed yet. Run an AI Review in the Design Review Studio and sign off on a stage to populate this ledger.")
    else:
        completed_df = pd.DataFrame(records)
        completed_df['stage'] = completed_df['stage'].apply(clean_stage_name)
        display = completed_df.rename(columns={
            'project': 'Project',
            'stage': 'Design Stage',
            'discipline': 'Discipline',
            'status': 'Workflow Status',
            'reviewer': 'Authorizing Reviewer',
            'note': 'Sign-off Note',
            'completed_at': 'Completed Timestamp'
        })
        cols = [c for c in ['Project', 'Design Stage', 'Discipline', 'Workflow Status', 'Authorizing Reviewer', 'Sign-off Note', 'Completed Timestamp'] if c in display.columns]
        st.dataframe(display[cols], use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Audit Trail (CSV)",
            display[cols].to_csv(index=False),
            file_name="ellington_completed_design_stages.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.stop()


# ---------------------------------------------------------
# 3. AI DESIGN REVIEW STUDIO (MAIN WORKFLOW)
# ---------------------------------------------------------
st.markdown("""
<div class='header-banner'>
    <div class='title'>
        <span>Ellington AI Design Review Studio</span>
        <span class='gold-badge'>Human-in-the-Loop AI</span>
    </div>
    <div class='subtitle'>AI-assisted first-pass review, comments tracking, compliance scoring, and delta analysis.</div>
</div>
""", unsafe_allow_html=True)

# Active Session Notification
if st.session_state.get('consultant_package_ready'):
    meta_loaded = st.session_state.get('meta', {})
    st.markdown(f"""
    <div style='background: #EFF6FF; border: 1px solid #BFDBFE; border-left: 5px solid #2563EB; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='font-size: 1rem; font-weight: 700; color: #1E40AF;'>
                📌 Active Session Loaded: {meta_loaded.get('project', 'Ellington Bukadra Tower')} — {meta_loaded.get('stage', 'Schematic Design')}
            </div>
            <span style='background: #2563EB; color: #FFFFFF; padding: 3px 10px; border-radius: 5px; font-size: 0.75rem; font-weight: 700;'>
                Consultant Action Required
            </span>
        </div>
        <div style='color: #1E3A8A; font-size: 0.85rem; margin-top: 4px;'>
            The consultant communication package has been prepared. Review the confirmed items in <b>Step 5 (Comments Tracker)</b> or proceed to <b>Step 6</b> to ingest the revised consultant resubmission (V2.0) and run AI Delta Review.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class='process-container'>
    <div class='process-step active'><span class='step-num'>1</span> Ingestion & Context</div>
    <div class='process-step active'><span class='step-num'>2</span> AI First-Pass Review</div>
    <div class='process-step active'><span class='step-num'>3</span> Compliance Scoring & Impact</div>
    <div class='process-step active'><span class='step-num'>4</span> Human Checkpoint</div>
    <div class='process-step active'><span class='step-num'>5</span> Comments Tracker</div>
    <div class='process-step active'><span class='step-num'>6</span> Delta Review & Sign-Off</div>
</div>
""", unsafe_allow_html=True)

# Step 1: Project & Knowledge Configuration
left_col, right_col = st.columns([1, 1])
with left_col:
    st.subheader("1. Project Context & Stage Setup")
    project = st.text_input("Project Name", st.session_state.get('project', 'Ellington Bukadra Tower (Plot 6117262)'))
    
    dcr_options = [
        "Meydan Horizon / Bukadra DCR",
        "Dubai Hills Estate (DHE) DCR",
        "Business Bay DCR",
        "Nakheel Jumeirah Village Circle (JVC) DCR",
        "Dubai Islands DCR",
        "Marjan Island Beach District DCR",
        "Downtown Jebel Ali DCR",
        "Sobha Hartland Master Plan DCR"
    ]
    master_dcr = st.selectbox("Master Developer DCR Framework", dcr_options)
    
    stage_idx = 1
    current_saved_stage = clean_stage_name(st.session_state.get('stage', 'Schematic Design'))
    if current_saved_stage in STAGE_ORDER:
        stage_idx = STAGE_ORDER.index(current_saved_stage)
    stage = st.selectbox("Design Stage", STAGE_ORDER, index=stage_idx)
    
    discipline_options = ['Architecture & Planning', 'Fire & Life Safety (FLS)', 'Structural', 'MEP & Utilities', 'Acoustics', 'Multi-disciplinary']
    disc_idx = 0
    if st.session_state.get('discipline') in discipline_options:
        disc_idx = discipline_options.index(st.session_state.get('discipline'))
    discipline = st.selectbox("Discipline", discipline_options, index=disc_idx)
    
    version = st.text_input("Submission Version", st.session_state.get('version', 'V1.0'))

with right_col:
    st.subheader("2. Drawing Package Input")
    st.markdown("Choose a pre-indexed sample from the **Sample Schematic Design Package** or upload your own file:")
    
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🏢 Load Bukadra Arch Package", use_container_width=True):
            sample_file = BASE_DIR / "sample_schematic_arch.txt"
            if sample_file.exists():
                st.session_state['loaded_sample_text'] = sample_file.read_text(encoding='utf-8')
                st.session_state['loaded_sample_name'] = "015-24_Bukadra_Plot_6117262_Schematic_Architecture_V1.txt"
                st.success("Loaded Bukadra Architectural Package!")
    with b2:
        if st.button("🚒 Load Bukadra FLS Package", use_container_width=True):
            sample_file = BASE_DIR / "sample_schematic_fls.txt"
            if sample_file.exists():
                st.session_state['loaded_sample_text'] = sample_file.read_text(encoding='utf-8')
                st.session_state['loaded_sample_name'] = "01524-XYZ-B01-FLS-Egress-Strategy_V1.txt"
                st.success("Loaded Bukadra FLS Package!")
    with b3:
        if st.button("🔊 Load Acoustics & Struct", use_container_width=True):
            sample_file = BASE_DIR / "sample_schematic_acoustics_struct.txt"
            if sample_file.exists():
                st.session_state['loaded_sample_text'] = sample_file.read_text(encoding='utf-8')
                st.session_state['loaded_sample_name'] = "Infosight_Acoustic_Structural_Report_V1.txt"
                st.success("Loaded Acoustics & Structural Package!")

    uploaded = st.file_uploader("Or Upload PDF / DOCX / TXT Submission", type=['pdf', 'docx', 'txt'], key='initial_upload')
    
    if 'loaded_sample_name' in st.session_state:
        st.info(f"Active Drawing Package: **{st.session_state['loaded_sample_name']}**")

st.markdown("#### Active Knowledge Grounding Sources")
g1, g2, g3, g4 = st.columns(4)
g1.success(f"**Authority Code**\n\nDubai Municipality DBC 2021 & UAE Fire Code")
g2.success(f"**DCR Master Plan**\n\n{master_dcr.split(' ')[0]} Master Framework")
g3.success(f"**Brand Standards**\n\nEllington 2024 Luxury Guidelines")
g4.success(f"**Cross-Discipline Memory**\n\nPlot 6117262 Approved Baseline")

if st.button("🚀 Run AI First-Pass Review", type="primary", use_container_width=True):
    raw_text = ""
    file_label = ""
    if uploaded:
        raw_text = extract_text_from_file(uploaded)
        file_label = uploaded.name
    elif 'loaded_sample_text' in st.session_state:
        raw_text = st.session_state['loaded_sample_text']
        file_label = st.session_state.get('loaded_sample_name', 'Sample Submission')
    else:
        sample_file = BASE_DIR / "sample_schematic_arch.txt"
        if sample_file.exists():
            raw_text = sample_file.read_text(encoding='utf-8')
            file_label = "015-24_Bukadra_Plot_6117262_Schematic_Architecture_V1.txt"
        
    if raw_text.strip():
        st.session_state['review_df'] = run_ai_review(raw_text)
        st.session_state['meta'] = {'project': project, 'stage': stage, 'discipline': discipline, 'version': version, 'dcr': master_dcr}
        st.session_state['filename'] = file_label
        st.session_state['initial_text'] = raw_text
        st.session_state['stage_completed'] = False
        upsert_stage_status(project, stage, discipline, 'In Review')
        st.session_state.pop('consultant_package_ready', None)
        st.session_state.pop('delta_df', None)
        st.session_state.pop('final_signed_off', None)
        st.rerun()

# ---------------------------------------------------------
# Step 2 & 3: Findings, Compliance Scoring & Impact Assessment
# ---------------------------------------------------------
if 'review_df' in st.session_state:
    df = st.session_state['review_df']
    meta = st.session_state['meta']
    
    st.divider()
    st.subheader("3. AI First-Pass Review Summary & Automated Intelligence")
    
    compliance_score = calculate_compliance_score(df)
    resub_threshold = 80
    resub_triggered = compliance_score < resub_threshold
    
    total_cost_delta = df['Cost Delta (AED)'].sum()
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        score_color = "#059669" if compliance_score >= 80 else "#DC2626"
        st.markdown(f"<div class='metric-card'><div class='card-label'>Compliance Score</div><div class='card-value' style='color:{score_color};'>{compliance_score}%</div></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Compliance Gaps / Issues</div><div class='card-value' style='color:#DC2626;'>{int((df['AI Status'] == 'Potential Gap').sum())}</div></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Estimated Cost Impact (AED)</div><div class='card-value'>AED {total_cost_delta:,}</div></div>", unsafe_allow_html=True)
    with m4:
        st.markdown(f"<div class='metric-card'><div class='card-label'>Cross-Discipline Checks</div><div class='card-value' style='color:#0284C7;'>{int((df['AI Status'] == 'Needs Baseline Comparison').sum())}</div></div>", unsafe_allow_html=True)

    if resub_triggered:
        st.warning(f"⚠️ **Automated Resubmission Trigger:** Package compliance score ({compliance_score}%) is below the {resub_threshold}% review threshold. Consultant resubmission is indicated pending Design Manager confirmation.")
    else:
        st.success(f"✅ **Compliance Score Acceptable:** Package score ({compliance_score}%) meets the {resub_threshold}% review threshold.")
        
    st.caption("ℹ️ **Change Impact Disclaimer:** All cost and schedule impacts are AI-generated advisory estimates pending QS / PM validation.")

    st.subheader("4. Human Checkpoint — Design Manager Authorization")
    st.markdown("""
    <div class='human-box'>
        <b>Design Manager Authority Gate:</b> AI findings are internal only. Design Managers must review each item and set the decision to <b>Confirm Issue</b>, <b>Reject AI Finding</b>, <b>Modify & Confirm</b>, or <b>Need Clarification</b>. Only confirmed items will be logged in the Comments Tracker.
    </div>
    """, unsafe_allow_html=True)
    
    edited = st.data_editor(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Finding ID': st.column_config.TextColumn('ID', width='small', disabled=True),
            'Drawing Ref': st.column_config.TextColumn('Drawing Ref', width='small', disabled=True),
            'Category': st.column_config.TextColumn('Category', width='medium', disabled=True),
            'Reference Source': st.column_config.TextColumn('Authority / DCR Source', width='medium', disabled=True),
            'AI Status': st.column_config.TextColumn('AI Status', width='small', disabled=True),
            'Severity': st.column_config.TextColumn('Severity', width='small', disabled=True),
            'Cost Delta (AED)': st.column_config.NumberColumn('Estimated Cost Impact (AED)', format="AED %d", disabled=True),
            'Schedule Impact': st.column_config.TextColumn('Est. Schedule', width='small', disabled=True),
            'Standard Clause': st.column_config.TextColumn('Applicable Clause', width='medium', disabled=True),
            'Reviewer Decision': st.column_config.SelectboxColumn(
                'Reviewer Decision',
                options=['Pending Review', 'Confirm Issue', 'Reject AI Finding', 'Modify & Confirm', 'Need Clarification'],
                width='medium',
                required=True
            ),
            'Reviewer Note': st.column_config.TextColumn('Internal Reviewer Note', width='medium'),
            'Consultant Comment': st.column_config.TextColumn('Consultant-Facing Comment', width='large'),
        },
        key='review_editor_v5'
    )
    st.session_state['review_df'] = edited
    
    with st.expander("🔍 View Extracted Drawing Package Text Extract"):
        st.text(st.session_state.get('initial_text', '')[:5000])
        
    publishable = consultant_items(edited)
    pending = int((edited['Reviewer Decision'] == 'Pending Review').sum())
    
    a1, a2, a3 = st.columns(3)
    a1.metric("Confirmed Action Items", len(publishable))
    a2.metric("Rejected False Alarms", int((edited['Reviewer Decision'] == 'Reject AI Finding').sum()))
    a3.metric("Pending Reviewer Decisions", pending)
    
    if pending == 0:
        upsert_stage_status(meta['project'], meta['stage'], meta['discipline'], 'Human Review Complete', consultant_data=publishable.to_dict('records') if not publishable.empty else [])
        st.success("All reviewer decisions have been recorded. You can complete the stage if no items require consultant action, or proceed to generate the official Comments Tracker.")
        
        comp_note = st.text_area("Stage Completion Note (optional)", placeholder="e.g. Schematic Design human review verified; compliance score acceptable.")
        if publishable.empty:
            if st.button("✅ Complete Stage", type="primary", use_container_width=True, key="comp_stage_no_issues"):
                complete_current_stage(meta, reviewer="Senior Design Manager", note=comp_note, status="Completed")
                st.rerun()
        else:
            upsert_stage_status(meta['project'], meta['stage'], meta['discipline'], 'Consultant Action Required', consultant_data=publishable.to_dict('records'))
            st.warning("Reviewer-confirmed findings exist. Standard process: Issue Comments Tracker to consultant and review resubmission.")
            override_chk = st.checkbox("I confirm the Design Manager is intentionally completing this stage with open action items.", key='override_stage_close')
            if st.button("Complete Stage with Open Items", disabled=not override_chk, use_container_width=True, key="comp_stage_with_open_btn"):
                complete_current_stage(meta, reviewer="Senior Design Manager", note=comp_note or "Stage closed with open consultant-action items.", status="Completed with Open Items")
                st.rerun()

    if st.session_state.get('stage_completed'):
        st.info(f"Stage status: **{st.session_state.get('stage_completion_status')}**. View details in the Executive Dashboard.")

    if st.button("📤 Generate Official Comments Tracker", use_container_width=True, type="primary"):
        if publishable.empty:
            st.error("No reviewer-confirmed or clarification items found to log in the Comments Tracker.")
        else:
            st.session_state['consultant_package_ready'] = True
            st.session_state['consultant_df'] = publishable
            upsert_stage_status(meta['project'], meta['stage'], meta['discipline'], 'Consultant Action Required', consultant_data=publishable.to_dict('records'))
            st.rerun()

# ---------------------------------------------------------
# Step 4 & 5: Comments Tracker & Resubmission Input
# ---------------------------------------------------------
if st.session_state.get('consultant_package_ready'):
    meta = st.session_state.get('meta', {
        'project': project,
        'stage': stage,
        'discipline': discipline,
        'version': version,
        'dcr': master_dcr
    })
    
    st.divider()
    st.subheader("5. Official Design Comments Tracker")
    st.markdown("""
    <div class='client-box'>
        <b>Client & Consultant Facing Register:</b> Formatted strictly per Ellington Design Review standards. Only authorized comments appear in this register.
    </div>
    """, unsafe_allow_html=True)
    
    if 'consultant_df' in st.session_state:
        cons_df = st.session_state['consultant_df']
    else:
        cons_df = get_stage_consultant_df(meta['project'], meta['stage'], meta['discipline'])
        st.session_state['consultant_df'] = cons_df
        
    cols_to_show = ['Finding ID', 'Drawing Ref', 'Category', 'Reference Source', 'Severity', 'Standard Clause', 'Consultant Comment', 'Reviewer Decision']
    cols_available = [c for c in cols_to_show if c in cons_df.columns]
    st.dataframe(cons_df[cols_available], use_container_width=True, hide_index=True)
    
    review_df_to_use = st.session_state.get('review_df', get_stage_full_review_df(meta['project'], meta['stage'], meta['discipline']))
    report_html = build_comments_tracker_html(review_df_to_use, meta)
    
    dl_c1, dl_c2 = st.columns(2)
    with dl_c1:
        st.download_button(
            "📥 Download Comments Tracker (HTML)",
            report_html,
            file_name=f"ellington_comments_tracker_{meta['stage'].replace(' ', '_')}.html",
            mime="text/html",
            use_container_width=True
        )
    with dl_c2:
        st.download_button(
            "📥 Download Comments Tracker (CSV)",
            cons_df.to_csv(index=False),
            file_name=f"ellington_comments_tracker_{meta['stage'].replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    st.subheader("6. Consultant Resubmission Ingestion")
    r1, r2 = st.columns([1, 1])
    with r1:
        resub_ver = st.text_input("Resubmission Version", "V2.0")
        resub_note = st.text_area("Consultant Cover Letter / Response Summary", placeholder="e.g. Setback schedule added to Sheet AR-1000; parking layout revised to provide 412 bays; FLS egress paths highlighted.")
    with r2:
        st.markdown("Quick-load sample resubmission or upload revised file:")
        if st.button("🏢 Load Bukadra V2.0 Resubmission Sample", use_container_width=True):
            resub_sample_file = BASE_DIR / "sample_schematic_resubmission_v2.txt"
            if resub_sample_file.exists():
                st.session_state['loaded_resub_text'] = resub_sample_file.read_text(encoding='utf-8')
                st.session_state['loaded_resub_name'] = "015-24_Bukadra_Resubmission_Package_V2.0.txt"
                st.success("Loaded Bukadra V2.0 Resubmission!")
                
        resub_upload = st.file_uploader("Or Upload Revised PDF / DOCX / TXT", type=['pdf', 'docx', 'txt'], key='resub_upload')
        if 'loaded_resub_name' in st.session_state:
            st.info(f"Active Resubmission Sample: **{st.session_state['loaded_resub_name']}**")

    if st.button("🔄 Run AI Delta Review on Resubmission", type="primary", use_container_width=True):
        resub_text = ""
        if resub_upload:
            resub_text = extract_text_from_file(resub_upload)
        elif 'loaded_resub_text' in st.session_state:
            resub_text = st.session_state['loaded_resub_text']
        else:
            resub_sample_file = BASE_DIR / "sample_schematic_resubmission_v2.txt"
            if resub_sample_file.exists():
                resub_text = resub_sample_file.read_text(encoding='utf-8')
                
        if resub_text.strip():
            st.session_state['delta_df'] = compare_resubmission(resub_text, cons_df)
            st.session_state['resub_version'] = resub_ver
            st.session_state['consultant_response'] = resub_note
            st.session_state['resub_text'] = resub_text
            upsert_stage_status(meta['project'], meta['stage'], meta['discipline'], 'Resubmission Review')
            st.rerun()

# ---------------------------------------------------------
# Step 6 & 7: Delta Review & Final Sign-Off
# ---------------------------------------------------------
if 'delta_df' in st.session_state:
    delta = st.session_state['delta_df']
    meta = st.session_state.get('meta', {'project': project, 'stage': stage, 'discipline': discipline, 'version': version})
    
    st.divider()
    st.subheader("7. AI Delta Review — Resubmission vs Confirmed Items")
    
    res_count = int(delta['AI Delta Status'].isin(['Potentially Resolved', 'Response / Clarification Detected']).sum())
    open_count = int(delta['AI Delta Status'].isin(['Still Open / No Evidence Found', 'Clarification Still Required']).sum())
    
    d1, d2 = st.columns(2)
    d1.metric("Potentially Resolved / Responses Detected", res_count, delta="Evidence Verified")
    d2.metric("Still Open / Missing Responses", open_count, delta="Action Required", delta_color="inverse")
    
    final_edited = st.data_editor(
        delta,
        use_container_width=True,
        hide_index=True,
        column_config={
            'Finding ID': st.column_config.TextColumn('ID', width='small', disabled=True),
            'Drawing Ref': st.column_config.TextColumn('Drawing Ref', width='small', disabled=True),
            'Category': st.column_config.TextColumn('Category', width='medium', disabled=True),
            'Previous Consultant Comment': st.column_config.TextColumn('Issued Comment', width='large', disabled=True),
            'AI Delta Status': st.column_config.TextColumn('AI Delta Status', width='medium', disabled=True),
            'Resubmission Evidence': st.column_config.TextColumn('Detected Resubmission Evidence', width='large', disabled=True),
            'Final Reviewer Decision': st.column_config.SelectboxColumn(
                'Final Reviewer Decision',
                options=['Pending Final Review', 'Close Finding', 'Keep Open', 'Request Another Resubmission'],
                width='medium',
                required=True
            ),
            'Final Reviewer Note': st.column_config.TextColumn('Final Reviewer Note', width='large'),
        },
        key='final_delta_editor_v5'
    )
    st.session_state['delta_df'] = final_edited
    
    with st.expander("🔍 View Extracted Resubmission Text"):
        st.text(st.session_state.get('resub_text', '')[:5000])
        
    st.subheader("8. Final Milestone Sign-Off & Project Memory Integration")
    
    f_pending = int((final_edited['Final Reviewer Decision'] == 'Pending Final Review').sum())
    f_open = int(final_edited['Final Reviewer Decision'].isin(['Keep Open', 'Request Another Resubmission']).sum())
    f_closed = int((final_edited['Final Reviewer Decision'] == 'Close Finding').sum())
    
    x1, x2, x3 = st.columns(3)
    x1.metric("Closed Findings", f_closed)
    x2.metric("Remaining Open", f_open)
    x3.metric("Pending Final Decision", f_pending)
    
    signoff_person = st.text_input("Authorizing Senior Design Manager", "Senior Design Manager — Architecture")
    final_stage_note = st.text_area("Final Stage Sign-Off Record", f"All material compliance comments addressed satisfactorily in {st.session_state.get('resub_version', 'V2.0')} submission. {meta['stage']} approved.")
    
    close_btn_label = f"✅ Sign-Off & Complete {meta['stage']}" if f_open == 0 else f"Complete {meta['stage']} with Open Items"
    override_allowed = True
    if f_open > 0:
        st.warning("Some findings remain open. Completing this stage will record it as 'Completed with Open Items'.")
        override_allowed = st.checkbox("I confirm authorization to complete the milestone with open action items.", key='final_override_chk')
        
    if st.button(close_btn_label, type="primary" if f_open == 0 else "secondary", disabled=not override_allowed, use_container_width=True):
        if f_pending > 0:
            st.error("Please record a final decision for all items in the table above before signing off.")
        else:
            final_status_str = "Completed" if f_open == 0 else "Completed with Open Items"
            st.session_state['final_signed_off'] = True
            st.session_state['signoff_name'] = signoff_person
            st.session_state['final_note'] = final_stage_note
            st.session_state['final_status'] = final_status_str
            complete_current_stage(meta, reviewer=signoff_person, note=final_stage_note, status=final_status_str)
            st.rerun()

# ---------------------------------------------------------
# Step 8: Final Completion Evidence Pack Export
# ---------------------------------------------------------
if st.session_state.get('final_signed_off'):
    meta = st.session_state.get('meta', {'project': project, 'stage': stage, 'discipline': discipline, 'version': version})
    final_stat = st.session_state.get('final_status', 'Completed')
    
    st.divider()
    st.subheader(f"9. Milestone Finalized — Project Memory & Audit Evidence Pack")
    st.success(f"🎉 {meta['stage']} finalized successfully. Recorded Status: **{final_stat}**")
    
    memory_table = pd.DataFrame([
        ['Project Name', meta['project']],
        ['Design Milestone', meta['stage']],
        ['Discipline', meta['discipline']],
        ['DCR Framework', meta.get('dcr', 'Meydan Horizon DCR')],
        ['Initial Submission', meta['version']],
        ['Resubmission Version', st.session_state.get('resub_version', 'V2.0')],
        ['Authorizing Reviewer', st.session_state.get('signoff_name', 'Senior Design Manager')],
        ['Final Stage Status', final_stat],
        ['Authorization Timestamp', datetime.now().strftime('%Y-%m-%d %H:%M')],
        ['Sign-off Summary', st.session_state.get('final_note', '')],
    ], columns=['Project Memory Field', 'Value'])
    
    st.dataframe(memory_table, use_container_width=True, hide_index=True)
    
    evidence_html = build_evidence_pack(
        meta,
        st.session_state.get('review_df', get_stage_full_review_df(meta['project'], meta['stage'], meta['discipline'])),
        st.session_state.get('consultant_df', pd.DataFrame()),
        st.session_state.get('delta_df'),
        final_stat
    )
    
    st.download_button(
        "📥 Download Full Audit Evidence Pack (HTML)",
        evidence_html,
        file_name=f"ellington_{meta['project'].replace(' ', '_')}_{meta['stage'].replace(' ', '_')}_evidence_pack.html",
        mime="text/html",
        use_container_width=True
    )
    
    st.info("💡 **Project Memory Retained:** This finalized dataset is now persisted in `stage_history.json` and automatically carried forward to subsequent stages (e.g. Detailed Design & Tender Package) for cross-discipline and baseline consistency checking.")
    
    if st.button("🔄 Start New Design Review Cycle", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
