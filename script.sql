insert into "livePlan_tipoinversioninicial" (id,tipo) values (1, 'Activos fijos'),
                                                   (2, 'Gastos preoperativos y de constitucion'),
                                                   (3, 'Capital de trabajo inicial');

INSERT INTO "livePlan_gastosoperacion" (nombre, referencia) VALUES
('Sueldos gerenciales (incluye prestaciones sociales)', 1050.00),
('Sueldos de colaboradores (incluye prestaciones)', 1950.00),
('Uniformes', 30.00),
('Honorarios', 50.00),
('Publicidad', 150.00),
('Teléfono', 50.00),
('Energía eléctrica', 120.00),
('Agua', 42.00),
('Gas', 180.00),
('Gasolina', 120.00),
('Mantenimiento de vehículos', 45.00),
('Mantenimiento de planta y equipo', 63.00),
('Seguros contra daños', 65.00),
('Papelería y útiles para oficina', 23.00),
('Gastos de viaje/representación', NULL),
('Renta de locales', 500.00),
('Otros', NULL);

INSERT INTO "livePlan_categorias_costos" (id, nombre) VALUES
(1, 'Mano de obra'),(2, 'Materia prima'),(3, 'Gastos indirectos');