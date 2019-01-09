CREATE TABLE [Products] ( 
	[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
	[title] NVARCHAR(50)  NOT NULL,
    [price] INTEGER NOT NULL,
    [inventory_count] INTEGER DEFAULT 0
); 