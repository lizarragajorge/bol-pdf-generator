"""PDF templates for Bill of Lading documents using ReportLab."""

import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from data_generator import (
    BolData, InvoiceData, PackingListData, DeliveryOrderData,
    CoverLetterData, FreightManifestData,
)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(name="BolTitle", fontSize=14, leading=17, alignment=1,
                          spaceAfter=6, fontName="Helvetica-Bold"))
    ss.add(ParagraphStyle(name="BolSubtitle", fontSize=10, leading=12, alignment=1,
                          spaceAfter=4, fontName="Helvetica"))
    ss.add(ParagraphStyle(name="FieldLabel", fontSize=7, leading=9,
                          fontName="Helvetica-Bold", textColor=colors.HexColor("#333333")))
    ss.add(ParagraphStyle(name="FieldValue", fontSize=8, leading=10,
                          fontName="Helvetica"))
    ss.add(ParagraphStyle(name="SmallText", fontSize=6, leading=7,
                          fontName="Helvetica", textColor=colors.gray))
    return ss


def _header_table(data: BolData, title: str, styles, color: colors.Color):
    """Render a standard header block with title and BoL number."""
    title_para = Paragraph(title, styles["BolTitle"])
    subtitle = Paragraph(data.shipping_line, styles["BolSubtitle"])
    bol_label = Paragraph("B/L No.", styles["FieldLabel"])
    bol_val = Paragraph(f"<b>{data.bol_number}</b>", styles["FieldValue"])
    booking_label = Paragraph("Booking No.", styles["FieldLabel"])
    booking_val = Paragraph(data.booking_number, styles["FieldValue"])

    t = Table([
        [title_para, bol_label],
        [subtitle, bol_val],
        ["", booking_label],
        ["", booking_val],
    ], colWidths=[4.5 * inch, 2.5 * inch])
    t.setStyle(TableStyle([
        ("SPAN", (0, 0), (0, 1)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOX", (0, 0), (-1, -1), 1.5, color),
        ("LINEBELOW", (0, 0), (-1, 0), 0.5, color),
        ("BACKGROUND", (0, 0), (-1, 0), color),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t


def _party_block(label: str, name: str, address: str, styles):
    return [
        Paragraph(label, styles["FieldLabel"]),
        Paragraph(f"<b>{name}</b>", styles["FieldValue"]),
        Paragraph(address, styles["FieldValue"]),
    ]


# ---------------------------------------------------------------------------
# Template 1: Ocean Bill of Lading
# ---------------------------------------------------------------------------

def render_ocean_bol(data: BolData, filepath: str):
    """Classic ocean freight BoL with structured table layout."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#003366")
    elements = []

    # Header
    elements.append(_header_table(data, "BILL OF LADING", styles, accent))
    elements.append(Spacer(1, 8))

    # Parties block: shipper | consignee | notify
    shipper = _party_block("Shipper / Exporter", data.shipper_name, data.shipper_address, styles)
    consignee = _party_block("Consignee", data.consignee_name, data.consignee_address, styles)
    notify = _party_block("Notify Party", data.notify_party_name, data.notify_party_address, styles)

    party_data = []
    for i in range(3):
        party_data.append([shipper[i], consignee[i], notify[i]])

    party_table = Table(party_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    party_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(party_table)
    elements.append(Spacer(1, 6))

    # Vessel / port info
    vessel_data = [
        [Paragraph("Vessel Name", styles["FieldLabel"]),
         Paragraph("Voyage No.", styles["FieldLabel"]),
         Paragraph("Port of Loading", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"])],
        [Paragraph(data.vessel_name, styles["FieldValue"]),
         Paragraph(data.voyage_number, styles["FieldValue"]),
         Paragraph(data.port_of_loading, styles["FieldValue"]),
         Paragraph(data.port_of_discharge, styles["FieldValue"])],
        [Paragraph("Place of Receipt", styles["FieldLabel"]),
         Paragraph("Place of Delivery", styles["FieldLabel"]),
         Paragraph("Date of Shipment", styles["FieldLabel"]),
         Paragraph("Freight Terms", styles["FieldLabel"])],
        [Paragraph(data.place_of_receipt, styles["FieldValue"]),
         Paragraph(data.place_of_delivery, styles["FieldValue"]),
         Paragraph(data.date_of_shipment, styles["FieldValue"]),
         Paragraph(data.freight_terms, styles["FieldValue"])],
    ]
    vt = Table(vessel_data, colWidths=[1.875 * inch] * 4)
    vt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(vt)
    elements.append(Spacer(1, 6))

    # Container / cargo table
    cargo_header = [
        Paragraph("Container No.", styles["FieldLabel"]),
        Paragraph("Seal No.", styles["FieldLabel"]),
        Paragraph("Type", styles["FieldLabel"]),
        Paragraph("Packages", styles["FieldLabel"]),
        Paragraph("Description of Goods", styles["FieldLabel"]),
        Paragraph("Gross Wt (KG)", styles["FieldLabel"]),
        Paragraph("Volume (CBM)", styles["FieldLabel"]),
    ]
    cargo_rows = [cargo_header]
    for c in data.containers:
        cargo_rows.append([
            Paragraph(c.container_number, styles["FieldValue"]),
            Paragraph(c.seal_number, styles["FieldValue"]),
            Paragraph(c.container_type, styles["FieldValue"]),
            Paragraph(f"{c.packages} {c.package_type}", styles["FieldValue"]),
            Paragraph(c.commodity, styles["FieldValue"]),
            Paragraph(f"{c.gross_weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(f"{c.volume_cbm:,.2f}", styles["FieldValue"]),
        ])
    # Totals row
    cargo_rows.append([
        Paragraph("<b>TOTAL</b>", styles["FieldValue"]),
        "", "",
        Paragraph(f"<b>{data.total_packages}</b>", styles["FieldValue"]),
        "",
        Paragraph(f"<b>{data.total_weight_kg:,.2f}</b>", styles["FieldValue"]),
        Paragraph(f"<b>{data.total_volume_cbm:,.2f}</b>", styles["FieldValue"]),
    ])

    ct = Table(cargo_rows, colWidths=[1.1 * inch, 0.9 * inch, 0.7 * inch, 1.0 * inch,
                                       1.3 * inch, 1.0 * inch, 0.9 * inch])
    ct.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e6eef5")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (0, -1), (-1, -1), 0.75, accent),
    ]))
    elements.append(Paragraph("PARTICULARS FURNISHED BY SHIPPER", styles["FieldLabel"]))
    elements.append(Spacer(1, 2))
    elements.append(ct)
    elements.append(Spacer(1, 8))

    # Special instructions
    if data.special_instructions:
        elements.append(Paragraph("Special Instructions:", styles["FieldLabel"]))
        elements.append(Paragraph(data.special_instructions, styles["FieldValue"]))
        elements.append(Spacer(1, 6))

    # Footer / signatures
    footer_data = [
        [Paragraph("Date of Issue", styles["FieldLabel"]),
         Paragraph("Place of Issue", styles["FieldLabel"]),
         Paragraph("Incoterm", styles["FieldLabel"]),
         Paragraph("Signature", styles["FieldLabel"])],
        [Paragraph(data.date_of_issue, styles["FieldValue"]),
         Paragraph(data.port_of_loading, styles["FieldValue"]),
         Paragraph(data.incoterm, styles["FieldValue"]),
         Paragraph("_________________________", styles["FieldValue"])],
    ]
    ft = Table(footer_data, colWidths=[1.875 * inch] * 4)
    ft.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(ft)
    elements.append(Spacer(1, 6))

    # Legal text
    legal = ("RECEIVED by the Carrier the Goods as specified above in apparent good order and "
             "condition unless otherwise stated, to be transported to such place as agreed, "
             "authorized or permitted herein and subject to all the terms and conditions appearing "
             "on the front and reverse of this Bill of Lading. IN WITNESS WHEREOF the number of "
             "original Bills of Lading stated on this document have been signed, one of which being "
             "accomplished, the others to stand void.")
    elements.append(Paragraph(legal, styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template 2: Truck / Inland Bill of Lading (Straight BoL)
# ---------------------------------------------------------------------------

def render_truck_bol(data: BolData, filepath: str):
    """US-style straight truck Bill of Lading."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#2d5f2d")
    elements = []

    # Title
    title = Paragraph("STRAIGHT BILL OF LADING — SHORT FORM", styles["BolTitle"])
    elements.append(title)
    elements.append(Paragraph("ORIGINAL — NOT NEGOTIABLE", styles["BolSubtitle"]))
    elements.append(Spacer(1, 8))

    # Top info row
    top_data = [
        [Paragraph("Date", styles["FieldLabel"]),
         Paragraph("B/L Number", styles["FieldLabel"]),
         Paragraph("PRO Number", styles["FieldLabel"]),
         Paragraph("Carrier", styles["FieldLabel"])],
        [Paragraph(data.date_of_issue, styles["FieldValue"]),
         Paragraph(data.bol_number, styles["FieldValue"]),
         Paragraph(data.pro_number, styles["FieldValue"]),
         Paragraph(data.carrier_name, styles["FieldValue"])],
    ]
    tt = Table(top_data, colWidths=[1.7 * inch, 1.9 * inch, 1.7 * inch, 2.2 * inch])
    tt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f0e8")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(tt)
    elements.append(Spacer(1, 6))

    # Ship From / Ship To
    from_to = [
        [Paragraph("<b>SHIP FROM</b>", styles["FieldLabel"]),
         Paragraph("<b>SHIP TO</b>", styles["FieldLabel"])],
        [Paragraph(data.shipper_name, styles["FieldValue"]),
         Paragraph(data.consignee_name, styles["FieldValue"])],
        [Paragraph(data.shipper_address, styles["FieldValue"]),
         Paragraph(data.consignee_address, styles["FieldValue"])],
        [Paragraph(f"Origin: {data.origin_city}", styles["FieldValue"]),
         Paragraph(f"Destination: {data.destination_city}", styles["FieldValue"])],
    ]
    ft_table = Table(from_to, colWidths=[3.75 * inch, 3.75 * inch])
    ft_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f0e8")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(ft_table)
    elements.append(Spacer(1, 6))

    # Third-party billing / trailer
    third_data = [
        [Paragraph("Third Party Freight Charges Bill To:", styles["FieldLabel"]),
         Paragraph("Trailer No.", styles["FieldLabel"]),
         Paragraph("Driver Name", styles["FieldLabel"])],
        [Paragraph(data.notify_party_name + "\n" + data.notify_party_address, styles["FieldValue"]),
         Paragraph(data.trailer_number, styles["FieldValue"]),
         Paragraph(data.driver_name, styles["FieldValue"])],
    ]
    tdt = Table(third_data, colWidths=[3.0 * inch, 2.25 * inch, 2.25 * inch])
    tdt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(tdt)
    elements.append(Spacer(1, 6))

    # Cargo table
    cargo_header = [
        Paragraph("QTY", styles["FieldLabel"]),
        Paragraph("Type", styles["FieldLabel"]),
        Paragraph("Weight (KG)", styles["FieldLabel"]),
        Paragraph("Description of Articles", styles["FieldLabel"]),
        Paragraph("NMFC #", styles["FieldLabel"]),
        Paragraph("Class", styles["FieldLabel"]),
    ]
    cargo_rows = [cargo_header]
    # Generate 1-5 line items for truck
    num_items = random.randint(1, 5)
    from data_generator import COMMODITIES, PACKAGE_TYPES
    for _ in range(num_items):
        qty = random.randint(1, 200)
        wt = round(random.uniform(50, 5000), 1)
        cargo_rows.append([
            Paragraph(str(qty), styles["FieldValue"]),
            Paragraph(random.choice(PACKAGE_TYPES), styles["FieldValue"]),
            Paragraph(f"{wt:,.1f}", styles["FieldValue"]),
            Paragraph(random.choice(COMMODITIES), styles["FieldValue"]),
            Paragraph(str(random.randint(40000, 189999)), styles["FieldValue"]),
            Paragraph(str(random.choice([50, 55, 60, 65, 70, 77.5, 85, 92.5, 100, 110, 125, 150, 175, 200, 250, 300, 400, 500])), styles["FieldValue"]),
        ])

    ct = Table(cargo_rows, colWidths=[0.7 * inch, 1.0 * inch, 1.0 * inch, 2.5 * inch, 1.0 * inch, 0.8 * inch])
    ct.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8f0e8")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(cargo_header_para := Paragraph("DESCRIPTION OF ARTICLES, SPECIAL MARKS & EXCEPTIONS", styles["FieldLabel"]))
    elements.append(Spacer(1, 2))
    elements.append(ct)
    elements.append(Spacer(1, 8))

    # Special instructions
    if data.special_instructions:
        elements.append(Paragraph(f"Special Instructions: {data.special_instructions}", styles["FieldValue"]))
        elements.append(Spacer(1, 6))

    # COD / Freight section
    cod_data = [
        [Paragraph("Freight Charges", styles["FieldLabel"]),
         Paragraph("COD Amount", styles["FieldLabel"]),
         Paragraph("Fee Terms", styles["FieldLabel"])],
        [Paragraph(data.freight_terms, styles["FieldValue"]),
         Paragraph("$0.00", styles["FieldValue"]),
         Paragraph(data.incoterm, styles["FieldValue"])],
    ]
    cod_t = Table(cod_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    cod_t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(cod_t)
    elements.append(Spacer(1, 10))

    # Signatures
    sig_data = [
        [Paragraph("Shipper Signature", styles["FieldLabel"]),
         Paragraph("Carrier Signature", styles["FieldLabel"]),
         Paragraph("Consignee Signature", styles["FieldLabel"])],
        [Paragraph("_________________________", styles["FieldValue"]),
         Paragraph("_________________________", styles["FieldValue"]),
         Paragraph("_________________________", styles["FieldValue"])],
        [Paragraph(f"Date: {data.date_of_issue}", styles["SmallText"]),
         Paragraph(f"Date: {data.date_of_shipment}", styles["SmallText"]),
         Paragraph("Date: _______________", styles["SmallText"])],
    ]
    st = Table(sig_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    st.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, accent),
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(st)

    # Legal
    elements.append(Spacer(1, 6))
    legal = ("Subject to the classifications and lawfully filed tariffs in effect on the date "
             "of the issue of this Bill of Lading. The agreed or declared value of the property "
             "is hereby specifically stated by the shipper to be not exceeding the released value "
             "per package as provided in the applicable tariff.")
    elements.append(Paragraph(legal, styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template 3: Short-Form Bill of Lading
# ---------------------------------------------------------------------------

def render_short_bol(data: BolData, filepath: str):
    """Condensed short-form BoL — single-page compact layout."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.3 * inch, bottomMargin=0.3 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#800020")
    elements = []

    # Compact header
    hdr = Table([
        [Paragraph(f"<b>{data.shipping_line}</b>", styles["BolSubtitle"]),
         Paragraph(f"B/L: <b>{data.bol_number}</b>", styles["FieldValue"])],
        [Paragraph("SHORT FORM BILL OF LADING — NON-NEGOTIABLE", styles["BolTitle"]), ""],
    ], colWidths=[5.0 * inch, 2.5 * inch])
    hdr.setStyle(TableStyle([
        ("SPAN", (0, 1), (1, 1)),
        ("BOX", (0, 0), (-1, -1), 1.5, accent),
        ("BACKGROUND", (0, 1), (-1, 1), accent),
        ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(hdr)
    elements.append(Spacer(1, 6))

    # 2-col party info
    party = [
        [Paragraph("<b>Shipper</b>", styles["FieldLabel"]),
         Paragraph("<b>Consignee</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.shipper_name}<br/>{data.shipper_address}", styles["FieldValue"]),
         Paragraph(f"{data.consignee_name}<br/>{data.consignee_address}", styles["FieldValue"])],
        [Paragraph("<b>Notify Party</b>", styles["FieldLabel"]),
         Paragraph("<b>Booking / Reference</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.notify_party_name}<br/>{data.notify_party_address}", styles["FieldValue"]),
         Paragraph(f"Booking: {data.booking_number}<br/>Voyage: {data.voyage_number}", styles["FieldValue"])],
    ]
    pt = Table(party, colWidths=[3.75 * inch, 3.75 * inch])
    pt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 4))

    # Routing row
    route = [
        [Paragraph("Vessel", styles["FieldLabel"]),
         Paragraph("Port of Loading", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"]),
         Paragraph("Freight", styles["FieldLabel"])],
        [Paragraph(data.vessel_name, styles["FieldValue"]),
         Paragraph(data.port_of_loading, styles["FieldValue"]),
         Paragraph(data.port_of_discharge, styles["FieldValue"]),
         Paragraph(data.freight_terms, styles["FieldValue"])],
    ]
    rt = Table(route, colWidths=[2.0 * inch, 2.0 * inch, 2.0 * inch, 1.5 * inch])
    rt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 4))

    # Cargo — compact
    cargo_header = [
        Paragraph("Container", styles["FieldLabel"]),
        Paragraph("Seal", styles["FieldLabel"]),
        Paragraph("Pkgs", styles["FieldLabel"]),
        Paragraph("Description", styles["FieldLabel"]),
        Paragraph("Weight (KG)", styles["FieldLabel"]),
        Paragraph("CBM", styles["FieldLabel"]),
    ]
    cargo_rows = [cargo_header]
    for c in data.containers:
        cargo_rows.append([
            Paragraph(c.container_number, styles["FieldValue"]),
            Paragraph(c.seal_number, styles["FieldValue"]),
            Paragraph(str(c.packages), styles["FieldValue"]),
            Paragraph(c.commodity, styles["FieldValue"]),
            Paragraph(f"{c.gross_weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(f"{c.volume_cbm:,.2f}", styles["FieldValue"]),
        ])

    ct = Table(cargo_rows, colWidths=[1.3 * inch, 1.0 * inch, 0.6 * inch, 2.0 * inch, 1.1 * inch, 0.8 * inch])
    ct.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f5e6ea")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(ct)
    elements.append(Spacer(1, 6))

    # Totals + signature line
    totals = [
        [Paragraph(f"Total Packages: <b>{data.total_packages}</b>", styles["FieldValue"]),
         Paragraph(f"Total Weight: <b>{data.total_weight_kg:,.2f} KG</b>", styles["FieldValue"]),
         Paragraph(f"Total Volume: <b>{data.total_volume_cbm:,.2f} CBM</b>", styles["FieldValue"]),
         Paragraph(f"Date: {data.date_of_issue}", styles["FieldValue"])],
    ]
    tt = Table(totals, colWidths=[2.0 * inch, 2.0 * inch, 2.0 * inch, 1.5 * inch])
    tt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(tt)
    elements.append(Spacer(1, 10))

    # Compact legal
    legal = ("This is a non-negotiable short form Bill of Lading. All terms, conditions and "
             "exceptions of the Carrier's applicable long form Bill of Lading are incorporated "
             "herein by reference.")
    elements.append(Paragraph(legal, styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template 4: FIATA Multimodal Transport Bill of Lading
# ---------------------------------------------------------------------------

def render_multimodal_bol(data: BolData, filepath: str):
    """FIATA-style multimodal / combined transport BoL."""
    doc = SimpleDocTemplate(filepath, pagesize=A4,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#4a235a")
    elements = []

    # Header with FIATA-style branding
    hdr_data = [
        [Paragraph("NEGOTIABLE MULTIMODAL TRANSPORT<br/>BILL OF LADING", styles["BolTitle"]),
         Paragraph(f"<b>FBL No.</b><br/>{data.bol_number}", styles["FieldValue"])],
        [Paragraph(f"Issued by: {data.shipping_line}", styles["BolSubtitle"]),
         Paragraph(f"Booking Ref: {data.booking_number}", styles["FieldValue"])],
    ]
    hdr = Table(hdr_data, colWidths=[4.5 * inch, 2.3 * inch])
    hdr.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 2, accent),
        ("BACKGROUND", (0, 0), (0, 0), accent),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("LINEBELOW", (0, 0), (-1, 0), 1, accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(hdr)
    elements.append(Spacer(1, 6))

    # Consignment parties — 4-quad layout
    quad = [
        [Paragraph("<b>Consignor / Shipper</b>", styles["FieldLabel"]),
         Paragraph("<b>Consignee (or Order)</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.shipper_name}<br/>{data.shipper_address}", styles["FieldValue"]),
         Paragraph(f"{data.consignee_name}<br/>{data.consignee_address}", styles["FieldValue"])],
        [Paragraph("<b>Notify Party / Address</b>", styles["FieldLabel"]),
         Paragraph("<b>Delivery Contact</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.notify_party_name}<br/>{data.notify_party_address}", styles["FieldValue"]),
         Paragraph(f"{data.consignee_name}<br/>Tel: {'+1-' + '-'.join([str(random.randint(100,999)), str(random.randint(100,999)), str(random.randint(1000,9999))])}", styles["FieldValue"])],
    ]
    qt = Table(quad, colWidths=[3.4 * inch, 3.4 * inch])
    qt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0e6f6")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f0e6f6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(qt)
    elements.append(Spacer(1, 4))

    # Transport details
    transport_modes = random.choice([
        "SEA / ROAD", "SEA / RAIL", "AIR / ROAD", "SEA / ROAD / RAIL", "ROAD / SEA"
    ])
    transport_data = [
        [Paragraph("Place of Receipt", styles["FieldLabel"]),
         Paragraph("Port of Loading", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"]),
         Paragraph("Place of Delivery", styles["FieldLabel"]),
         Paragraph("Mode of Transport", styles["FieldLabel"])],
        [Paragraph(data.place_of_receipt, styles["FieldValue"]),
         Paragraph(data.port_of_loading, styles["FieldValue"]),
         Paragraph(data.port_of_discharge, styles["FieldValue"]),
         Paragraph(data.place_of_delivery, styles["FieldValue"]),
         Paragraph(transport_modes, styles["FieldValue"])],
        [Paragraph("Pre-carriage by", styles["FieldLabel"]),
         Paragraph("Ocean Vessel / Voyage", styles["FieldLabel"]),
         Paragraph("", styles["FieldLabel"]),
         Paragraph("On-carriage by", styles["FieldLabel"]),
         Paragraph("Freight Terms", styles["FieldLabel"])],
        [Paragraph("TRUCK", styles["FieldValue"]),
         Paragraph(f"{data.vessel_name} / V.{data.voyage_number}", styles["FieldValue"]),
         Paragraph("", styles["FieldValue"]),
         Paragraph(random.choice(["TRUCK", "RAIL", "BARGE"]), styles["FieldValue"]),
         Paragraph(data.freight_terms, styles["FieldValue"])],
    ]
    trt = Table(transport_data, colWidths=[1.36 * inch] * 5)
    trt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0e6f6")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#f0e6f6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(trt)
    elements.append(Spacer(1, 4))

    # Goods description table
    elements.append(Paragraph("PARTICULARS DECLARED BY THE CONSIGNOR — CARRIER NOT RESPONSIBLE FOR ACCURACY", styles["FieldLabel"]))
    elements.append(Spacer(1, 2))
    goods_header = [
        Paragraph("Marks & Numbers", styles["FieldLabel"]),
        Paragraph("No. of Packages", styles["FieldLabel"]),
        Paragraph("Description of Goods", styles["FieldLabel"]),
        Paragraph("Gross Weight (KG)", styles["FieldLabel"]),
        Paragraph("Measurement (CBM)", styles["FieldLabel"]),
    ]
    goods_rows = [goods_header]
    for c in data.containers:
        goods_rows.append([
            Paragraph(f"{c.container_number}<br/>Seal: {c.seal_number}<br/>{c.container_type}", styles["FieldValue"]),
            Paragraph(f"{c.packages} {c.package_type}", styles["FieldValue"]),
            Paragraph(c.commodity, styles["FieldValue"]),
            Paragraph(f"{c.gross_weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(f"{c.volume_cbm:,.2f}", styles["FieldValue"]),
        ])
    # Total
    goods_rows.append([
        Paragraph("<b>TOTALS</b>", styles["FieldValue"]),
        Paragraph(f"<b>{data.total_packages}</b>", styles["FieldValue"]),
        "",
        Paragraph(f"<b>{data.total_weight_kg:,.2f}</b>", styles["FieldValue"]),
        Paragraph(f"<b>{data.total_volume_cbm:,.2f}</b>", styles["FieldValue"]),
    ])

    gt = Table(goods_rows, colWidths=[1.6 * inch, 1.1 * inch, 1.8 * inch, 1.15 * inch, 1.15 * inch])
    gt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f0e6f6")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (0, -1), (-1, -1), 0.75, accent),
    ]))
    elements.append(gt)
    elements.append(Spacer(1, 6))

    # Declaration & signature
    decl_data = [
        [Paragraph("Declared Value for Carriage", styles["FieldLabel"]),
         Paragraph("Declared Value for Customs", styles["FieldLabel"]),
         Paragraph("Place and Date of Issue", styles["FieldLabel"]),
         Paragraph("No. of Originals", styles["FieldLabel"])],
        [Paragraph("As per Invoice", styles["FieldValue"]),
         Paragraph("As per Commercial Invoice", styles["FieldValue"]),
         Paragraph(f"{data.port_of_loading}<br/>{data.date_of_issue}", styles["FieldValue"]),
         Paragraph("THREE (3)", styles["FieldValue"])],
    ]
    dt = Table(decl_data, colWidths=[1.7 * inch] * 4)
    dt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(dt)
    elements.append(Spacer(1, 8))

    # Signature block
    sig = Table([
        [Paragraph("Signature of Carrier or their Agent", styles["FieldLabel"]),
         Paragraph("Signature of Consignor or their Agent", styles["FieldLabel"])],
        [Paragraph("<br/><br/>_________________________________", styles["FieldValue"]),
         Paragraph("<br/><br/>_________________________________", styles["FieldValue"])],
    ], colWidths=[3.4 * inch, 3.4 * inch])
    sig.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(sig)
    elements.append(Spacer(1, 6))

    # Legal
    legal = ("Taken in charge in apparently good order and condition, unless otherwise noted "
             "herein, at the place of receipt for transport and delivery as mentioned above. "
             "The Freight Forwarder, in issuing this Bill of Lading, undertakes to perform or "
             "procure the performance of the entire transport from the place of receipt to the "
             "place of delivery. This FBL is issued subject to UNCTAD/ICC Rules for Multimodal "
             "Transport Documents (ICC Publication 481).")
    elements.append(Paragraph(legal, styles["SmallText"]))

    doc.build(elements)


# ===========================================================================
# NON-BOL TEMPLATES (negative examples for classifier)
# ===========================================================================

# ---------------------------------------------------------------------------
# Template: Commercial Invoice
# ---------------------------------------------------------------------------

def render_commercial_invoice(data: InvoiceData, filepath: str):
    """Standard commercial invoice — NOT a Bill of Lading."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#1a5276")
    elements = []

    # Header
    hdr = Table([
        [Paragraph("COMMERCIAL INVOICE", styles["BolTitle"]),
         Paragraph(f"Invoice No: <b>{data.invoice_number}</b>", styles["FieldValue"])],
        [Paragraph(f"{data.seller_name}", styles["BolSubtitle"]),
         Paragraph(f"Date: {data.invoice_date}", styles["FieldValue"])],
    ], colWidths=[5.0 * inch, 2.5 * inch])
    hdr.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.5, accent),
        ("BACKGROUND", (0, 0), (0, 0), accent),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("LINEBELOW", (0, 0), (-1, 0), 1, accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(hdr)
    elements.append(Spacer(1, 8))

    # Seller / Buyer
    party = [
        [Paragraph("<b>Seller / Exporter</b>", styles["FieldLabel"]),
         Paragraph("<b>Buyer / Importer</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.seller_name}<br/>{data.seller_address}", styles["FieldValue"]),
         Paragraph(f"{data.buyer_name}<br/>{data.buyer_address}", styles["FieldValue"])],
    ]
    pt = Table(party, colWidths=[3.75 * inch, 3.75 * inch])
    pt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 6))

    # Terms row
    terms_data = [
        [Paragraph("Currency", styles["FieldLabel"]),
         Paragraph("Payment Terms", styles["FieldLabel"]),
         Paragraph("Incoterm", styles["FieldLabel"]),
         Paragraph("Country of Origin", styles["FieldLabel"])],
        [Paragraph(data.currency, styles["FieldValue"]),
         Paragraph(data.payment_terms, styles["FieldValue"]),
         Paragraph(data.incoterm, styles["FieldValue"]),
         Paragraph(data.country_of_origin, styles["FieldValue"])],
    ]
    tt = Table(terms_data, colWidths=[1.875 * inch] * 4)
    tt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(tt)
    elements.append(Spacer(1, 8))

    # Line items
    item_header = [
        Paragraph("Description", styles["FieldLabel"]),
        Paragraph("HS Code", styles["FieldLabel"]),
        Paragraph("Qty", styles["FieldLabel"]),
        Paragraph(f"Unit Price ({data.currency})", styles["FieldLabel"]),
        Paragraph(f"Total ({data.currency})", styles["FieldLabel"]),
    ]
    item_rows = [item_header]
    for item in data.line_items:
        item_rows.append([
            Paragraph(item.description, styles["FieldValue"]),
            Paragraph(item.hs_code, styles["FieldValue"]),
            Paragraph(str(item.quantity), styles["FieldValue"]),
            Paragraph(f"{item.unit_price:,.2f}", styles["FieldValue"]),
            Paragraph(f"{item.total_price:,.2f}", styles["FieldValue"]),
        ])
    # Totals
    item_rows.append(["", "", "", Paragraph("<b>Subtotal</b>", styles["FieldValue"]),
                       Paragraph(f"<b>{data.subtotal:,.2f}</b>", styles["FieldValue"])])
    item_rows.append(["", "", "", Paragraph("<b>Tax</b>", styles["FieldValue"]),
                       Paragraph(f"<b>{data.tax_amount:,.2f}</b>", styles["FieldValue"])])
    item_rows.append(["", "", "", Paragraph("<b>TOTAL</b>", styles["FieldValue"]),
                       Paragraph(f"<b>{data.total_amount:,.2f}</b>", styles["FieldValue"])])

    it = Table(item_rows, colWidths=[2.2 * inch, 1.0 * inch, 0.7 * inch, 1.5 * inch, 1.5 * inch])
    it.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d4e6f1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (3, -3), (-1, -3), 0.75, accent),
    ]))
    elements.append(it)
    elements.append(Spacer(1, 8))

    if data.notes:
        elements.append(Paragraph(f"Notes: {data.notes}", styles["FieldValue"]))
        elements.append(Spacer(1, 6))

    # Signature
    elements.append(Paragraph("Authorized Signature: _________________________", styles["FieldValue"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "We certify that the goods described herein are of the origin stated and that this "
        "invoice is true and correct in all particulars.",
        styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template: Packing List
# ---------------------------------------------------------------------------

def render_packing_list(data: PackingListData, filepath: str):
    """Standard packing list — NOT a Bill of Lading."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#6c3483")
    elements = []

    # Header
    elements.append(Paragraph("PACKING LIST", styles["BolTitle"]))
    elements.append(Spacer(1, 4))

    hdr_data = [
        [Paragraph("P/L Number", styles["FieldLabel"]),
         Paragraph("Date", styles["FieldLabel"]),
         Paragraph("Invoice Ref.", styles["FieldLabel"])],
        [Paragraph(data.packing_list_number, styles["FieldValue"]),
         Paragraph(data.date, styles["FieldValue"]),
         Paragraph(data.invoice_reference, styles["FieldValue"])],
    ]
    ht = Table(hdr_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    ht.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4ecf7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(ht)
    elements.append(Spacer(1, 6))

    # Parties
    party = [
        [Paragraph("<b>Seller</b>", styles["FieldLabel"]),
         Paragraph("<b>Buyer</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.seller_name}<br/>{data.seller_address}", styles["FieldValue"]),
         Paragraph(f"{data.buyer_name}<br/>{data.buyer_address}", styles["FieldValue"])],
    ]
    pt = Table(party, colWidths=[3.75 * inch, 3.75 * inch])
    pt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 8))

    # Items table
    item_header = [
        Paragraph("#", styles["FieldLabel"]),
        Paragraph("Description", styles["FieldLabel"]),
        Paragraph("Qty", styles["FieldLabel"]),
        Paragraph("Pkg Type", styles["FieldLabel"]),
        Paragraph("Net Wt (KG)", styles["FieldLabel"]),
        Paragraph("Gross Wt (KG)", styles["FieldLabel"]),
        Paragraph("Dimensions", styles["FieldLabel"]),
    ]
    item_rows = [item_header]
    for item in data.items:
        item_rows.append([
            Paragraph(str(item.item_number), styles["FieldValue"]),
            Paragraph(item.description, styles["FieldValue"]),
            Paragraph(str(item.quantity), styles["FieldValue"]),
            Paragraph(item.package_type, styles["FieldValue"]),
            Paragraph(f"{item.net_weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(f"{item.gross_weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(item.dimensions, styles["FieldValue"]),
        ])
    # Totals
    item_rows.append([
        Paragraph("<b>TOTAL</b>", styles["FieldValue"]),
        "",
        Paragraph(f"<b>{data.total_packages}</b>", styles["FieldValue"]),
        "",
        Paragraph(f"<b>{data.total_net_weight_kg:,.2f}</b>", styles["FieldValue"]),
        Paragraph(f"<b>{data.total_gross_weight_kg:,.2f}</b>", styles["FieldValue"]),
        "",
    ])

    it = Table(item_rows, colWidths=[0.4 * inch, 1.7 * inch, 0.6 * inch, 0.9 * inch,
                                      1.0 * inch, 1.0 * inch, 1.4 * inch])
    it.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f4ecf7")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (0, -1), (-1, -1), 0.75, accent),
    ]))
    elements.append(it)
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "This packing list is for reference purposes only and does not constitute a "
        "contract of carriage or a negotiable document.",
        styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template: Delivery Order
# ---------------------------------------------------------------------------

def render_delivery_order(data: DeliveryOrderData, filepath: str):
    """Port/carrier delivery order — NOT a Bill of Lading."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    styles = _styles()
    accent = colors.HexColor("#b7950b")
    elements = []

    # Header
    elements.append(Paragraph("DELIVERY ORDER", styles["BolTitle"]))
    elements.append(Paragraph(data.carrier_name, styles["BolSubtitle"]))
    elements.append(Spacer(1, 8))

    # DO info row
    info_data = [
        [Paragraph("D/O Number", styles["FieldLabel"]),
         Paragraph("Date", styles["FieldLabel"]),
         Paragraph("Vessel / Voyage", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"])],
        [Paragraph(data.do_number, styles["FieldValue"]),
         Paragraph(data.date, styles["FieldValue"]),
         Paragraph(f"{data.vessel_name} / V.{data.voyage_number}", styles["FieldValue"]),
         Paragraph(data.port_of_discharge, styles["FieldValue"])],
    ]
    info_t = Table(info_data, colWidths=[1.7 * inch, 1.7 * inch, 2.2 * inch, 1.9 * inch])
    info_t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fef9e7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(info_t)
    elements.append(Spacer(1, 6))

    # Consignee / Delivery address
    party = [
        [Paragraph("<b>Consignee</b>", styles["FieldLabel"]),
         Paragraph("<b>Delivery Address</b>", styles["FieldLabel"])],
        [Paragraph(f"{data.consignee_name}<br/>{data.consignee_address}", styles["FieldValue"]),
         Paragraph(data.delivery_address, styles["FieldValue"])],
    ]
    pt = Table(party, colWidths=[3.75 * inch, 3.75 * inch])
    pt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(pt)
    elements.append(Spacer(1, 6))

    # Containers list
    cont_header = [Paragraph("Container Number", styles["FieldLabel"])]
    cont_rows = [cont_header]
    for cn in data.container_numbers:
        cont_rows.append([Paragraph(cn, styles["FieldValue"])])

    ct = Table(cont_rows, colWidths=[7.5 * inch])
    ct.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fef9e7")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(Paragraph("CONTAINERS TO BE RELEASED", styles["FieldLabel"]))
    elements.append(Spacer(1, 2))
    elements.append(ct)
    elements.append(Spacer(1, 6))

    # Release / free time
    rel_data = [
        [Paragraph("Release Date", styles["FieldLabel"]),
         Paragraph("Free Time Expiry", styles["FieldLabel"])],
        [Paragraph(data.release_date, styles["FieldValue"]),
         Paragraph(data.free_time_expiry, styles["FieldValue"])],
    ]
    rt = Table(rel_data, colWidths=[3.75 * inch, 3.75 * inch])
    rt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    elements.append(rt)
    elements.append(Spacer(1, 8))

    if data.remarks:
        elements.append(Paragraph(f"Remarks: {data.remarks}", styles["FieldValue"]))
        elements.append(Spacer(1, 6))

    # Signature
    elements.append(Paragraph("Authorized by: _________________________", styles["FieldValue"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        "This Delivery Order authorizes the release of the above-mentioned containers. "
        "It does not constitute a Bill of Lading or any contract of carriage.",
        styles["SmallText"]))

    doc.build(elements)


# ===========================================================================
# BOL-PARTIAL TEMPLATES (documents containing BoL content/references)
# ===========================================================================

# ---------------------------------------------------------------------------
# Template: Cover Letter with BoL Summary
# ---------------------------------------------------------------------------

def render_bol_cover_letter(data: CoverLetterData, filepath: str):
    """Shipping document cover letter that references and summarizes a BoL."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.5 * inch, bottomMargin=0.5 * inch,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch)
    styles = _styles()
    accent = colors.HexColor("#2c3e50")
    elements = []

    # Letter header
    elements.append(Paragraph(f"<b>{data.sender_company}</b>", styles["BolSubtitle"]))
    elements.append(Paragraph(data.sender_address, styles["FieldValue"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(data.date, styles["FieldValue"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"{data.recipient_name}", styles["FieldValue"]))
    elements.append(Paragraph(f"<b>{data.recipient_company}</b>", styles["FieldValue"]))
    elements.append(Paragraph(data.recipient_address, styles["FieldValue"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"Re: {data.reference_number}", styles["FieldValue"]))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(f"Dear {data.recipient_name},", styles["FieldValue"]))
    elements.append(Spacer(1, 6))

    # Body text
    for para in data.body_text.split("\n\n"):
        elements.append(Paragraph(para, styles["FieldValue"]))
        elements.append(Spacer(1, 6))

    # Enclosed documents list
    elements.append(Paragraph("<b>Enclosed Documents:</b>", styles["FieldValue"]))
    for doc_name in data.enclosed_documents:
        elements.append(Paragraph(f"&bull; {doc_name}", styles["FieldValue"]))
    elements.append(Spacer(1, 8))

    # BoL summary table (the BoL-partial content)
    bol = data.bol_data
    elements.append(Paragraph("<b>Bill of Lading Summary</b>", styles["FieldLabel"]))
    elements.append(Spacer(1, 4))
    summary_data = [
        [Paragraph("B/L Number", styles["FieldLabel"]),
         Paragraph("Vessel / Voyage", styles["FieldLabel"]),
         Paragraph("Port of Loading", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"])],
        [Paragraph(bol.bol_number, styles["FieldValue"]),
         Paragraph(f"{bol.vessel_name} / {bol.voyage_number}", styles["FieldValue"]),
         Paragraph(bol.port_of_loading, styles["FieldValue"]),
         Paragraph(bol.port_of_discharge, styles["FieldValue"])],
        [Paragraph("Shipper", styles["FieldLabel"]),
         Paragraph("Consignee", styles["FieldLabel"]),
         Paragraph("Total Packages", styles["FieldLabel"]),
         Paragraph("Total Weight (KG)", styles["FieldLabel"])],
        [Paragraph(bol.shipper_name, styles["FieldValue"]),
         Paragraph(bol.consignee_name, styles["FieldValue"]),
         Paragraph(str(bol.total_packages), styles["FieldValue"]),
         Paragraph(f"{bol.total_weight_kg:,.2f}", styles["FieldValue"])],
    ]
    st = Table(summary_data, colWidths=[1.75 * inch] * 4)
    st.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaecee")),
        ("BACKGROUND", (0, 2), (-1, 2), colors.HexColor("#eaecee")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(st)
    elements.append(Spacer(1, 12))

    # Closing
    elements.append(Paragraph("Sincerely,", styles["FieldValue"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(data.sender_name, styles["FieldValue"]))
    elements.append(Paragraph(data.sender_company, styles["FieldValue"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template: Freight Manifest
# ---------------------------------------------------------------------------

def render_freight_manifest(data: FreightManifestData, filepath: str):
    """Cargo/freight manifest listing multiple BoLs — contains BoL data as part of it."""
    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            topMargin=0.4 * inch, bottomMargin=0.4 * inch,
                            leftMargin=0.4 * inch, rightMargin=0.4 * inch)
    styles = _styles()
    accent = colors.HexColor("#1b4f72")
    elements = []

    # Header
    hdr = Table([
        [Paragraph("CARGO MANIFEST", styles["BolTitle"]),
         Paragraph(f"Manifest No: <b>{data.manifest_number}</b>", styles["FieldValue"])],
        [Paragraph(data.shipping_line, styles["BolSubtitle"]),
         Paragraph(f"Date: {data.date}", styles["FieldValue"])],
    ], colWidths=[5.2 * inch, 2.5 * inch])
    hdr.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1.5, accent),
        ("BACKGROUND", (0, 0), (0, 0), accent),
        ("TEXTCOLOR", (0, 0), (0, 0), colors.white),
        ("LINEBELOW", (0, 0), (-1, 0), 1, accent),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(hdr)
    elements.append(Spacer(1, 6))

    # Vessel / voyage info
    vessel_data = [
        [Paragraph("Vessel Name", styles["FieldLabel"]),
         Paragraph("Voyage No.", styles["FieldLabel"]),
         Paragraph("Port of Loading", styles["FieldLabel"]),
         Paragraph("Port of Discharge", styles["FieldLabel"])],
        [Paragraph(data.vessel_name, styles["FieldValue"]),
         Paragraph(data.voyage_number, styles["FieldValue"]),
         Paragraph(data.port_of_loading, styles["FieldValue"]),
         Paragraph(data.port_of_discharge, styles["FieldValue"])],
    ]
    vt = Table(vessel_data, colWidths=[1.925 * inch] * 4)
    vt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d4e6f1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elements.append(vt)
    elements.append(Spacer(1, 8))

    # BoL entries table
    elements.append(Paragraph("BILL OF LADING SUMMARY", styles["FieldLabel"]))
    elements.append(Spacer(1, 2))

    bol_header = [
        Paragraph("B/L Number", styles["FieldLabel"]),
        Paragraph("Shipper", styles["FieldLabel"]),
        Paragraph("Consignee", styles["FieldLabel"]),
        Paragraph("Containers", styles["FieldLabel"]),
        Paragraph("Weight (KG)", styles["FieldLabel"]),
        Paragraph("Commodity", styles["FieldLabel"]),
    ]
    bol_rows = [bol_header]
    for entry in data.entries:
        bol_rows.append([
            Paragraph(entry.bol_number, styles["FieldValue"]),
            Paragraph(entry.shipper, styles["FieldValue"]),
            Paragraph(entry.consignee, styles["FieldValue"]),
            Paragraph(str(entry.containers), styles["FieldValue"]),
            Paragraph(f"{entry.weight_kg:,.2f}", styles["FieldValue"]),
            Paragraph(entry.commodity, styles["FieldValue"]),
        ])
    # Totals
    bol_rows.append([
        Paragraph(f"<b>TOTAL ({len(data.entries)} B/Ls)</b>", styles["FieldValue"]),
        "", "",
        Paragraph(f"<b>{data.total_containers}</b>", styles["FieldValue"]),
        Paragraph(f"<b>{data.total_weight_kg:,.2f}</b>", styles["FieldValue"]),
        "",
    ])

    bt = Table(bol_rows, colWidths=[1.3 * inch, 1.3 * inch, 1.3 * inch, 0.8 * inch,
                                     1.2 * inch, 1.5 * inch])
    bt.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.75, accent),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#d4e6f1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LINEABOVE", (0, -1), (-1, -1), 0.75, accent),
    ]))
    elements.append(bt)
    elements.append(Spacer(1, 10))

    # Footer
    elements.append(Paragraph(
        "This Cargo Manifest is prepared for customs and port authority use. "
        "It lists all Bills of Lading for the above vessel and voyage. "
        "This document itself is not a Bill of Lading and does not confer title to goods.",
        styles["SmallText"]))

    doc.build(elements)


# ---------------------------------------------------------------------------
# Template registry
# ---------------------------------------------------------------------------

TEMPLATES = {
    "ocean": render_ocean_bol,
    "truck": render_truck_bol,
    "short": render_short_bol,
    "multimodal": render_multimodal_bol,
}

NON_BOL_TEMPLATES = {
    "commercial_invoice": render_commercial_invoice,
    "packing_list": render_packing_list,
    "delivery_order": render_delivery_order,
}

BOL_PARTIAL_TEMPLATES = {
    "bol_cover_letter": render_bol_cover_letter,
    "freight_manifest": render_freight_manifest,
}

ALL_TEMPLATES = {**TEMPLATES, **NON_BOL_TEMPLATES, **BOL_PARTIAL_TEMPLATES}

# Maps each template name to its document category
TEMPLATE_CATEGORIES = {}
for t in TEMPLATES:
    TEMPLATE_CATEGORIES[t] = "bol"
for t in NON_BOL_TEMPLATES:
    TEMPLATE_CATEGORIES[t] = "non_bol"
for t in BOL_PARTIAL_TEMPLATES:
    TEMPLATE_CATEGORIES[t] = "bol_partial"
