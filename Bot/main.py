import requests
import time
import os

# ─── CONFIGURATION ───
BASE_URL = "https://database-4ce7c-default-rtdb.firebaseio.com"
SUBMISSIONS_URL = f"{BASE_URL}/html_vault_submissions.json"
PROCESSED_URL = f"{BASE_URL}/processed_ids.json"

# Green-API settings
ID_INSTANCE = "7107627485" 
API_TOKEN = "f713ce355f10440daad6476608772436828b8f6b02c74a09a8"
API_URL = "https://7107.api.greenapi.com"

MESSAGE_TEMPLATE = "Your form has been submitted successfully. We'll be in touch with you very shortly.\n— ELECSY Team"

def get_processed_ids_from_db():
    """Database theke processed IDs gulo niye ashe"""
    try:
        response = requests.get(PROCESSED_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                return set(data.keys())
    except Exception as e:
        print(f"⚠️ Error fetching processed IDs: {e}")
    return set()

def save_processed_id_to_db(submission_id):
    """Database-e submission ID mark kore rakhe"""
    try:
        url = f"{BASE_URL}/processed_ids/{submission_id}.json"
        requests.put(url, json=True)
    except Exception as e:
        print(f"⚠️ Error saving processed ID to DB: {e}")

def send_whatsapp_api(phone):
    """Eita background e message pathabe, browser lagbe na"""
    try:
        # Phone number clean kora
        phone = str(phone).strip().replace("+", "").replace(" ", "").replace("-", "")
        # Remove leading 0 if present and not already starting with 88
        if phone.startswith("0") and not phone.startswith("00"):
            phone = "88" + phone
        elif not phone.startswith("88"):
            phone = "88" + phone
        
        url = f"{API_URL}/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
        
        payload = {
            "chatId": f"{phone}@c.us",
            "message": MESSAGE_TEMPLATE
        }
        
        headers = {'Content-Type': 'application/json'}
        
        print(f"Sending auto-msg to: {phone}...")
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Successfully sent to {phone}")
            return True
        else:
            print(f"❌ Failed! Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"⚠️ API Error: {e}")
        return False

def main():
    print("🚀 WhatsApp Full-Auto Bot Started (Database Only Mode)")
    print(f"Monitoring Firebase: {SUBMISSIONS_URL}")
    
    while True:
        try:
            # Prothome database theke processed IDs gulo load kori
            processed_ids = get_processed_ids_from_db()
            
            response = requests.get(SUBMISSIONS_URL)
            if response.status_code == 200:
                data = response.json()
                if data:
                    for sub_id, info in data.items():
                        if sub_id not in processed_ids:
                            phone = info.get("phone")
                            if phone:
                                success = send_whatsapp_api(phone)
                                if success:
                                    save_processed_id_to_db(sub_id)
                                    time.sleep(2) # Flood protection
            else:
                print(f"Database error: {response.status_code}")
                
        except Exception as e:
            print(f"Loop Error: {e}")
            
        time.sleep(20) # 20 second por por check korbe

if __name__ == "__main__":
    main()
