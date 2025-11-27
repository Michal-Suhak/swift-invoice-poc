-- Create the invoices table in Supabase
-- Run this SQL in your Supabase SQL Editor (https://supabase.com/dashboard/project/YOUR_PROJECT/editor)

CREATE TABLE IF NOT EXISTS invoices (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    customer TEXT NOT NULL,
    amount NUMERIC(10, 2) NOT NULL CHECK (amount > 0),
    status TEXT NOT NULL CHECK (status IN ('pending', 'paid', 'cancelled')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create an index on created_at for faster sorting
CREATE INDEX IF NOT EXISTS idx_invoices_created_at ON invoices(created_at DESC);

-- Optional: Add Row Level Security (RLS) if needed
-- ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;

-- Optional: Create a policy for public access (adjust based on your needs)
-- CREATE POLICY "Enable read access for all users" ON invoices FOR SELECT USING (true);
-- CREATE POLICY "Enable insert access for all users" ON invoices FOR INSERT WITH CHECK (true);
