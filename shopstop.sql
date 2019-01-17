CREATE TABLE IF NOT EXISTS [Products] ( 
	[id] INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT, 
	[title] NVARCHAR(50)  NOT NULL,
    [price] INTEGER NOT NULL,
    [inventory_count] INTEGER DEFAULT 0
); 

CREATE TABLE IF NOT EXISTS [Carts] (
    [id] INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    [total_cost] INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS [ProductsCarts] (
    [cart_id] INTEGER,
    [product_id] INTEGER,
        FOREIGN KEY (cart_id) REFERENCES Carts(id)
        FOREIGN KEY (product_id) REFERENCES Products(id)
);