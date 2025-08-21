INSERT INTO public.crime(description) VALUES
('Assault'),
('Battery'),
('Arson'),
('Homicide'),
('Robbery'),
('Driving Under the Influence');

INSERT INTO public.cell(cellnum, numberofbeds) VALUES
(10, 3),
(11, 2),
(12, 2);

INSERT INTO public.user(username,password) VALUES
('admin','JailPassword')