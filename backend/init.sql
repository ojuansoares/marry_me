-- Drop existing types if they exist
DROP TYPE IF EXISTS public.usertype CASCADE;
DROP TYPE IF EXISTS public.weddingstatus CASCADE;
DROP TYPE IF EXISTS public.phototype CASCADE;

-- Create ENUM types
CREATE TYPE public.usertype AS ENUM ('fiance', 'guest');
CREATE TYPE public.weddingstatus AS ENUM ('active', 'postponed', 'cancelled');
CREATE TYPE public.phototype AS ENUM ('couple', 'guests'); 