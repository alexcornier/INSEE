--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: departementenvironnement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departementenvironnement (
    nb text NOT NULL,
    departements text,
    valorisationorga2013 double precision,
    valorisationorga2009 double precision,
    surfacearti2012 double precision,
    surfacearti2006 double precision,
    agriculturebio2016 double precision,
    agriculturebio2010 double precision,
    prodgranulat2014 double precision,
    prodgranulat2009 double precision,
    eolien2015 double precision,
    eolien2010 double precision,
    photovoltaique2015 double precision,
    photovoltaique2010 double precision,
    autre2015 double precision,
    autre2010 double precision
);


ALTER TABLE public.departementenvironnement OWNER TO postgres;

--
-- Name: departements; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departements (
    dep text NOT NULL,
    reg text,
    cheflieu text,
    tncc text,
    ncc text,
    nccenr text,
    libelle text
);


ALTER TABLE public.departements OWNER TO postgres;

--
-- Name: departementsocial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.departementsocial (
    nb text NOT NULL,
    departements text,
    esphommes2015 text,
    esphommes2010 double precision,
    espfemmes2015 double precision,
    espfemmes2010 double precision,
    popeloignee7min double precision,
    popzoneinondable2013 double precision,
    popzoneinondable2008 double precision
);


ALTER TABLE public.departementsocial OWNER TO postgres;

--
-- Name: regions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.regions (
    reg text NOT NULL,
    cheflieu text,
    tncc integer,
    ncc text,
    nccenr text,
    libelle text
);


ALTER TABLE public.regions OWNER TO postgres;

--
-- Name: regionsocial; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.regionsocial (
    nb text NOT NULL,
    region text,
    pauvrete double precision,
    jeunesnoninseres2014 double precision,
    jeunesnoninseres2009 double precision,
    poidseco double precision
);


ALTER TABLE public.regionsocial OWNER TO postgres;

--
-- Name: departementenvironnement departementenvironnement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departementenvironnement
    ADD CONSTRAINT departementenvironnement_pkey PRIMARY KEY (nb);


--
-- Name: departements departements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departements
    ADD CONSTRAINT departements_pkey PRIMARY KEY (dep);


--
-- Name: departementsocial departementsocial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.departementsocial
    ADD CONSTRAINT departementsocial_pkey PRIMARY KEY (nb);


--
-- Name: regions regions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.regions
    ADD CONSTRAINT regions_pkey PRIMARY KEY (reg);


--
-- Name: regionsocial regionsocial_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.regionsocial
    ADD CONSTRAINT regionsocial_pkey PRIMARY KEY (nb);


--
-- PostgreSQL database dump complete
--

