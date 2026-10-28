import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
wb.remove(wb.active)  # remove default sheet

# 1. Dim_Equipment
ws_dim = wb.create_sheet(title="Dim_Equipment")
dim_headers = ["equipment_id", "equipment_name", "category", "serial_number", "base_storage_hub", "status", "assigned_owner"]
ws_dim.append(dim_headers)

sample_equipment = [
    ("EQ-1001", "Heavy Generator 15kW", "Power", "SN-GEN-8831", "Hub Alpha (Main)", "Operational", "John Doe"),
    ("EQ-1002", "Satellite Comm Terminal", "Telecom", "SN-SAT-4412", "Hub Bravo", "In Transit", "Alice Smith"),
    ("EQ-1003", "Diagnostic Scan Tool v4", "Maintenance", "SN-DIAG-9901", "Hub Charlie", "Operational", "Robert Johnson"),
    ("EQ-1004", "Hydraulic Lift Unit 5T", "Machinery", "SN-HYD-1120", "Hub Alpha (Main)", "Operational", "David Lee"),
    ("EQ-1005", "Rugged Field Laptop Toughbook", "IT", "SN-LAP-7723", "Hub Delta", "Operational", "Alice Smith"),
    ("EQ-1006", "Thermal Imaging Camera", "Inspection", "SN-THM-3329", "Hub Echo", "Operational", "Emily Davis"),
    ("EQ-1007", "High-Pressure Air Compressor", "Pneumatic", "SN-AIR-5541", "Hub Foxtrot", "In Transit", "Michael Brown"),
    ("EQ-1008", "Portable Water Filtration Rig", "Utilities", "SN-WTR-2209", "Hub Golf", "Operational", "John Doe"),
    ("EQ-1009", "Radio Repeater Base Station", "Telecom", "SN-RAD-6611", "Hub Hotel", "Operational", "Robert Johnson"),
    ("EQ-1010", "Digital Oscilloscope Lab-Grade", "Electronics", "SN-OSC-4488", "Hub India", "Operational", "David Lee"),
    ("EQ-1011", "Emergency Hazmat Response Kit", "Safety", "SN-HAZ-0012", "Hub Juliet", "Operational", "Emily Davis"),
    ("EQ-1012", "Surveying Total Station GPS", "Geodetic", "SN-SUR-7711", "Hub Kilo", "Operational", "Michael Brown"),
    ("EQ-1013", "Industrial Welder Inverter", "Machinery", "SN-WLD-8802", "Hub Lima", "Operational", "John Doe"),
    ("EQ-1014", "Deep-Cycle Battery Bank 48V", "Power", "SN-BAT-5590", "Hub Alpha (Main)", "Needs Inspection", "Unassigned"),
    ("EQ-1015", "Spare Fiber Optic Splicer", "Telecom", "SN-FBR-1133", "Hub Bravo", "Unassigned", "Unassigned"),
]

for row in sample_equipment:
    ws_dim.append(row)

# 2. Fact_Assignments (Tracking 12 Hubs, 6 Travel Destinations, 12 Vehicles, Containers)
ws_fact = wb.create_sheet(title="Fact_Assignments")
fact_headers = [
    "assignment_id", "equipment_id", "equipment_name", "serial_number",
    "person_responsible", "current_location", "travel_destination",
    "transport_mode", "vehicle_id", "container_serial", "manifest_status"
]
ws_fact.append(fact_headers)

sample_facts = [
    ("ASG-001", "EQ-1001", "Heavy Generator 15kW", "SN-GEN-8831", "John Doe", "Hub Alpha (Main)", "Site Alpha (North)", "Vehicle Only", "VEH-01 (Ford F550)", "N/A", "Loaded"),
    ("ASG-002", "EQ-1002", "Satellite Comm Terminal", "SN-SAT-4412", "Alice Smith", "In Transit", "Site Bravo (East)", "Container Sea/Air", "N/A", "CONT-SEA-8812", "In Cargo"),
    ("ASG-003", "EQ-1003", "Diagnostic Scan Tool v4", "SN-DIAG-9901", "Robert Johnson", "Hub Charlie", "Site Charlie (South)", "Vehicle Only", "VEH-03 (Dodge 4500)", "N/A", "Loaded"),
    ("ASG-004", "EQ-1004", "Hydraulic Lift Unit 5T", "SN-HYD-1120", "David Lee", "Hub Alpha (Main)", "Site Delta (West)", "Container Sea/Air", "N/A", "CONT-AIR-4401", "Staged"),
    ("ASG-005", "EQ-1005", "Rugged Field Laptop Toughbook", "SN-LAP-7723", "Alice Smith", "Hub Delta", "Site Echo (Central)", "Vehicle Only", "VEH-05 (Toyota Hilux)", "N/A", "Loaded"),
    ("ASG-006", "EQ-1006", "Thermal Imaging Camera", "SN-THM-3329", "Emily Davis", "Hub Echo", "Site Foxtrot (Offshore)", "Container Sea/Air", "N/A", "CONT-SEA-9920", "Packed"),
    ("ASG-007", "EQ-1007", "High-Pressure Air Compressor", "SN-AIR-5541", "Michael Brown", "In Transit", "Site Alpha (North)", "Container Sea/Air", "N/A", "CONT-SEA-8812", "In Cargo"),
    ("ASG-008", "EQ-1008", "Portable Water Filtration Rig", "SN-WTR-2209", "John Doe", "Hub Golf", "Site Bravo (East)", "Vehicle Only", "VEH-08 (Freightliner)", "N/A", "Loaded"),
    ("ASG-009", "EQ-1009", "Radio Repeater Base Station", "SN-RAD-6611", "Robert Johnson", "Hub Hotel", "Site Charlie (South)", "Container Sea/Air", "N/A", "CONT-AIR-4401", "Staged"),
    ("ASG-010", "EQ-1010", "Digital Oscilloscope Lab-Grade", "SN-OSC-4488", "David Lee", "Hub India", "Site Delta (West)", "Vehicle Only", "VEH-10 (Kenworth T880)", "N/A", "Loaded"),
    ("ASG-011", "EQ-1011", "Emergency Hazmat Response Kit", "SN-HAZ-0012", "Emily Davis", "Hub Juliet", "Site Echo (Central)", "Vehicle Only", "VEH-11 (GMC 3500)", "N/A", "Staged"),
    ("ASG-012", "EQ-1012", "Surveying Total Station GPS", "SN-SUR-7711", "Michael Brown", "Hub Kilo", "Site Foxtrot (Offshore)", "Container Sea/Air", "N/A", "CONT-SEA-9920", "Packed"),
    ("ASG-013", "EQ-1013", "Industrial Welder Inverter", "SN-WLD-8802", "John Doe", "Hub Lima", "Site Alpha (North)", "Vehicle Only", "VEH-02 (RAM 5500)", "N/A", "Loaded"),
    ("ASG-014", "EQ-1014", "Deep-Cycle Battery Bank 48V", "SN-BAT-5590", "Unassigned", "Hub Alpha (Main)", "Unassigned", "Unassigned", "UNASSIGNED", "UNASSIGNED", "Pending Disposition"),
    ("ASG-015", "EQ-1015", "Spare Fiber Optic Splicer", "SN-FBR-1133", "Unassigned", "Hub Bravo", "Unassigned", "Unassigned", "UNASSIGNED", "UNASSIGNED", "Pending Disposition")
]

for row in sample_facts:
    ws_fact.append(row)

# 3. Dashboard Tab (Interactive Summary & KPIs)
ws_dash = wb.create_sheet(title="Dashboard")
ws_dash["A1"] = "EQUIPMENT FLEET & LOGISTICS COMMAND DASHBOARD"
ws_dash["A1"].font = Font(name="Calibri", size=16, bold=True, color="1F497D")

# Summary KPI Blocks
kpis = [
    ("Total Equipment Tracked", "=COUNTA(Dim_Equipment!A2:A100)", "A3", "B3"),
    ("Operational Items", '=COUNTIF(Dim_Equipment!F2:F100, "Operational")', "C3", "D3"),
    ("In Transit Items", '=COUNTIF(Dim_Equipment!F2:F100, "In Transit")', "E3", "F3"),
    ("Pending Disposition / Unassigned", '=COUNTIF(Fact_Assignments!K2:K100, "Pending Disposition")', "G3", "H3"),
    ("Total Storage Hubs", "12 Hubs Active", "A5", "B5"),
    ("Travel Destinations", "6 Site Locations", "C5", "D5"),
    ("Transport Vehicles", "12 Dedicated Trucks", "E5", "F5"),
    ("Cargo Containers", "3 Active Containers", "G5", "H5")
]

for label, val, c1, c2 in kpis:
    ws_dash[c1] = label
    ws_dash[c1].font = Font(size=9, bold=True, color="595959")
    ws_dash[c2] = val
    ws_dash[c2].font = Font(size=14, bold=True, color="002060")

ws_dash["A8"] = "OPERATIONAL DISCREPANCY AUDIT & RECONCILIATION"
ws_dash["A8"].font = Font(size=12, bold=True, color="C00000")

ws_dash["A10"] = "Audit Category"
ws_dash["B10"] = "Status"
ws_dash["C10"] = "Impacted ID"
ws_dash["D10"] = "Audit Findings"
ws_dash["E10"] = "Action Required"

audit_headers_cells = ["A10", "B10", "C10", "D10", "E10"]
for c in audit_headers_cells:
    ws_dash[c].font = Font(size=10, bold=True, color="FFFFFF")
    ws_dash[c].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")

audit_rows = [
    ("Unassigned Equipment", "FLAGGED", "EQ-1014", "Deep-Cycle Battery Bank 48V has no assigned owner", "Assign personnel in Dim_Equipment"),
    ("Pending Disposition", "FLAGGED", "EQ-1015", "Spare Fiber Optic Splicer has no travel destination", "Assign destination site or warehouse hold"),
    ("Missing Serial Audit", "PASS", "ALL", "100% equipment items have verified serial numbers", "None - Audit verified"),
    ("Container Integrity", "PASS", "ALL", "Container serials match shipping manifest", "None - Audit verified")
]
for idx, r in enumerate(audit_rows, start=11):
    ws_dash[f"A{idx}"] = r[0]
    ws_dash[f"B{idx}"] = r[1]
    ws_dash[f"C{idx}"] = r[2]
    ws_dash[f"D{idx}"] = r[3]
    ws_dash[f"E{idx}"] = r[4]
    if r[1] == "FLAGGED":
        ws_dash[f"B{idx}"].font = Font(bold=True, color="C00000")
    else:
        ws_dash[f"B{idx}"].font = Font(bold=True, color="008000")

# 4. Manifest_Print Tab (Formatted for A4 Printing)
ws_print = wb.create_sheet(title="Manifest_Print")
ws_print["A1"] = "OFFICIAL CARGO & TRANSPORT EQUIPMENT MANIFEST"
ws_print["A1"].font = Font(size=16, bold=True, color="000000")

ws_print["A3"] = "Manifest ID:"
ws_print["B3"] = "MNF-2026-OCT-089"
ws_print["D3"] = "Date / Time:"
ws_print["E3"] = "2026-10-28 14:00 UTC"

ws_print["A4"] = "Transport Type:"
ws_print["B4"] = "Containerized Sea/Air Cargo"
ws_print["D4"] = "Destination:"
ws_print["E4"] = "Site Alpha (North)"

ws_print["A5"] = "Container / Flight #:"
ws_print["B5"] = "CONT-SEA-8812"
ws_print["D5"] = "Officer in Charge:"
ws_print["E5"] = "John Doe"

manifest_headers = ["Item #", "Equipment ID", "Equipment Description", "Serial Number", "Assigned Person", "Loaded Status", "Verification Signature"]
for col_idx, h in enumerate(manifest_headers, start=1):
    c = ws_print.cell(row=7, column=col_idx, value=h)
    c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    c.fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
    c.alignment = Alignment(horizontal="center", vertical="center")

manifest_items = [
    (1, "EQ-1001", "Heavy Generator 15kW", "SN-GEN-8831", "John Doe", "VERIFIED LOADED", "[     SIGNED     ]"),
    (2, "EQ-1007", "High-Pressure Air Compressor", "SN-AIR-5541", "Michael Brown", "VERIFIED LOADED", "[     SIGNED     ]"),
    (3, "EQ-1013", "Industrial Welder Inverter", "SN-WLD-8802", "John Doe", "VERIFIED LOADED", "[     SIGNED     ]"),
]
for row_idx, item in enumerate(manifest_items, start=8):
    for col_idx, val in enumerate(item, start=1):
        c = ws_print.cell(row=row_idx, column=col_idx, value=val)
        c.alignment = Alignment(horizontal="center" if col_idx in [1, 2, 4, 6, 7] else "left")

# Polish styling across all sheets
header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
border_thin = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9")
)

for ws in [ws_dim, ws_fact]:
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            cell.border = border_thin
            if cell.row == 1:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

for ws in [ws_dash, ws_print]:
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = 22

out_path = "C:/Projects/b2b-saas-affiliate-engine/Equipment_Master_Tracker_Prototype.xlsx"
wb.save(out_path)
print(f"SUCCESS: Generated {out_path}")
