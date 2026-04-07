-- =====================================================
-- LivLin v6.0 — Setup SQL para Supabase
-- Ejecutar en: Supabase → SQL Editor → New Query
-- =====================================================

-- 1. Tabla principal de diagnósticos
create table if not exists visits (
  id          text primary key,
  data        jsonb not null,
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);
alter table visits enable row level security;
create policy "service_role_all" on visits
  for all using (true) with check (true);

-- 2. Tabla de usuarios (v6.0 — persistente en Supabase)
-- Los usuarios se guardan aquí para sobrevivir redeploys en Streamlit Cloud
create table if not exists users (
  username      text primary key,
  password_hash text not null,
  role          text default 'user',
  display_name  text default '',
  space_name    text default '',
  visit_id      text references visits(id) on delete set null,
  created_at    timestamptz default now(),
  updated_at    timestamptz default now()
);
alter table users enable row level security;
create policy "service_role_all_users" on users
  for all using (true) with check (true);

-- 3. Tabla de fotos (base64)
create table if not exists photos (
  id         text primary key,
  visit_id   text references visits(id) on delete cascade,
  filename   text not null,
  label      text default '',
  mimetype   text default 'image/jpeg',
  data       text not null,
  created_at timestamptz default now()
);
alter table photos enable row level security;
create policy "service_role_full_access_photos"
  on photos for all using (true) with check (true);
create index if not exists photos_visit_id_idx on photos(visit_id);

-- =====================================================
-- NOTA v6.0: La tabla users reemplaza users.json
-- Los usuarios creados desde el panel admin persisten
-- aunque se haga redeploy en Streamlit Cloud.
-- Si ya tenías usuarios en users.json, créalos
-- manualmente desde el panel de administración.
-- =====================================================
