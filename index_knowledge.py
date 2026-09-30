import os
import json
from pathlib import Path

ONEDRIVE_DIR = r"C:\Users\Sharath\OneDrive - WISSDA CONSULTING PRIVATE LIMITED\Sharath\AI Design"
OUTPUT_FILE = Path(__file__).parent / "knowledge_catalog.json"

CATEGORY_MAPPING = {
    "Authority Design Codes and Guidelines": "Authority Codes",
    "Development Control Regulations (DCR)": "Development Regulations (DCR)",
    "Ellington Brand Guidelines": "Brand Standards",
    "Sample Schematic Design Package": "Project Submissions & Packages"
}

def format_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def index_repository(root_path):
    catalog = []
    root = Path(root_path)
    if not root.exists():
        print(f"Error: Directory not found: {root_path}")
        return catalog

    for p in root.rglob("*"):
        if p.is_file():
            rel_path = p.relative_to(root)
            parts = rel_path.parts
            top_category = parts[0] if len(parts) > 0 else "General"
            sub_category = parts[1] if len(parts) > 2 else (parts[0] if len(parts) > 1 else "Root")
            
            discipline = "Multi-disciplinary"
            name_lower = p.name.lower()
            
            if "arch" in name_lower or "facade" in name_lower or "façade" in name_lower or "building" in name_lower:
                discipline = "Architecture & Façade"
            elif "fls" in name_lower or "fire" in name_lower or "safety" in name_lower or "dcd" in name_lower:
                discipline = "Fire & Life Safety"
            elif "str" in name_lower or "structure" in name_lower or "slab" in name_lower or "column" in name_lower:
                discipline = "Structural"
            elif "mep" in name_lower or "dewa" in name_lower or "electrical" in name_lower or "lpg" in name_lower:
                discipline = "MEP & Utilities"
            elif "acoustic" in name_lower:
                discipline = "Acoustics"
            elif "landscape" in name_lower or "green" in name_lower or "safaat" in name_lower:
                discipline = "Landscape & Sustainability"
            elif "hotel" in name_lower or "dtcm" in name_lower or "resort" in name_lower:
                discipline = "Hospitality / Commercial"
            elif "brand" in name_lower or "colour" in name_lower or "color" in name_lower:
                discipline = "Brand & Finishes"
            elif "dcr" in name_lower or "planning" in name_lower or "guideline" in name_lower or "regulation" in name_lower:
                discipline = "Planning & Regulations"

            item = {
                "id": f"KB-{len(catalog) + 1:04d}",
                "name": p.name,
                "relative_path": str(rel_path).replace("\\", "/"),
                "full_path": str(p),
                "top_category": top_category,
                "top_category_display": CATEGORY_MAPPING.get(top_category, top_category),
                "sub_category": sub_category,
                "extension": p.suffix.lower(),
                "size_bytes": p.stat().st_size,
                "size_display": format_size(p.stat().st_size),
                "discipline": discipline,
                "applicable_stages": ["Concept Design", "Schematic Design", "Detailed Design", "Tender Package"],
            }
            catalog.append(item)

    return catalog

if __name__ == "__main__":
    print(f"Scanning directory: {ONEDRIVE_DIR}")
    catalog = index_repository(ONEDRIVE_DIR)
    print(f"Indexed {len(catalog)} files.")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
    print(f"Saved catalog to: {OUTPUT_FILE}")
