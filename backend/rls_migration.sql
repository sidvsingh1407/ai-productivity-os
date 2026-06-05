BEGIN;

-- Running upgrade manual_001 -> 7a8b9c0d1e2f

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON users
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON organizations
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE org_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON org_members
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE audits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON audits
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON workflows
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON reports
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE export_jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON export_jobs
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON subscriptions
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON invitations
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE audit_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON audit_versions
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE blueprints ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON blueprints
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE integration_results ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON integration_results
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE billing_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON billing_plans
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE contact_leads ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON contact_leads
            AS PERMISSIVE FOR ALL
            USING (current_user NOT IN ('anon', 'authenticated'))
            WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

UPDATE alembic_version SET version_num='7a8b9c0d1e2f' WHERE alembic_version.version_num = 'manual_001';

COMMIT;
