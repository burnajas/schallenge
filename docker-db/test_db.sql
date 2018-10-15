CREATE TABLE public.items (
    id integer NOT NULL,
    name character varying(31),
    price double precision,
    report_id integer
);
CREATE TABLE public.reports (
    id integer NOT NULL,
    organization character varying(31),
    reported date
);
INSERT INTO public.items (id, name, price, report_id) VALUES (1, 'name1a', 22.21, 1);
INSERT INTO public.items (id, name, price, report_id) VALUES (2, 'name1b', 220.21, 1);
INSERT INTO public.items (id, name, price, report_id) VALUES (3, 'name2a', 2200.21, 2);
INSERT INTO public.items (id, name, price, report_id) VALUES (4, 'name2b', 22000.21, 2);
INSERT INTO public.reports (id, organization, reported) VALUES (1, 'suade', '2018-01-01');
INSERT INTO public.reports (id, organization, reported) VALUES (2, 'suade', '2018-02-02');

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.reports
    ADD CONSTRAINT reports_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.items
    ADD CONSTRAINT fk_reports_report_id FOREIGN KEY (report_id) REFERENCES public.reports(id);
