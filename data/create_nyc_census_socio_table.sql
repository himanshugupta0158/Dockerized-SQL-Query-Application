--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: nyc_census_sociodata; Type: TABLE; Schema: public; Owner: pramsey; Tablespace: 
--

CREATE TABLE nyc_census_sociodata (
    tractid character varying,
    transit_total integer,
    transit_private integer,
    transit_public integer,
    transit_walk integer,
    transit_other integer,
    transit_none integer,
    transit_time_mins real,
    family_count integer,
    family_income_median integer,
    family_income_mean integer,
    family_income_aggregate integer,
    edu_total integer,
    edu_no_highschool_dipl integer,
    edu_highschool_dipl integer,
    edu_college_dipl integer,
    edu_graduate_dipl integer
);