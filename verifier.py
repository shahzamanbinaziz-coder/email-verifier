import re
import smtplib
import dns.resolver

SAFE_MODE = True  # Keeps verification non-intrusive

def is_valid_format(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def get_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return str(answers[0].exchange)
    except Exception:
        return None

def verify_email(email):
    if not is_valid_format(email):
        return False, "❌ Invalid format"

    domain = email.split('@')[-1]
    mx_record = get_mx_record(domain)
    if not mx_record:
        return False, "❌ No MX record"

    try:
        server = smtplib.SMTP(mx_record, timeout=10)
        server.ehlo()
        if SAFE_MODE:
            server.mail("check@yourdomain.com")
            code, _ = server.rcpt(email)
            server.quit()
            if code in [250, 251]:
                return True, "✅ Deliverable"
            else:
                return False, f"⚠️ Not deliverable ({code})"
        else:
            server.quit()
            return True, "✅ Domain reachable"
    except smtplib.SMTPServerDisconnected:
        return False, "⚠️ Disconnected"
    except smtplib.SMTPConnectError:
        return False, "⚠️ Cannot connect"
    except Exception:
        return False, "⚠️ Unknown error"
