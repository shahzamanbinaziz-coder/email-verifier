import re
import dns.resolver

# Simple regex for email format
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def verify_email(email):
    # 1. Check format
    if not EMAIL_REGEX.match(email):
        return {"email": email, "valid": False, "status": "❌ Invalid format"}

    domain = email.split('@')[-1]

    # 2. Check domain DNS
    try:
        # Check MX record
        answers = dns.resolver.resolve(domain, 'MX')
        if answers:
            return {"email": email, "valid": True, "status": "✅ MX record found"}
    except dns.resolver.NXDOMAIN:
        return {"email": email, "valid": False, "status": "❌ Domain does not exist"}
    except dns.resolver.NoAnswer:
        # Try A record as fallback
        try:
            dns.resolver.resolve(domain, 'A')
            return {"email": email, "valid": True, "status": "⚠️ No MX record, but A record found"}
        except:
            return {"email": email, "valid": False, "status": "❌ No DNS record found"}
    except Exception as e:
        return {"email": email, "valid": False, "status": f"⚠️ Error: {e}"}

    return {"email": email, "valid": False, "status": "❌ Unknown issue"}

