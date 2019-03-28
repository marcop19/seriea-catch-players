CREATE TABLE giocatori (
	gi_id int,
	gi_nrmaglia int,
	gi_nome varchar(100),
	gi_datanascita datetime,
	gi_ruolo varchar(20),
	gi_nazionalita varchar(50),
	gi_partitegiocate int,
	gi_golfatti int,
	gi_golsubiti int,
	gi_ammonizioni int,
	gi_ammespu int,
	gi_espulsioni int,
	gi_squadra varchar(50)
)

CREATE UNIQUE CLUSTERED INDEX [idx_gi_id] ON [dbo].[giocatori] (
	[gi_id] ASC
)