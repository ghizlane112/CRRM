# test_google_ads.py
try:
    from google.ads.google_ads.client import GoogleAdsClient
    print("Module google.ads.google_ads est disponible")
except ImportError as e:
    print(f"Erreur d'importation : {e}")
