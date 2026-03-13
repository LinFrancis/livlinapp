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
