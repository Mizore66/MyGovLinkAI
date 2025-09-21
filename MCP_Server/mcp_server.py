import random
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from datetime import datetime

# Initialize FastMCP server
mcp = FastMCP("GovLink")

# Constants
USER_AGENT = "gov-link/1.0"
FAKER_SAMAN = "https://fakerapi.it/api/v2/custom?_seed=500&_quantity=1&email=email&phoneNumber=phone&address=address&licenseNumber=number&expiryDate=dateTime&isDigital=boolean"

async def make_faker_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Faker API with proper error handling."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def format_alert(feature: dict) -> str:
    """Format an alert feature into a readable string."""
    props = feature["properties"]
    return f"""
Event: {props.get('event', 'Unknown')}
Area: {props.get('areaDesc', 'Unknown')}
Severity: {props.get('severity', 'Unknown')}
Description: {props.get('description', 'No description available')}
Instructions: {props.get('instruction', 'No specific instructions provided')}
"""

@mcp.tool(description="Retrieve driving license information for a Malaysian citizen using their MyKad number")
async def get_license_data(mykad: str) -> str:
    """Get driving license data for a Malaysian citizen.
    
    Args:
        mykad: Malaysian Identity Card (MyKad) number
        
    Returns:
        Formatted string containing license details including validity status
    """
    url = f"https://fakerapi.it/api/v2/custom?_seed={mykad}&_quantity=1&email=email&phoneNumber=phone&address=streetAddress&licenseNumber=number&expiryDate=dateTime&isDigital=boolean"
    data = await make_faker_request(url)
    if data and "data" in data and len(data["data"]) > 0:
        license = data["data"][0]
        licenseType = ["LDL", "PDL", "CDL"]
        try:
            mykad_int = int(mykad)
            randomLicense = licenseType[mykad_int % len(licenseType)]
        except ValueError:
            randomLicense = "LDL"  # Default license type
        # Format the saman data as a readable string
        expiry_str = license.get('expiryDate', '')
        try:
            expiry_date = datetime.fromisoformat(expiry_str.replace('Z', '+00:00'))
            is_valid = expiry_date > datetime.now(expiry_date.tzinfo)
        except Exception:
            is_valid = False

        return f"""
    myKadNumber: {mykad} 
    Email: {license.get('email', 'Unknown')}
    Phone: {license.get('phoneNumber', 'Unknown')}
    Address: {license.get('address', 'Unknown')}
    License Number: {license.get('licenseNumber', 'Unknown')}
    License Type: {randomLicense}\nExpiry: {license.get('expiryDate', 'Unknown')}
    Status: {'TRUE' if is_valid else 'FALSE'}
    Digital: {license.get('isDigital', 'Unknown')}
    """
    return "Couldnt find a license, DO NOT create a random one just say you cant find one"

@mcp.tool(description="Retrieve traffic summons (saman) records for a Malaysian citizen using their MyKad number")
async def get_saman_data(mykad: str) -> str:
    """Get traffic summons data for a Malaysian citizen.
    
    Args:
        mykad: Malaysian Identity Card (MyKad) number
        
    Returns:
        Formatted string containing summons details including amount and offense
    """
    random.seed(mykad)
    url = f"https://fakerapi.it/api/v2/custom?_seed={mykad}&_quantity=1&summonId=number&amount=number&issueDate=dateTime&location=streetAddress"
    data = await make_faker_request(url)
    if data and "data" in data and len(data["data"]) > 0:
        saman = data["data"][0]
        offenses = [
            "Speeding in a residential area",
            "Parking in a non-designated zone",
            "Failure to display valid road tax sticker",
            "Running a red light",
            "Using a mobile phone while driving",
            "Not wearing a seatbelt",
            "Driving without a valid license",
        ]
        offense = random.choice(offenses)
        # Format the saman data as a readable string
        return f"""summonId: {saman.get('summonId', 'Unknown')}
myKadNumber: {mykad}
offenseDetails: {offense}
amount: {saman.get('amount', 'Unknown')}
issueDate: {saman.get('issueDate', 'Unknown')}
location: {saman.get('location', 'Unknown')}
status: Pending
paidDate: None
"""
    return "Couldn't find a saman"

@mcp.tool(description="Get information about how to pay traffic summons online")
async def pay_saman() -> str:
    """Provide instructions for paying traffic summons.
    
    Returns:
        Instructions on where to pay traffic summons
    """
    return "To pay your traffic summons, you can visit the official government website at https://www.myeg.com.my/services/jpj or use the MyEG app for a convenient online payment option or visit the nearest JPJ office."

@mcp.tool(description="Get information about renewing a Malaysian driving license")
async def renew_license() -> str:
    """Provide instructions for renewing a driving license.
    
    Returns:
        Instructions on how to renew a driving license
    """
    return "Visit the nearest JPJ office or use the MyJPJ app to renew your driving license. Alternatively, you can visit this website https://www.myeg.com.my/services/jpj"
    

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')