-- HealTrack AI - Database Schema for Supabase
-- Run this in your Supabase SQL Editor to set up the database

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ==================== PATIENTS TABLE ====================
CREATE TABLE patients (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    age INTEGER CHECK (age >= 0 AND age <= 150),
    medical_conditions TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on patients
ALTER TABLE patients ENABLE ROW LEVEL SECURITY;

-- RLS Policies for patients
CREATE POLICY "Users can view own patients" ON patients
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own patients" ON patients
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own patients" ON patients
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own patients" ON patients
    FOR DELETE USING (auth.uid() = user_id);

-- ==================== WOUND CASES TABLE ====================
CREATE TABLE wound_cases (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    patient_id UUID REFERENCES patients(id) ON DELETE CASCADE,
    wound_type TEXT,
    location TEXT,
    description TEXT,
    start_date DATE DEFAULT CURRENT_DATE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'healed', 'complicated')),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on wound_cases
ALTER TABLE wound_cases ENABLE ROW LEVEL SECURITY;

-- RLS Policies for wound_cases
CREATE POLICY "Users can view cases through patients" ON wound_cases
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM patients 
            WHERE patients.id = wound_cases.patient_id 
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert cases through patients" ON wound_cases
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM patients 
            WHERE patients.id = wound_cases.patient_id 
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update cases through patients" ON wound_cases
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM patients 
            WHERE patients.id = wound_cases.patient_id 
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete cases through patients" ON wound_cases
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM patients 
            WHERE patients.id = wound_cases.patient_id 
            AND patients.user_id = auth.uid()
        )
    );

-- ==================== WOUND SCANS TABLE ====================
CREATE TABLE wound_scans (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    case_id UUID REFERENCES wound_cases(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    pain_level INTEGER CHECK (pain_level >= 0 AND pain_level <= 10),
    notes TEXT,
    healing_score INTEGER CHECK (healing_score >= 0 AND healing_score <= 100),
    infection_risk NUMERIC(5,2),
    redness_score NUMERIC(5,2),
    size_mm2 NUMERIC(10,2),
    texture_stability NUMERIC(5,2),
    analysis_data JSONB DEFAULT '{}',
    analyzed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on wound_scans
ALTER TABLE wound_scans ENABLE ROW LEVEL SECURITY;

-- RLS Policies for wound_scans
CREATE POLICY "Users can view scans through cases" ON wound_scans
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = wound_scans.case_id
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert scans through cases" ON wound_scans
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = wound_scans.case_id
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update scans through cases" ON wound_scans
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = wound_scans.case_id
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete scans through cases" ON wound_scans
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = wound_scans.case_id
            AND patients.user_id = auth.uid()
        )
    );

-- ==================== REPORTS TABLE ====================
CREATE TABLE reports (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    case_id UUID REFERENCES wound_cases(id) ON DELETE CASCADE,
    scan_id UUID REFERENCES wound_scans(id) ON DELETE SET NULL,
    report_type TEXT NOT NULL CHECK (report_type IN ('doctor', 'patient', 'summary')),
    content JSONB NOT NULL DEFAULT '{}',
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS on reports
ALTER TABLE reports ENABLE ROW LEVEL SECURITY;

-- RLS Policies for reports
CREATE POLICY "Users can view reports through cases" ON reports
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = reports.case_id
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can insert reports through cases" ON reports
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = reports.case_id
            AND patients.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can delete reports through cases" ON reports
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM wound_cases
            JOIN patients ON patients.id = wound_cases.patient_id
            WHERE wound_cases.id = reports.case_id
            AND patients.user_id = auth.uid()
        )
    );

-- ==================== STORAGE BUCKET ====================
-- Create storage bucket for wound images (run in Supabase Dashboard)
-- Note: This needs to be done through the Supabase Dashboard or Storage API
-- INSERT INTO storage.buckets (id, name, public) VALUES ('wound-images', 'wound-images', true);

-- Storage RLS Policies (run after creating bucket)
-- CREATE POLICY "Allow authenticated uploads" ON storage.objects
--     FOR INSERT TO authenticated WITH CHECK (bucket_id = 'wound-images');

-- CREATE POLICY "Allow authenticated reads" ON storage.objects
--     FOR SELECT TO authenticated USING (bucket_id = 'wound-images');

-- ==================== INDEXES ====================
CREATE INDEX idx_patients_user_id ON patients(user_id);
CREATE INDEX idx_wound_cases_patient_id ON wound_cases(patient_id);
CREATE INDEX idx_wound_scans_case_id ON wound_scans(case_id);
CREATE INDEX idx_wound_scans_created_at ON wound_scans(created_at);
CREATE INDEX idx_reports_case_id ON reports(case_id);
CREATE INDEX idx_reports_generated_at ON reports(generated_at);

-- ==================== FUNCTIONS ====================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for patients updated_at
CREATE TRIGGER update_patients_updated_at
    BEFORE UPDATE ON patients
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to get dashboard stats
CREATE OR REPLACE FUNCTION get_dashboard_stats(p_user_id UUID)
RETURNS TABLE (
    total_patients BIGINT,
    active_cases BIGINT,
    total_scans BIGINT,
    avg_healing_score NUMERIC,
    high_risk_cases BIGINT
) AS $$
BEGIN
    RETURN QUERY
    WITH user_patients AS (
        SELECT id FROM patients WHERE user_id = p_user_id
    ),
    user_cases AS (
        SELECT wc.id, wc.status
        FROM wound_cases wc
        JOIN user_patients up ON wc.patient_id = up.id
    ),
    user_scans AS (
        SELECT ws.healing_score, ws.infection_risk, ws.case_id
        FROM wound_scans ws
        JOIN user_cases uc ON ws.case_id = uc.id
    )
    SELECT
        (SELECT COUNT(*) FROM user_patients) as total_patients,
        (SELECT COUNT(*) FROM user_cases WHERE status = 'active') as active_cases,
        (SELECT COUNT(*) FROM user_scans) as total_scans,
        (SELECT COALESCE(AVG(healing_score), 0) FROM user_scans WHERE healing_score IS NOT NULL) as avg_healing_score,
        (SELECT COUNT(DISTINCT case_id) FROM user_scans WHERE infection_risk > 70) as high_risk_cases;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ==================== SAMPLE DATA (Optional) ====================
-- Uncomment to add sample data for testing

/*
-- Sample patient
INSERT INTO patients (user_id, name, email, age, medical_conditions)
VALUES (
    'your-user-id-here',
    'John Doe',
    'john@example.com',
    45,
    ARRAY['Diabetes', 'Hypertension']
);

-- Sample wound case
INSERT INTO wound_cases (patient_id, wound_type, location, description)
VALUES (
    (SELECT id FROM patients LIMIT 1),
    'surgical',
    'Left forearm',
    'Post-surgical incision from fracture repair'
);
*/
