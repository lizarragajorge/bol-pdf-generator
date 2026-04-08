"""Random data generator for Bill of Lading documents."""

import random
import string
from dataclasses import dataclass, field
from faker import Faker

fake = Faker()


VESSEL_NAMES = [
    "MSC OSCAR", "EVER GIVEN", "HMM ALGECIRAS", "CMA CGM JACQUES SAADE",
    "MADRID MAERSK", "OOCL HONG KONG", "COSCO SHIPPING UNIVERSE",
    "MOL TRIUMPH", "EVER ACE", "MSC GULSUN", "HYUNDAI MERCHANT",
    "YANG MING WELLNESS", "PIL PIRAEUS", "ZIM SHANGHAI", "HAPAG LLOYD EXPRESS",
    "ATLANTIC STAR", "PACIFIC VOYAGER", "NORTHERN SPIRIT", "SOUTHERN CROSS",
    "ORIENTAL JADE", "GOLDEN HORIZON", "BLUE MARLIN", "RED FALCON",
]

PORTS = [
    "Shanghai, China", "Singapore", "Ningbo-Zhoushan, China", "Shenzhen, China",
    "Guangzhou, China", "Busan, South Korea", "Qingdao, China", "Hong Kong",
    "Tianjin, China", "Rotterdam, Netherlands", "Port Klang, Malaysia",
    "Antwerp, Belgium", "Xiamen, China", "Kaohsiung, Taiwan",
    "Hamburg, Germany", "Los Angeles, USA", "Long Beach, USA",
    "Tanjung Pelepas, Malaysia", "Laem Chabang, Thailand", "New York, USA",
    "Savannah, USA", "Felixstowe, UK", "Valencia, Spain", "Colombo, Sri Lanka",
    "Jawaharlal Nehru, India", "Jeddah, Saudi Arabia", "Piraeus, Greece",
    "Yokohama, Japan", "Tokyo, Japan", "Santos, Brazil",
]

COMMODITIES = [
    "Electronic Components", "Textile Fabrics", "Auto Parts", "Machinery Equipment",
    "Chemical Products", "Steel Coils", "Plastic Granules", "Paper Products",
    "Furniture", "Canned Food Products", "Frozen Seafood", "Rubber Products",
    "Glass Products", "Ceramic Tiles", "Toys and Games", "Medical Supplies",
    "Household Appliances", "Footwear", "Garments", "Wooden Pallets",
    "Copper Wire", "Aluminum Sheets", "Cotton Yarn", "Rice (Bagged)",
    "Coffee Beans", "Cocoa Powder", "Fertilizer", "Paint and Coatings",
    "Bicycle Parts", "Solar Panels",
]

PACKAGE_TYPES = [
    "Cartons", "Pallets", "Drums", "Bags", "Crates", "Bundles",
    "Rolls", "Bales", "Cases", "Containers",
]

CONTAINER_TYPES = ["20' DRY", "40' DRY", "40' HC", "20' REEFER", "40' REEFER", "20' OT", "40' OT"]

SHIPPING_LINES = [
    "Maersk Line", "MSC - Mediterranean Shipping Co.", "CMA CGM Group",
    "COSCO Shipping Lines", "Hapag-Lloyd", "ONE (Ocean Network Express)",
    "Evergreen Marine Corp.", "Yang Ming Marine Transport",
    "HMM (Hyundai Merchant Marine)", "ZIM Integrated Shipping",
    "PIL (Pacific International Lines)", "Wan Hai Lines",
    "IRISL Group", "KMTC", "SM Line Corporation",
]

INCOTERMS = ["FOB", "CIF", "CFR", "EXW", "FCA", "DAP", "DDP", "CPT", "CIP"]

CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CNY", "CHF", "CAD", "AUD"]

PAYMENT_TERMS = [
    "Net 30", "Net 60", "Net 90", "Due on Receipt",
    "Letter of Credit", "Cash in Advance", "Open Account",
]

HS_CODES = [
    "8471.30", "6006.32", "8708.99", "8479.89", "2917.39",
    "7210.49", "3901.20", "4802.55", "9401.61", "1602.49",
    "0303.89", "4016.99", "7005.29", "6907.23", "9503.00",
    "3006.60", "8516.60", "6403.99", "6204.62", "4415.20",
]

COUNTRIES_OF_ORIGIN = [
    "China", "United States", "Germany", "Japan", "South Korea",
    "India", "Vietnam", "Taiwan", "Thailand", "Malaysia",
    "Indonesia", "Brazil", "Mexico", "Italy", "France",
]

TRUCK_CARRIERS = [
    "J.B. Hunt Transport Services", "Schneider National", "Werner Enterprises",
    "XPO Logistics", "Swift Transportation", "Knight-Swift", "Landstar System",
    "Old Dominion Freight Line", "FedEx Freight", "UPS Freight",
    "YRC Worldwide", "Estes Express Lines", "Saia Inc.", "ABF Freight",
    "Southeastern Freight Lines", "R+L Carriers", "Holland Motor Express",
]


@dataclass
class ContainerInfo:
    container_number: str
    seal_number: str
    container_type: str
    packages: int
    package_type: str
    gross_weight_kg: float
    volume_cbm: float
    commodity: str


@dataclass
class BolData:
    bol_number: str
    booking_number: str
    shipper_name: str
    shipper_address: str
    consignee_name: str
    consignee_address: str
    notify_party_name: str
    notify_party_address: str
    vessel_name: str
    voyage_number: str
    port_of_loading: str
    port_of_discharge: str
    place_of_receipt: str
    place_of_delivery: str
    shipping_line: str
    date_of_issue: str
    date_of_shipment: str
    containers: list = field(default_factory=list)
    freight_terms: str = "PREPAID"
    incoterm: str = "FOB"
    special_instructions: str = ""
    # Truck-specific fields
    carrier_name: str = ""
    trailer_number: str = ""
    driver_name: str = ""
    pro_number: str = ""
    origin_city: str = ""
    destination_city: str = ""
    # Totals
    total_packages: int = 0
    total_weight_kg: float = 0.0
    total_volume_cbm: float = 0.0


def _gen_container_number() -> str:
    prefix = "".join(random.choices(string.ascii_uppercase, k=4))
    digits = "".join(random.choices(string.digits, k=7))
    return f"{prefix}{digits}"


def _gen_seal_number() -> str:
    return f"SL{random.randint(100000, 999999)}"


def _gen_bol_number() -> str:
    prefix = random.choice(["MSKU", "HLCU", "CMAU", "OOLU", "EISU", "TCLU"])
    return f"{prefix}{random.randint(100000000, 999999999)}"


def _gen_booking_number() -> str:
    return f"BK{random.randint(10000000, 99999999)}"


def _gen_voyage_number() -> str:
    direction = random.choice(["E", "W", "N", "S"])
    return f"{random.randint(100, 999)}{direction}"


def _gen_pro_number() -> str:
    return f"PRO-{random.randint(10000000, 99999999)}"


def _gen_trailer_number() -> str:
    return f"TRL-{random.randint(10000, 99999)}"


def generate_container() -> ContainerInfo:
    packages = random.randint(10, 500)
    weight = round(random.uniform(1000, 25000), 2)
    volume = round(random.uniform(10, 67), 2)
    return ContainerInfo(
        container_number=_gen_container_number(),
        seal_number=_gen_seal_number(),
        container_type=random.choice(CONTAINER_TYPES),
        packages=packages,
        package_type=random.choice(PACKAGE_TYPES),
        gross_weight_kg=weight,
        volume_cbm=volume,
        commodity=random.choice(COMMODITIES),
    )


def generate_bol_data(template_type: str = "ocean") -> BolData:
    """Generate random BoL data. template_type: ocean, truck, short, multimodal, ocean_multi, truck_multi."""
    is_multi = template_type.endswith("_multi")
    base_type = template_type.removesuffix("_multi")

    if base_type == "truck":
        num_containers = 0
    elif is_multi:
        num_containers = random.randint(6, 12)
    else:
        num_containers = random.randint(1, 4)
    containers = [generate_container() for _ in range(num_containers)]

    port_loading = random.choice(PORTS)
    port_discharge = random.choice([p for p in PORTS if p != port_loading])

    issue_date = fake.date_between(start_date="-2y", end_date="today")
    ship_date = fake.date_between(start_date=issue_date, end_date="+30d")

    total_pkgs = sum(c.packages for c in containers)
    total_wt = round(sum(c.gross_weight_kg for c in containers), 2)
    total_vol = round(sum(c.volume_cbm for c in containers), 2)

    if base_type == "truck":
        total_pkgs = random.randint(10, 500)
        total_wt = round(random.uniform(500, 20000), 2)
        total_vol = round(random.uniform(5, 80), 2)

    data = BolData(
        bol_number=_gen_bol_number(),
        booking_number=_gen_booking_number(),
        shipper_name=fake.company(),
        shipper_address=fake.address().replace("\n", ", "),
        consignee_name=fake.company(),
        consignee_address=fake.address().replace("\n", ", "),
        notify_party_name=fake.company(),
        notify_party_address=fake.address().replace("\n", ", "),
        vessel_name=random.choice(VESSEL_NAMES),
        voyage_number=_gen_voyage_number(),
        port_of_loading=port_loading,
        port_of_discharge=port_discharge,
        place_of_receipt=port_loading.split(",")[0],
        place_of_delivery=port_discharge.split(",")[0],
        shipping_line=random.choice(SHIPPING_LINES),
        date_of_issue=issue_date.strftime("%B %d, %Y"),
        date_of_shipment=ship_date.strftime("%B %d, %Y"),
        containers=containers,
        freight_terms=random.choice(["PREPAID", "COLLECT", "THIRD PARTY"]),
        incoterm=random.choice(INCOTERMS),
        special_instructions=random.choice([
            "", "", "",
            "HANDLE WITH CARE", "KEEP DRY", "TEMPERATURE CONTROLLED",
            "FRAGILE - DO NOT STACK", "HAZARDOUS MATERIAL - CLASS 3",
            "NOTIFY CONSIGNEE UPON ARRIVAL",
        ]),
        carrier_name=random.choice(TRUCK_CARRIERS) if base_type == "truck" else "",
        trailer_number=_gen_trailer_number() if base_type == "truck" else "",
        driver_name=fake.name() if base_type == "truck" else "",
        pro_number=_gen_pro_number() if base_type == "truck" else "",
        origin_city=fake.city() + ", " + fake.state_abbr() if base_type == "truck" else "",
        destination_city=fake.city() + ", " + fake.state_abbr() if base_type == "truck" else "",
        total_packages=total_pkgs,
        total_weight_kg=total_wt,
        total_volume_cbm=total_vol,
    )
    return data


# ---------------------------------------------------------------------------
# Non-BoL document data
# ---------------------------------------------------------------------------

@dataclass
class InvoiceLineItem:
    description: str
    hs_code: str
    quantity: int
    unit_price: float
    total_price: float


@dataclass
class InvoiceData:
    invoice_number: str
    invoice_date: str
    seller_name: str
    seller_address: str
    buyer_name: str
    buyer_address: str
    currency: str
    payment_terms: str
    country_of_origin: str
    incoterm: str
    line_items: list = field(default_factory=list)
    subtotal: float = 0.0
    tax_amount: float = 0.0
    total_amount: float = 0.0
    notes: str = ""


@dataclass
class PackingListItem:
    item_number: int
    description: str
    quantity: int
    package_type: str
    net_weight_kg: float
    gross_weight_kg: float
    dimensions: str


@dataclass
class PackingListData:
    packing_list_number: str
    date: str
    seller_name: str
    seller_address: str
    buyer_name: str
    buyer_address: str
    invoice_reference: str
    items: list = field(default_factory=list)
    total_packages: int = 0
    total_net_weight_kg: float = 0.0
    total_gross_weight_kg: float = 0.0


@dataclass
class DeliveryOrderData:
    do_number: str
    date: str
    carrier_name: str
    consignee_name: str
    consignee_address: str
    delivery_address: str
    vessel_name: str
    voyage_number: str
    port_of_discharge: str
    container_numbers: list = field(default_factory=list)
    release_date: str = ""
    free_time_expiry: str = ""
    remarks: str = ""


# ---------------------------------------------------------------------------
# BoL-partial document data
# ---------------------------------------------------------------------------

@dataclass
class CoverLetterData:
    date: str
    sender_name: str
    sender_company: str
    sender_address: str
    recipient_name: str
    recipient_company: str
    recipient_address: str
    reference_number: str
    bol_data: BolData = None
    enclosed_documents: list = field(default_factory=list)
    body_text: str = ""


@dataclass
class FreightManifestEntry:
    bol_number: str
    shipper: str
    consignee: str
    port_of_loading: str
    port_of_discharge: str
    containers: int
    weight_kg: float
    commodity: str


@dataclass
class FreightManifestData:
    manifest_number: str
    vessel_name: str
    voyage_number: str
    date: str
    port_of_loading: str
    port_of_discharge: str
    shipping_line: str
    entries: list = field(default_factory=list)
    total_containers: int = 0
    total_weight_kg: float = 0.0


# ---------------------------------------------------------------------------
# Non-BoL data generators
# ---------------------------------------------------------------------------

def _gen_invoice_number() -> str:
    prefix = random.choice(["INV", "CI", "CINV"])
    return f"{prefix}-{random.randint(100000, 999999)}"


def _gen_packing_list_number() -> str:
    return f"PL-{random.randint(100000, 999999)}"


def _gen_do_number() -> str:
    return f"DO-{random.randint(100000, 999999)}"


def _gen_manifest_number() -> str:
    return f"MFT-{random.randint(10000, 99999)}"


def generate_invoice_data(multi: bool = False) -> InvoiceData:
    """Generate random commercial invoice data."""
    num_items = random.randint(15, 30) if multi else random.randint(2, 8)
    items = []
    for _ in range(num_items):
        qty = random.randint(10, 500)
        unit_price = round(random.uniform(5.0, 500.0), 2)
        items.append(InvoiceLineItem(
            description=random.choice(COMMODITIES),
            hs_code=random.choice(HS_CODES),
            quantity=qty,
            unit_price=unit_price,
            total_price=round(qty * unit_price, 2),
        ))
    subtotal = round(sum(i.total_price for i in items), 2)
    tax = round(subtotal * random.uniform(0.0, 0.15), 2)

    issue_date = fake.date_between(start_date="-2y", end_date="today")
    return InvoiceData(
        invoice_number=_gen_invoice_number(),
        invoice_date=issue_date.strftime("%B %d, %Y"),
        seller_name=fake.company(),
        seller_address=fake.address().replace("\n", ", "),
        buyer_name=fake.company(),
        buyer_address=fake.address().replace("\n", ", "),
        currency=random.choice(CURRENCIES),
        payment_terms=random.choice(PAYMENT_TERMS),
        country_of_origin=random.choice(COUNTRIES_OF_ORIGIN),
        incoterm=random.choice(INCOTERMS),
        line_items=items,
        subtotal=subtotal,
        tax_amount=tax,
        total_amount=round(subtotal + tax, 2),
        notes=random.choice([
            "", "",
            "All goods are of domestic origin.",
            "Payment due per agreed terms.",
            "Prices quoted in the agreed currency.",
        ]),
    )


def generate_packing_list_data(multi: bool = False) -> PackingListData:
    """Generate random packing list data."""
    num_items = random.randint(20, 40) if multi else random.randint(3, 10)
    items = []
    for idx in range(1, num_items + 1):
        net = round(random.uniform(5, 500), 2)
        gross = round(net * random.uniform(1.05, 1.30), 2)
        dims = f"{random.randint(20,120)}x{random.randint(20,80)}x{random.randint(10,60)} cm"
        items.append(PackingListItem(
            item_number=idx,
            description=random.choice(COMMODITIES),
            quantity=random.randint(1, 200),
            package_type=random.choice(PACKAGE_TYPES),
            net_weight_kg=net,
            gross_weight_kg=gross,
            dimensions=dims,
        ))
    issue_date = fake.date_between(start_date="-2y", end_date="today")
    return PackingListData(
        packing_list_number=_gen_packing_list_number(),
        date=issue_date.strftime("%B %d, %Y"),
        seller_name=fake.company(),
        seller_address=fake.address().replace("\n", ", "),
        buyer_name=fake.company(),
        buyer_address=fake.address().replace("\n", ", "),
        invoice_reference=_gen_invoice_number(),
        items=items,
        total_packages=sum(i.quantity for i in items),
        total_net_weight_kg=round(sum(i.net_weight_kg for i in items), 2),
        total_gross_weight_kg=round(sum(i.gross_weight_kg for i in items), 2),
    )


def generate_delivery_order_data() -> DeliveryOrderData:
    """Generate random delivery order data."""
    port = random.choice(PORTS)
    issue_date = fake.date_between(start_date="-2y", end_date="today")
    release_date = fake.date_between(start_date=issue_date, end_date="+10d")
    free_time = fake.date_between(start_date=release_date, end_date="+14d")
    num_containers = random.randint(1, 4)
    return DeliveryOrderData(
        do_number=_gen_do_number(),
        date=issue_date.strftime("%B %d, %Y"),
        carrier_name=random.choice(SHIPPING_LINES),
        consignee_name=fake.company(),
        consignee_address=fake.address().replace("\n", ", "),
        delivery_address=fake.address().replace("\n", ", "),
        vessel_name=random.choice(VESSEL_NAMES),
        voyage_number=_gen_voyage_number(),
        port_of_discharge=port,
        container_numbers=[_gen_container_number() for _ in range(num_containers)],
        release_date=release_date.strftime("%B %d, %Y"),
        free_time_expiry=free_time.strftime("%B %d, %Y"),
        remarks=random.choice([
            "", "",
            "Subject to payment of all charges.",
            "Release upon presentation of original documents.",
            "Containers to be returned within free time.",
        ]),
    )


# ---------------------------------------------------------------------------
# BoL-partial data generators
# ---------------------------------------------------------------------------

def generate_cover_letter_data(multi: bool = False) -> CoverLetterData:
    """Generate cover letter data that references and summarizes a BoL."""
    bol = generate_bol_data(template_type="ocean_multi" if multi else "ocean")
    issue_date = fake.date_between(start_date="-2y", end_date="today")
    enclosed = random.sample([
        "Original Bill of Lading (3/3)",
        "Commercial Invoice",
        "Packing List",
        "Certificate of Origin",
        "Insurance Certificate",
        "Inspection Certificate",
        "Fumigation Certificate",
    ], k=random.randint(3, 5))
    body = (
        f"Please find enclosed the shipping documents for B/L No. {bol.bol_number}, "
        f"covering a shipment of goods from {bol.port_of_loading} to "
        f"{bol.port_of_discharge} aboard the vessel {bol.vessel_name} "
        f"(Voyage {bol.voyage_number}).\n\n"
        f"The shipment consists of {bol.total_packages} packages with a total "
        f"gross weight of {bol.total_weight_kg:,.2f} KG.\n\n"
        "Please arrange for the collection and clearance of the cargo upon arrival. "
        "Should you have any questions, please do not hesitate to contact us."
    )
    return CoverLetterData(
        date=issue_date.strftime("%B %d, %Y"),
        sender_name=fake.name(),
        sender_company=bol.shipping_line,
        sender_address=fake.address().replace("\n", ", "),
        recipient_name=fake.name(),
        recipient_company=bol.consignee_name,
        recipient_address=bol.consignee_address,
        reference_number=f"REF-{random.randint(100000, 999999)}",
        bol_data=bol,
        enclosed_documents=enclosed,
        body_text=body,
    )


def generate_freight_manifest_data(multi: bool = False) -> FreightManifestData:
    """Generate a freight manifest listing multiple BoLs."""
    vessel = random.choice(VESSEL_NAMES)
    voyage = _gen_voyage_number()
    port_load = random.choice(PORTS)
    port_disc = random.choice([p for p in PORTS if p != port_load])
    line = random.choice(SHIPPING_LINES)
    issue_date = fake.date_between(start_date="-2y", end_date="today")

    num_entries = random.randint(30, 50) if multi else random.randint(5, 15)
    entries = []
    for _ in range(num_entries):
        num_cont = random.randint(1, 4)
        wt = round(random.uniform(5000, 80000), 2)
        entries.append(FreightManifestEntry(
            bol_number=_gen_bol_number(),
            shipper=fake.company(),
            consignee=fake.company(),
            port_of_loading=port_load,
            port_of_discharge=port_disc,
            containers=num_cont,
            weight_kg=wt,
            commodity=random.choice(COMMODITIES),
        ))

    return FreightManifestData(
        manifest_number=_gen_manifest_number(),
        vessel_name=vessel,
        voyage_number=voyage,
        date=issue_date.strftime("%B %d, %Y"),
        port_of_loading=port_load,
        port_of_discharge=port_disc,
        shipping_line=line,
        entries=entries,
        total_containers=sum(e.containers for e in entries),
        total_weight_kg=round(sum(e.weight_kg for e in entries), 2),
    )
