CREATE TABLE "departementenvironnement" (
  "nb" text PRIMARY KEY,
  "departements" text,
  "valorisationorga2013" float,
  "valorisationorga2009" float,
  "surfacearti2012" float,
  "surfacearti2006" float,
  "agriculturebio2016" float,
  "agriculturebio2010" float,
  "prodgranulat2014" float,
  "prodgranulat2009" float,
  "eolien2015" float,
  "eolien2010" float,
  "photovoltaique2015" float,
  "photovoltaique2010" float,
  "autre2015" float,
  "autre2010" float
);

CREATE TABLE "departements" (
  "dep" text PRIMARY KEY,
  "reg" text,
  "cheflieu" text,
  "tncc" text,
  "ncc" text,
  "nccenr" text,
  "libelle" text
);

CREATE TABLE "departementsocial" (
  "nb" text PRIMARY KEY,
  "departements" text,
  "esphommes2015" text,
  "esphommes2010" float,
  "espfemmes2015" float,
  "espfemmes2010" float,
  "popeloignee7min" float,
  "popzoneinondable2013" float,
  "popzoneinondable2008" float
);

CREATE TABLE "regions" (
  "reg" text PRIMARY KEY,
  "cheflieu" text,
  "tncc" integer,
  "ncc" text,
  "nccenr" text,
  "libelle" text
);

CREATE TABLE "regionsocial" (
  "nb" text PRIMARY KEY,
  "region" text,
  "pauvrete" float,
  "jeunesnoninseres2014" float,
  "jeunesnoninseres2009" float,
  "poidseco" float
);

ALTER TABLE "departementenvironnement" ADD FOREIGN KEY ("nb") REFERENCES "departements" ("dep");

ALTER TABLE "departementsocial" ADD FOREIGN KEY ("nb") REFERENCES "departements" ("dep");

ALTER TABLE "departements" ADD FOREIGN KEY ("reg") REFERENCES "regions" ("reg");

ALTER TABLE "regionsocial" ADD FOREIGN KEY ("nb") REFERENCES "regions" ("reg");
