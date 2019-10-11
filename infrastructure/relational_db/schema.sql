--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Debian 11.5-1.pgdg90+1)
-- Dumped by pg_dump version 11.5

-- Started on 2019-10-09 21:38:38

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

--
-- TOC entry 2 (class 3079 OID 16394)
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- TOC entry 2937 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- TOC entry 213 (class 1255 OID 16463)
-- Name: tr_set_timestamps_for_bike_type(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.tr_set_timestamps_for_bike_type() RETURNS trigger
    LANGUAGE plpgsql
    AS $$BEGIN
	IF NEW.created_on IS NULL THEN
	   UPDATE public.bike_type SET created_on = now() WHERE id = NEW.id;
	END IF;
	UPDATE public.bike_type SET updated_on = now() WHERE id = NEW.id;
END;$$;


ALTER FUNCTION public.tr_set_timestamps_for_bike_type() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 199 (class 1259 OID 16428)
-- Name: bike; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bike (
    id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    purchase_price numeric,
    selling_price numeric,
    status_key smallint,
    user_id uuid,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    created_by uuid,
    updated_by uuid,
    bike_type_id uuid,
    is_public boolean DEFAULT false NOT NULL
);


ALTER TABLE public.bike OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 16451)
-- Name: bike_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bike_status (
    id smallint NOT NULL,
    value character varying
);


ALTER TABLE public.bike_status OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 16405)
-- Name: bike_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bike_type (
    id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    title character varying NOT NULL,
    description character varying,
    stars numeric,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    created_by uuid,
    updated_by uuid
);


ALTER TABLE public.bike_type OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 16437)
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    created_by uuid,
    updated_by uuid,
    name character varying
);


ALTER TABLE public.role OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 16414)
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    id uuid DEFAULT public.uuid_generate_v1() NOT NULL,
    created_on timestamp without time zone,
    updated_on timestamp without time zone,
    created_by uuid,
    updated_by uuid,
    email character varying NOT NULL,
    name character varying
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 16446)
-- Name: user_role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_role (
    user_id uuid NOT NULL,
    role_id uuid
);


ALTER TABLE public.user_role OWNER TO postgres;

--
-- TOC entry 2785 (class 2606 OID 16436)
-- Name: bike bike_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT bike_pkey PRIMARY KEY (id);


--
-- TOC entry 2791 (class 2606 OID 16465)
-- Name: bike_status bike_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike_status
    ADD CONSTRAINT bike_status_pkey PRIMARY KEY (id);


--
-- TOC entry 2781 (class 2606 OID 16413)
-- Name: bike_type bike_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike_type
    ADD CONSTRAINT bike_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2787 (class 2606 OID 16445)
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- TOC entry 2783 (class 2606 OID 16421)
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- TOC entry 2789 (class 2606 OID 16450)
-- Name: user_role user_role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT user_role_pkey PRIMARY KEY (user_id);


--
-- TOC entry 2796 (class 2606 OID 16473)
-- Name: bike bike_type_id_fkey_bike_type; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT bike_type_id_fkey_bike_type FOREIGN KEY (bike_type_id) REFERENCES public.bike_type(id) NOT VALID;


--
-- TOC entry 2938 (class 0 OID 0)
-- Dependencies: 2796
-- Name: CONSTRAINT bike_type_id_fkey_bike_type ON bike; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON CONSTRAINT bike_type_id_fkey_bike_type ON public.bike IS 'column_fkey_table';


--
-- TOC entry 2792 (class 2606 OID 24601)
-- Name: bike_type created_by_fkey_bike_type_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike_type
    ADD CONSTRAINT created_by_fkey_bike_type_user FOREIGN KEY (created_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2798 (class 2606 OID 24591)
-- Name: bike created_by_fkey_bike_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT created_by_fkey_bike_user FOREIGN KEY (created_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2801 (class 2606 OID 24611)
-- Name: role created_by_fkey_role_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT created_by_fkey_role_user FOREIGN KEY (created_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2794 (class 2606 OID 24621)
-- Name: user created_by_fkey_user_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT created_by_fkey_user_user FOREIGN KEY (created_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2804 (class 2606 OID 24581)
-- Name: user_role role_id_fkey_role; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT role_id_fkey_role FOREIGN KEY (role_id) REFERENCES public.role(id) NOT VALID;


--
-- TOC entry 2800 (class 2606 OID 24632)
-- Name: bike status_key_fkey_bike_bike_status; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT status_key_fkey_bike_bike_status FOREIGN KEY (status_key) REFERENCES public.bike_status(id) NOT VALID;


--
-- TOC entry 2793 (class 2606 OID 24606)
-- Name: bike_type updated_by_fkey_bike_type_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike_type
    ADD CONSTRAINT updated_by_fkey_bike_type_user FOREIGN KEY (updated_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2799 (class 2606 OID 24596)
-- Name: bike updated_by_fkey_bike_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT updated_by_fkey_bike_user FOREIGN KEY (updated_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2802 (class 2606 OID 24616)
-- Name: role updated_by_fkey_role_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT updated_by_fkey_role_user FOREIGN KEY (updated_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2795 (class 2606 OID 24626)
-- Name: user updated_by_fkey_user_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT updated_by_fkey_user_user FOREIGN KEY (updated_by) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2803 (class 2606 OID 24576)
-- Name: user_role user_id_fkey_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_role
    ADD CONSTRAINT user_id_fkey_user FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;


--
-- TOC entry 2797 (class 2606 OID 24586)
-- Name: bike user_id_fkey_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bike
    ADD CONSTRAINT user_id_fkey_user FOREIGN KEY (user_id) REFERENCES public."user"(id) NOT VALID;


-- Completed on 2019-10-09 21:38:38

--
-- PostgreSQL database dump complete
--

