from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SECRET_ACCESS_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
