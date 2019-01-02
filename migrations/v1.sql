CREATE TABLE categories(
 id VARCHAR (70) PRIMARY KEY,
 name VARCHAR (250) NOT NULL,
 parent VARCHAR(70),
 created_at TIMESTAMP without time zone default (now() at time zone 'utc'),
 updated_at TIMESTAMP without time zone default (now() at time zone 'utc')
);

CREATE TABLE products(
 id VARCHAR (70) PRIMARY KEY,
 brand VARCHAR (150) NOT NULL,
 sku VARCHAR (150) NOT NULL,
 title VARCHAR (250) NOT NULL,
 description TEXT DEFAULT '',
 prod_type VARCHAR(250) NOT NULL,
 mrp BIGINT NOT NULL,
 available_price BIGINT NOT NULL,
 discount_percentage DECIMAL,
 discount_range VARCHAR (70),
 category VARCHAR (70) NOT NULL,
 created_at TIMESTAMP without time zone default (now() at time zone 'utc'),
 updated_at TIMESTAMP without time zone default (now() at time zone 'utc')
);

INSERT INTO categories(id, name, parent, created_at, updated_at) VALUES
 ('ea0950a8-5357-444a-9f55-f2366d9f63a9', 'Electronics', NULL, now(), now());

INSERT INTO categories(id, name, parent, created_at, updated_at) VALUES
 ('665f8fec-1ba3-4200-960f-c43a2022885f', 'Mobile', 'ea0950a8-5357-444a-9f55-f2366d9f63a9', now(), now());

INSERT INTO categories(id, name, parent, created_at, updated_at) VALUES
 ('e92fa102-9c79-44ec-b36c-35f0f3c63b26', 'Smartphone', '665f8fec-1ba3-4200-960f-c43a2022885f', now(), now());

INSERT INTO categories(id, name, parent, created_at, updated_at) VALUES
 ('a572aae1-8b8c-4a8d-a17d-4655b8487960', 'Android', 'e92fa102-9c79-44ec-b36c-35f0f3c63b26', now(), now());

INSERT INTO categories(id, name, parent, created_at, updated_at) VALUES
 ('2977d7ea-b3a6-47f2-8ded-8512c1d6e29e', 'ios', 'e92fa102-9c79-44ec-b36c-35f0f3c63b26', now(), now());