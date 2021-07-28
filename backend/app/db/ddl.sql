CREATE DATABASE healthcaredb;
\c healthcaredb;

DROP TABLE IF EXISTS organisations CASCADE;
DROP TABLE IF EXISTS phones CASCADE;
DROP TABLE IF EXISTS specialities CASCADE;
DROP TABLE IF EXISTS qualifications CASCADE;
DROP TABLE IF EXISTS providers CASCADE;
DROP TABLE IF EXISTS provider_phone CASCADE;
DROP TABLE IF EXISTS provider_speciality CASCADE;
DROP TABLE IF EXISTS provider_qualification CASCADE;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE organisations (
  org_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  org_name VARCHAR(64) NOT NULL,
  org_location VARCHAR(64),
  org_address VARCHAR(256) NOT NULL,
  UNIQUE(org_name, org_location, org_address)
);

CREATE TABLE phones (
  phone_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  phone_country_code VARCHAR(3) NOT NULL,
  phone_number VARCHAR(15) NOT NULL,
  UNIQUE(phone_country_code, phone_number)
);

CREATE TABLE specialities (
  spec_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  spec_name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE qualifications (
  qual_id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  qual_name VARCHAR(64) UNIQUE NOT NULL
);

CREATE TABLE providers (
  provider_id UUID PRIMARY KEY DEFAULT uuid_generate_v4 (),
  provider_name VARCHAR(64) UNIQUE NOT NULL,
  provider_active BOOLEAN NOT NULL,
  provider_department VARCHAR(64),
  provider_org_id INTEGER REFERENCES organisations(org_id) ON DELETE CASCADE,
  provider_created_on TIMESTAMP NOT NULL,
  provider_last_modified_on TIMESTAMP,
  provider_search_tokens tsvector NOT NULL
);

CREATE TABLE provider_phone (
  provider_id UUID REFERENCES providers(provider_id) ON DELETE CASCADE,
  phone_id INTEGER REFERENCES phones(phone_id) ON DELETE CASCADE,
  PRIMARY KEY (provider_id, phone_id)
);

CREATE TABLE provider_speciality (
  provider_id UUID REFERENCES providers(provider_id) ON DELETE CASCADE,
  spec_id INTEGER REFERENCES specialities(spec_id) ON DELETE CASCADE,
  PRIMARY KEY (provider_id, spec_id)
);

CREATE TABLE provider_qualification (
  provider_id UUID REFERENCES providers(provider_id) ON DELETE CASCADE,
  qual_id INTEGER REFERENCES qualifications(qual_id) ON DELETE CASCADE,
  PRIMARY KEY (provider_id, qual_id)
);

CREATE INDEX idx_provider_search_tokens ON providers(provider_search_tokens);