-- =====================================================
-- LivLin v12 — Setup SQL para Supabase
-- Ejecutar en: Supabase → SQL Editor → New Query
-- =====================================================

-- 1. Tabla principal de diagnósticos
create table if not exists visits (
  id          text primary key,
  data        jsonb not null,
  created_at  timestamptz default now(),
  updated_at  timestamptz default now()
);

-- 2. Habilitar Row Level Security
alter table visits enable row level security;

-- 3. Política: acceso total para service_role (la app)
create policy "service_role_all" on visits
  for all
  using (true)
  with check (true);

-- =====================================================
-- Después de ejecutar este SQL:
-- Ir a Storage → New bucket → Nombre: fotos-livlin
-- Público: NO (privado)
-- =====================================================

-- Tabla de fotos (base64) — v2.0
create table if not exists photos (
  id         text primary key,
  visit_id   text references visits(id) on delete cascade,
  filename   text not null,
  label      text default '',
  mimetype   text default 'image/jpeg',
  data       text not null,  -- base64 encoded
  created_at timestamptz default now()
);

alter table photos enable row level security;
create policy "service role full access photos"
on photos for all using (true) with check (true);

create index if not exists photos_visit_id_idx on photos(visit_id);
