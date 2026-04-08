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
    """Generate random BoL data. template_type: ocean, truck, short, multimodal."""
    num_containers = random.randint(1, 4) if template_type != "truck" else 0
    containers = [generate_container() for _ in range(num_containers)]

    port_loading = random.choice(PORTS)
    port_discharge = random.choice([p for p in PORTS if p != port_loading])

    issue_date = fake.date_between(start_date="-2y", end_date="today")
    ship_date = fake.date_between(start_date=issue_date, end_date="+30d")

    total_pkgs = sum(c.packages for c in containers)
    total_wt = round(sum(c.gross_weight_kg for c in containers), 2)
    total_vol = round(sum(c.volume_cbm for c in containers), 2)

    if template_type == "truck":
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
        carrier_name=random.choice(TRUCK_CARRIERS) if template_type == "truck" else "",
        trailer_number=_gen_trailer_number() if template_type == "truck" else "",
        driver_name=fake.name() if template_type == "truck" else "",
        pro_number=_gen_pro_number() if template_type == "truck" else "",
        origin_city=fake.city() + ", " + fake.state_abbr() if template_type == "truck" else "",
        destination_city=fake.city() + ", " + fake.state_abbr() if template_type == "truck" else "",
        total_packages=total_pkgs,
        total_weight_kg=total_wt,
        total_volume_cbm=total_vol,
    )
    return data
