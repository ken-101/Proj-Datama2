import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://ucetgthdnnsuezfiwiyc.supabase.co')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVjZXRndGhkbm5zdWV6Zml3aXljIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA1NTExMDQsImV4cCI6MjA1NjEyNzEwNH0.5LvV_D24ZvYg207gAIzuZU2-B_037hhrWx9lc1o7B_E')