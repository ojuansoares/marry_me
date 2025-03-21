-- Drop existing types if they exist
DROP TYPE IF EXISTS public.usertype CASCADE;
DROP TYPE IF EXISTS public.weddingstatus CASCADE;
DROP TYPE IF EXISTS public.phototype CASCADE;

-- Create ENUM types
CREATE TYPE public.usertype AS ENUM ('noivo', 'convidado');
CREATE TYPE public.weddingstatus AS ENUM ('ativo', 'adiado', 'cancelado');
CREATE TYPE public.phototype AS ENUM ('noivos', 'convidados'); 